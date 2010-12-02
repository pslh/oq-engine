# pylint: disable-msg=W0232

""" Probabilistic Event Mixin: 

    Defines the behaviour of a Job. Calls the compute_risk task

"""

import math
import os
import json
import sys

import numpy
from celery.exceptions import TimeoutError

from openquake import hazard
from openquake import job
from openquake import kvs
from openquake import logs
from openquake import producer
from openquake import risk
from openquake import settings
from openquake import shapes

from openquake.risk import probabilistic_event_based
from openquake.risk import job as risk_job
from openquake.output.risk import RiskXMLWriter
from openquake.parser import exposure
from openquake.parser import hazard as hazparser
from openquake.parser import vulnerability
from openquake.risk import tasks
from openquake.risk.job import output, RiskJobMixin


LOGGER = logs.LOG

DEFAULT_conditional_loss_poe = 0.01


def preload(fn):
    """ Preload decorator """
    def preloader(self, *args, **kwargs):
        """A decorator for preload steps that must run on the Jobber"""

        self.store_exposure_assets()
        self.store_vulnerability_model()

        return fn(self, *args, **kwargs)
    return preloader


class ProbabilisticEventMixin:
    """ Mixin for Probalistic Event Risk Job """

    @preload
    @output
    def execute(self):
        """ Execute a ProbabilisticLossRatio Job """
        results = []
        tasks = []
        for block_id in self.blocks_keys:
            LOGGER.debug("starting task block, block_id = %s of %s" 
                        % (block_id, len(self.blocks_keys)))
            # pylint: disable-msg=E1101
            tasks.append(risk_job.compute_risk.delay(self.id, block_id))

        # task compute_risk has return value 'True' (writes its results to
        # memcache).
        for task in tasks:
            try:
                # TODO(chris): Figure out where to put that timeout.
                task.wait(timeout=None)
            except TimeoutError:
                # TODO(jmc): Cancel and respawn this task
                return []
        return results # TODO(jmc): Move output from being a decorator

    def slice_gmfs(self, block_id):
        """Load and collate GMF values for all sites in this block. """
        # TODO(JMC): Confirm this works regardless of the method of haz calc.
        histories = int(self['NUMBER_OF_SEISMICITY_HISTORIES'])
        realizations = int(self['NUMBER_OF_HAZARD_CURVE_CALCULATIONS'])
        timespan = float(self['INVESTIGATION_TIME'])
        num_ses = histories * realizations
        tses = num_ses * timespan
        
        block = job.Block.from_kvs(block_id)
        sites_list = block.sites
        gmfs = {}
        for site in sites_list:
            risk_point = self.region.grid.point_at(site)
            key = "%s!%s" % (risk_point.row, risk_point.column)
            gmfs[key] = {"IMLs": [], "TSES": tses, "TimeSpan": timespan}
            
        ses_keys = []    
        for i in range(0, histories):
            ses_keys.extend([kvs.generate_product_key(
                        self.id, hazard.STOCHASTIC_SET_TOKEN, 
                        "%s!%s" % (i, j)) for j in range(0, realizations)])
            
        seses = kvs.get_client().get_multi(ses_keys).values()
        for ses in seses:
            fieldset = shapes.FieldSet.from_json(ses, self.region.grid)
            for field in fieldset:
                for key in gmfs.keys():
                    (row, col) = key.split("!")
                    gmfs[key]["IMLs"].append(field.get(int(row), int(col)))
        self.gmf_slices = gmfs

    def store_exposure_assets(self):
        """ Load exposure assets and write to memcache """
        exposure_parser = exposure.ExposurePortfolioFile("%s/%s" % 
            (self.base_path, self.params[job.EXPOSURE]))

        for site, asset in exposure_parser.filter(self.region):
            # TODO(JMC): This is kludgey
            asset['lat'] = site.latitude
            asset['lon'] = site.longitude
            point = self.region.grid.point_at(site)
            asset_key = risk.asset_key(self.id, point.row, point.column)
            kvs.get_client().rpush(asset_key, json.JSONEncoder().encode(asset))

    def store_vulnerability_model(self):
        """ load vulnerability and write to memcache """
        vulnerability.load_vulnerability_model(self.id,
            "%s/%s" % (self.base_path, self.params["VULNERABILITY"]))
    
    def assets_at_point(self, point):
        decoder = json.JSONDecoder()
        asset_key = risk.asset_key(self.id, point.row, point.column)
        asset_list = kvs.get_client().lrange(asset_key, 0, -1)
        return [decoder.decode(x) for x in asset_list]
                
    def compute_risk(self, block_id, **kwargs):
        """This task computes risk for a block of sites. It requires to have
        pre-initialized in memcache:
         1) list of sites
         2) gmfs
         3) exposure portfolio (=assets)
         4) vulnerability

        TODO(fab): make conditional_loss_poe (set of probabilities of exceedance
        for which the loss computation is done) a list of floats, and read it from
        the job configuration.
        """

        self.conditional_loss_poes = [float(x) for x in self.params.get(
                    'CONDITIONAL_LOSS_POE', "0.01").split()]
        self.slice_gmfs(block_id)
        self.vuln_curves = \
                vulnerability.load_vulnerability_curves_from_kvs(self.job_id)

        block = job.Block.from_kvs(block_id)
        curves = {}        
        
        # TODO(jmc): DONT assumes that hazard and risk grid are the same
        for point in block.grid(self.region):
            gmf_key = "%s!%s" % (point.row, point.column)
            gmf_slice = self.gmf_slices[gmf_key]
            for asset in self.assets_at_point(point):
                curves.update(
                        self.compute_risk_for_asset(asset, gmf_slice, point))
        kvs.get_client().mset(curves)
        return True
    
    def compute_risk_for_asset(self, asset, gmf_slice, point):
        curves = {}
        LOGGER.debug("processing asset %s" % (asset))
        if not asset["VulnerabilityFunction"] in self.vuln_curves:
            LOGGER.error("Unknown vuln function %s for asset %s"
                % (asset["VulnerabilityFunction"], asset["AssetID"]))
            return curves
        
        loss_ratio_curve = probabilistic_event_based.compute_loss_ratio_curve(
                self.vuln_curves[asset["VulnerabilityFunction"]], gmf_slice)
        if loss_ratio_curve is None:
            return curves
            
        key = risk.loss_ratio_key(
                self.id, point.row, point.column, asset["AssetID"])
        curves[key] = loss_ratio_curve.to_json()
            
        loss_curve = loss_ratio_curve.rescale_abscissae(asset["AssetValue"])
        key = risk.loss_curve_key(
                self.id, point.row, point.column, asset["AssetID"])
        curves[key] = loss_curve.to_json()
        
        for loss_poe in self.conditional_loss_poes:
            loss = probabilistic_event_based. \
                    compute_conditional_loss(loss_curve, loss_poe)
            key = risk.loss_key(self.id, point.row, point.column, 
                    asset["AssetID"], loss_poe)
            curves[key] = loss
        return curves


RiskJobMixin.register("Probabilistic Event", ProbabilisticEventMixin)
