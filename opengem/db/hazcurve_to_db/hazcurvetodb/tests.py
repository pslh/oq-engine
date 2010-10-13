#!/usr/bin/env python
# encoding: utf-8
"""
Test cases for the hazardcurve_to_db user story.
This user story maps hazard curve objects to the database using
Django/GeoDjango OR Mapping. 
There is a test to create a record for the following tables and check 
if it exists once created.
  Intensitymeasuretype
  Logictreestruc
  Hazardsoftware
  Calculationowner

Several records have to exist first before the hazard curve is written, namely:
IntensityMeasureType
LogicTreeStru
HazardSoftware
Calculationowner
HazardInputLtreeModel
HazardCalculation

The following have to be created if non-existent:
Geopoint
HazardCurve

The values used for the hazard curve comes from the 
/results_Europe_2010-03-26_14:49:07/
Europe_hazardCurves_PGA_50.0yr_mean.dat
for Point: -3.1, 72.6
"""

import sys
sys.path.append('/home/apm/Projects/opengem')
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from psycopg2 import IntegrityError
from django.contrib.gis.geos import *

import unittest
from ordereddict import *
import datetime

from opengem import test
from opengem import shapes
from hazcurvetodb.models import *

# input test values
intmeasuretype = "PGA"
hazsoftware =  "OPENSHA"
logtreestrname = "EULOGTREE"
calcownercode = "DM"  
calcgrpcode = "OPENGEMDEV"
datenow = datetime.datetime.now()
hilmsname = "Europe_LTree_V1"
#counterclockwise
hilmpolygonwkt = "POLYGON ((50 5, 150 5, 50 60, 50 5))"
#clockwise hilmpolygonwkt = "POLYGON ((50 5, 50 60, 150 60, 150 5, 50 5))"
hazcalcname = "Europe_Calc"
geopoint_WKT = "POINT (-3.1 +72.6)"
hazcurvename = "Test_EuHazcrv"
INVALID_POINT_WKT = "POINT (181 91)"
POINT_WKT = "POINT (-3.1000 72.6000)"   

# intmeaslvl or prob of exceedance, a list of 19 values 
intmeaslvls = [5.0000e-03, 7.0000e-03, 9.8000e-03, 1.3700e-02, 1.9200e-02,
                   2.6900e-02, 3.7600e-02, 5.2700e-02, 7.3800e-02, 1.0300e-01,
                   1.4500e-01, 2.0300e-01, 2.8400e-01, 3.9700e-01, 5.5600e-01,
                   7.7800e-01, 1.0900e+00, 1.5200e+00, 2.1300e+00]
# pgaval corr to intmeaslvl
pgavals = [9.9967e-01, 9.9618e-01, 9.7180e-01, 8.7730e-01, 6.7090e-01,
            4.0944e-01, 1.9946e-01, 7.8763e-02, 2.6100e-02, 7.4365e-03,
            1.7184e-03, 3.2060e-04, 4.1469e-05, 2.4926e-06, 4.7401e-09,
            0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00] 
hazcurvevalues = zip(intmeaslvls,pgavals)
imtcode="PGA"
imtname="Peak Ground Acceleration"
imtdesc="Description of Peak Ground Acceleration"
imtvalmin = 0.0
imtvalmax = 10.0
imtunittype = "none"
imtremarks = "Remarks for Peak Ground Acceleration"

class IntensitymeasuretypeTestCase(unittest.TestCase):
    def setUp(self):
        print "This should output."
        self.pga = Intensitymeasuretype(imcode=intmeasuretype,
                         imname=imtname,imdesc= imtdesc,imvaluemin=imtvalmin,
                         imvaluemax=imtvalmax,imunittype=imtunittype,
                         imunitdescr="g for pga",imremarks=imtremarks)
        self.pga.save()
    def testCreate(self):
        imtresults = Intensitymeasuretype.objects.filter(imcode=intmeasuretype)
        for pgafromdb in imtresults:
            self.assertEquals(pgafromdb,self.pga)

