# Copyright (c) 2010-2012, GEM Foundation.
#
# OpenQuake is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake.  If not, see <http://www.gnu.org/licenses/>.


"""
Celery tasks for extracting subset data from 5D result matrices.
"""

import numpy
from celery.task import task
import h5py

from openquake.shapes import hdistance
from openquake.calculators.hazard.disagg import FULL_DISAGG_MATRIX

# Disabling pylint checks: too many local vars, too many arguments,
# unused argument.
# pylint: disable=W0613,R0913,R0914

#: Data type used for matrices is double precision float with "native"
#: byte order. The same is used by java side.
DATA_TYPE = numpy.float64


def fulldisaggmatrix(site, full_matrix, *args, **kwargs):
    """
    Full matrix: returns ``full_matrix`` argument (5D).
    """
    return full_matrix


def magpmf(site, full_matrix,
           lat_bin_edges, lon_bin_edges, distance_bin_edges,
           nlat, nlon, nmag, neps, ntrt, ndist):
    """
    Magnitude PMF extractor (1D).
    """
    shape = [nmag - 1]
    ds = numpy.zeros(shape, DATA_TYPE)
    for i in xrange(nmag - 1):
        ds[i] = sum(full_matrix[j][k][i][l][m]
                    for j in xrange(nlat - 1)
                    for k in xrange(nlon - 1)
                    for l in xrange(neps - 1)
                    for m in xrange(ntrt))
    return ds


def _distgen(site, lat_bin_edges, lon_bin_edges, distance_bin_edges,
             nlat, nlon, nmag, neps, ntrt, ndist):
    """
    Common part of the code for all extractors that compute distances.
    """
    slat = site.latitude
    slon = site.longitude
    enumeration = ((i, j, k, l, m)
                   for i in xrange(nlat - 1)
                   for j in xrange(nlon - 1)
                   for k in xrange(nmag - 1)
                   for l in xrange(neps - 1)
                   for m in xrange(ntrt))
    for i, j, k, l, m in enumeration:
        meanlat = (lat_bin_edges[i] + lat_bin_edges[i + 1]) / 2
        meanlon = (lon_bin_edges[j] + lon_bin_edges[j + 1]) / 2
        dist = hdistance(meanlat, meanlon, slat, slon)
        if dist < distance_bin_edges[0] \
                or dist > distance_bin_edges[-1]:
            continue
        ii = 0
        for ii in xrange(ndist - 1):
            if dist >= distance_bin_edges[ii] \
                    and dist < distance_bin_edges[ii + 1]:
                break
        yield i, j, k, l, m, ii


def distpmf(site, full_matrix,
            lat_bin_edges, lon_bin_edges, distance_bin_edges,
            nlat, nlon, nmag, neps, ntrt, ndist):
    """
    Distance PMF extractor (1D).
    """
    shape = [ndist - 1]
    ds = numpy.zeros(shape, DATA_TYPE)
    distgen = _distgen(site, lat_bin_edges, lon_bin_edges, distance_bin_edges,
                       nlat, nlon, nmag, neps, ntrt, ndist)
    for i, j, k, l, m, ii in distgen:
        ds[ii] += full_matrix[i][j][k][l][m]
    return ds


def trtpmf(site, full_matrix,
           lat_bin_edges, lon_bin_edges, distance_bin_edges,
           nlat, nlon, nmag, neps, ntrt, ndist):
    """
    Tectonic region type PMF extractor (1D).
    """
    shape = [ntrt]
    ds = numpy.zeros(shape, DATA_TYPE)
    for i in xrange(ntrt):
        ds[i] = sum(full_matrix[j][k][l][m][i]
                    for j in xrange(nlat - 1)
                    for k in xrange(nlon - 1)
                    for l in xrange(nmag - 1)
                    for m in xrange(neps - 1))
    return ds


def magdistpmf(site, full_matrix,
               lat_bin_edges, lon_bin_edges, distance_bin_edges,
               nlat, nlon, nmag, neps, ntrt, ndist):
    """
    Magnitude-distance PMF extractor (2D).
    """
    ndist = len(distance_bin_edges)
    shape = [nmag - 1, ndist - 1]
    ds = numpy.zeros(shape, DATA_TYPE)
    distgen = _distgen(site, lat_bin_edges, lon_bin_edges, distance_bin_edges,
                       nlat, nlon, nmag, neps, ntrt, ndist)
    for i, j, k, l, m, ii in distgen:
        ds[k][ii] += full_matrix[i][j][k][l][m]
    return ds


def magdistepspmf(site, full_matrix,
                  lat_bin_edges, lon_bin_edges, distance_bin_edges,
                  nlat, nlon, nmag, neps, ntrt, ndist):
    """
    Magnitude-distance-epsilon PMF extractor (3D).
    """
    shape = [nmag - 1, ndist - 1, neps - 1]
    ds = numpy.zeros(shape, DATA_TYPE)
    distgen = _distgen(site, lat_bin_edges, lon_bin_edges, distance_bin_edges,
                       nlat, nlon, nmag, neps, ntrt, ndist)
    for i, j, k, l, m, ii in distgen:
        ds[k][ii][l] += full_matrix[i][j][k][l][m]
    return ds


def latlonpmf(site, full_matrix,
              lat_bin_edges, lon_bin_edges, distance_bin_edges,
              nlat, nlon, nmag, neps, ntrt, ndist):
    """
    Latitude-longitude PMF extractor (2D).
    """
    shape = [nlat - 1, nlon - 1]
    ds = numpy.zeros(shape, DATA_TYPE)
    for i in xrange(nlat - 1):
        for j in xrange(nlon - 1):
            ds[i][j] = sum(full_matrix[i][j][k][l][m]
                           for k in xrange(nmag - 1)
                           for l in xrange(neps - 1)
                           for m in xrange(ntrt))
    return ds


def latlonmagpmf(site, full_matrix,
                 lat_bin_edges, lon_bin_edges, distance_bin_edges,
                 nlat, nlon, nmag, neps, ntrt, ndist):
    """
    Latitude-longitude-magnitude PMF extractor (3D).
    """
    shape = [nlat - 1, nlon - 1, nmag - 1]
    ds = numpy.zeros(shape, DATA_TYPE)
    for i in xrange(nlat - 1):
        for j in xrange(nlon - 1):
            for k in xrange(nmag - 1):
                ds[i][j][k] = sum(full_matrix[i][j][k][l][m]
                                  for l in xrange(neps - 1)
                                  for m in xrange(ntrt))
    return ds


def latlonmagepspmf(site, full_matrix,
                    lat_bin_edges, lon_bin_edges, distance_bin_edges,
                    nlat, nlon, nmag, neps, ntrt, ndist):
    """
    Latitude-longitude-magnitude-epsilon PMF extractor (4D).
    """
    shape = [nlat - 1, nlon - 1, nmag - 1, neps - 1]
    ds = numpy.zeros(shape, DATA_TYPE)
    for i in xrange(nlat - 1):
        for j in xrange(nlon - 1):
            for k in xrange(nmag - 1):
                for l in xrange(neps - 1):
                    ds[i][j][k][l] = sum(full_matrix[i][j][k][l][m]
                                         for m in xrange(ntrt))
    return ds


def magtrtpmf(site, full_matrix,
              lat_bin_edges, lon_bin_edges, distance_bin_edges,
              nlat, nlon, nmag, neps, ntrt, ndist):
    """
    Magnitude -- tectonic region type PMF extractor (2D).
    """
    shape = [nmag - 1, ntrt]
    ds = numpy.zeros(shape, DATA_TYPE)
    for i in xrange(nmag - 1):
        for j in xrange(ntrt):
            ds[i][j] = sum(full_matrix[k][l][i][m][j]
                           for k in xrange(nlat - 1)
                           for l in xrange(nlon - 1)
                           for m in xrange(neps - 1))
    return ds


def latlontrtpmf(site, full_matrix,
                 lat_bin_edges, lon_bin_edges, distance_bin_edges,
                 nlat, nlon, nmag, neps, ntrt, ndist):
    """
    Latitude -- longitude -- tectonic region type PMF extractor (3D).
    """
    shape = [nlat - 1, nlon - 1, ntrt]
    ds = numpy.zeros(shape, DATA_TYPE)
    for i in xrange(nlat - 1):
        for j in xrange(nlon - 1):
            for k in xrange(ntrt):
                ds[i][j][k] = sum(full_matrix[i][j][l][m][k]
                                  for l in xrange(nmag - 1)
                                  for m in xrange(neps - 1))
    return ds


#: Mapping "extractor name -- extractor function".
#: Used by :func:`extract_subsets`.
SUBSET_EXTRACTORS = {
    "MagPMF": magpmf,
    "DistPMF": distpmf,
    "TRTPMF": trtpmf,
    "MagDistPMF": magdistpmf,
    "MagDistEpsPMF": magdistepspmf,
    "LatLonPMF": latlonpmf,
    "LatLonMagPMF": latlonmagpmf,
    "LatLonMagEpsPMF": latlonmagepspmf,
    "MagTRTPMF": magtrtpmf,
    "LatLonTRTPMF": latlontrtpmf,
    "FullDisaggMatrix": fulldisaggmatrix,
}


@task
def extract_subsets(
    job_id, site, full_matrix_path, lat_bin_edges, lon_bin_edges,
    mag_bin_edges, eps_bin_edges, distance_bin_edges, target_path, subsets):
    """
    Celery task for extracting subsets from full disaggregation matrix.

    All subsets are saved in one file with dataset name equal
    to the extractor name.

    :param int job_id: current job identifier.
    :param site: :class:`openquake.shapes.Site` instance.
    :param full_matrix_path: Path to the full matrix file in hdf5 format.
    :param lat_bin_edges: Corresponds to ``LATITUDE_BIN_LIMITS`` job parameter.
    :param lon_bin_edges:
        Corresponds to ``LONGITUDE_BIN_LIMITS`` job parameter.
    :param mag_bin_edges:
        Corresponds to ``MAGNITUDE_BIN_LIMITS`` job parameter.
    :param eps_bin_edges: Corresponds to ``EPSILON_BIN_LIMITS`` job parameter.
    :param distance_bin_edges:
        Corresponds to ``DISTANCE_BIN_LIMITS`` job parameter.
    :param target_path: Path to the file where the result should be saved.
    :param subsets: A list of PMF extractor names.
    """
    nlat = len(lat_bin_edges)
    nlon = len(lon_bin_edges)
    nmag = len(mag_bin_edges)
    neps = len(eps_bin_edges)
    ntrt = 5
    ndist = len(distance_bin_edges)
    subsets = set(subsets)
    assert not subsets - set(SUBSET_EXTRACTORS)
    assert subsets
    with h5py.File(full_matrix_path, 'r') as source:
        full_matrix = source[FULL_DISAGG_MATRIX].value
    with h5py.File(target_path, 'w') as target:
        for subset_type in subsets:
            extractor = SUBSET_EXTRACTORS[subset_type]
            dataset = extractor(
                site, full_matrix,
                lat_bin_edges, lon_bin_edges, distance_bin_edges,
                nlat, nlon, nmag, neps, ntrt, ndist
            )
            target.create_dataset(subset_type, data=dataset)