class LogictreestrucTestCase(unittest.TestCase):
    def setUp(self):
        self.lts = Logictreestruc(ltsshortname=logtreestrname,
                             ltsname=logtreestrname,
                             ltsdesc=logtreestrname, 
                             ltsremarks=logtreestrname, 
                             ltsnumlevels = 2)
        self.lts.save()
    def testCreate(self):
        ltsresults = Logictreestruc.objects.filter(ltsshortname=logtreestrname)
        for ltsfromdb in ltsresults:
            self.assertEquals(ltsfromdb,self.lts)

class HazardsoftwareTestCase(unittest.TestCase):
    def setUp(self):
        self.hs = Hazardsoftware(hscode=hazsoftware, 
                            hsname=hazsoftware,
                            hsdesc=hazsoftware,
                            hsremarks=hazsoftware,
                            hsadddate = datenow)
        self.hs.save()
    def testCreate(self):
        hsresults = Hazardsoftware.objects.filter(hscode=hazsoftware)
        for hsfromdb in hsresults:
            self.assertEquals(hsfromdb,self.hs)

class CalculationownerTestCase(unittest.TestCase):
    def setUp(self):
        self.cg = Calculationgroup(cgcode=calcgrpcode,
                                   cgname=calcgrpcode,
                                   cgdesc=calcgrpcode,
                                   cgadddate=datenow,
                                   cgauthlevel="1",
                                   cgremarks=calcgrpcode)
        self.cg.save()
        self.co = Calculationowner(cocode=calcownercode, 
                             coname=calcownercode,
                             codesc=calcownercode,
                             coauthlevel = "1",
                             coremarks=calcownercode,
                             coadddate = datenow,
                             cgcode=self.cg)
        self.co.save()
    def testCreate(self):
        coresults = Calculationowner.objects.filter(cocode=calcownercode)
        for cofromdb in coresults:
            self.assertEquals(cofromdb, self.co)

class Hazardinputltreemodel(unittest.TestCase):
    def setUp(self):
        ltsresults = Logictreestruc.objects.filter(ltsshortname=logtreestrname)
        if (ltsresults):
            for ltsval in ltsresults:
                self.lts=ltsval
        else:
            self.lts = Logictreestruc(ltsshortname=logtreestrname,
                             ltsname=logtreestrname,
                             ltsdesc=logtreestrname, 
                             ltsremarks=logtreestrname, 
                             ltsnumlevels = 2)
        self.hilm = Hazardinputltreemodel(hilmshortname=hilmsname, 
                             hilmname=hilmsname, 
                             hilmdesc=hilmsname, 
                             hilmremarks=hilmsname, 
                             hilmcvrgtypecode = 1,
                             hilmareapolygon = hilmpolygonwkt,
                             ltsid = self.lts,
                             hilmpgareapolygon = Polygon(hilmpolygonwkt)) 
	self.hilm.save()

    def testCreate(self):
        hilmresults = Hazardinputltreemodel.objects.filter(
                             hilmshortname=hilmsname)
        for hilmfromdb in hilmresults:
            self.assertEquals(hilmfromdb, self.hilm)


#class HazardCurveToDbTestCase(unittest.TestCase):
#    def setUp(self):
        # construct a hazard curve object to be mapped to DB
        # with values coming from Europe results as above

    # loss curve tests
#    def setUp(self):
#        self.hazcurvecode = "Test_EuHazCrv"
#        self.hazcrvvalues = hazcurvevalues
#        
#    def test_empty_hazard_curve(self):
#        """Degenerate case."""
        
        #self.assertEqual(compute_loss_curve(
        #        shapes.EMPTY_CURVE, None),
        #        shapes.EMPTY_CURVE)
#        pass

#    def test_emptynonexistent_intensitymeasuretype(self):
#        pass

#    def test_emptynonexistent_logictreestruc(self):
#        pass

#    def test_emptynonexistent_hazardsoftware(self):
#        pass

#    def test_emptynonexistent_calcowner(self):
#        pass
   
#    def test_emptynonexistent_hazardcalc(self):
#        pass
    
#    def test_emptynonexistent_geopoint(self):
#        pass
  
#    def test_emptynonexistent_hazardcurve(self):
#        pass

#    def test_emptynonexistent_hazardcurvevalues(self):
#        pass
   
#    def test_invalidhazardcurvevals(self):
#        pass

#    def test_savedhazardcurvevals_sameaspassed(self):
#        pass


