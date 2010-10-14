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
imtname="Peak Ground Acceleration"
imtdesc="Description of Peak Ground Acceleration"
imtvalmin = 0.0
imtvalmax = 10.0
imtunittype = "none"
imtremarks = "Remarks for Peak Ground Acceleration"

hazsoftware =  "OPENSHA"
logtreestrname = "EULOGTREE"
calcownercode = "DM"  
calcgrpcode = "OPENGEMDEV"
datenow = datetime.datetime.now()
hilmsname = "Europe_LTree_V1"
#counterclockwise
polygonwkt = "POLYGON ((50 5, 150 5, 150 60, 50 60, 50 5))"
#clockwise hilmpolygonwkt = "POLYGON ((50 5, 50 60, 150 60, 150 5, 50 5))"
hazcalcname = "Europe_Calc"
#geopoint_WKT = "POINT (-3.1 +72.6)"
hazcrvname = "Test_EuHazcrv"
#INVALID_POINT_WKT = "POINT (181 91)"
pointwkt = "POINT (-3.1000 72.6000)"   
hpep = 5.0000e-03
hpval = 9.9967e-01  
hpey = 1 # annual prob of exceedance or 1 year
class IntensitymeasuretypeTestCase(unittest.TestCase):
    def setUp(self):
        self.imt = Intensitymeasuretype(imcode=intmeasuretype,
                         imname=imtname,imdesc= imtdesc,imvaluemin=imtvalmin,
                         imvaluemax=imtvalmax,imunittype=imtunittype,
                         imunitdescr="g for pga",imremarks=imtremarks)
       
    def testCreate(self):
#        self.imt.save()
        imtresults = Intensitymeasuretype.objects.filter(imcode=intmeasuretype)
        for imtfromdb in imtresults:
            self.assertEquals(imtfromdb,self.imt)

class HazardsoftwareTestCase(unittest.TestCase):
    def setUp(self):
        self.hs = Hazardsoftware(hscode=hazsoftware,
                            hsname=hazsoftware,
                            hsdesc=hazsoftware,
                            hsremarks=hazsoftware,
                            hsadddate = datenow)
    def testCreate(self):
        #self.hs.save()
        hsresults = Hazardsoftware.objects.filter(hscode=hazsoftware)
        for hsfromdb in hsresults:
            self.assertEquals(hsfromdb,self.hs)

class LogictreestrucTestCase(unittest.TestCase):
    def setUp(self):
        self.lts = Logictreestruc(ltsshortname=logtreestrname,
                             ltsname=logtreestrname,
                             ltsdesc=logtreestrname,
                             ltsremarks=logtreestrname,
                             ltsnumlevels = 2)
       
    def testCreate(self):
        #self.lts.save()
        ltsresults = Logictreestruc.objects.filter(ltsshortname=logtreestrname)
        for ltsfromdb in ltsresults:
            self.assertEquals(ltsfromdb,self.lts)

class CalculationownerTestCase(unittest.TestCase):
    def setUp(self):
        cgresults=Calculationgroup.objects.filter(cgcode=calcgrpcode)
        if (cgresults):
            for cg in cgresults:
                self.cg=cg
        else:
            self.cg = Calculationgroup(cgcode=calcgrpcode,
                                   cgname=calcgrpcode,
                                   cgdesc=calcgrpcode,
                                   cgadddate=datenow,
                                   cgauthlevel="1",
                                   cgremarks=calcgrpcode)
           # self.cg.save()
        self.co = Calculationowner(cocode=calcownercode,
                             coname=calcownercode,
                             codesc=calcownercode,
                             coauthlevel = "1",
                             coremarks=calcownercode,
                             coadddate = datenow,
                             cgcode=self.cg)
       # self.co.save()
    def testCreate(self):
        coresults = Calculationowner.objects.filter(cocode=calcownercode)
        for cofromdb in coresults:
            self.assertEquals(cofromdb, self.co)

class HazardinputltreemodelTestCase(unittest.TestCase):
    def setUp(self):
        ltsresults = Logictreestruc.objects.filter(ltsshortname=logtreestrname)
        if (ltsresults):
            for lts in ltsresults:
                self.lts=lts
        else:
            self.lts = Logictreestruc(ltsshortname=logtreestrname,
                             ltsname=logtreestrname,
                             ltsdesc=logtreestrname,
                             ltsremarks=logtreestrname,
                             ltsnumlevels = 2)
           # self.lts.save()
    def testCreate(self):
        self.hilm = Hazardinputltreemodel(hilmshortname=hilmsname,
                             hilmname=hilmsname,
                             hilmdesc=hilmsname,
                             hilmremarks=hilmsname,
                             hilmcvrgtypecode = 1,
                             hilmareapolygon = polygonwkt,
                             ltsid = self.lts,
                             hilmpgareapolygon = GEOSGeometry(polygonwkt))
        #self.hilm.save()
        hilmresults = Hazardinputltreemodel.objects.filter(
                             hilmshortname=hilmsname)
        for hilmfromdb in hilmresults:
            self.assertEquals(hilmfromdb, self.hilm)

class HazardcalculationTestCase(unittest.TestCase):
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

        hilmresults = Hazardinputltreemodel.objects.filter(
                             hilmshortname=hilmsname)
        if (hilmresults):
            for hilm in hilmresults:
                 self.hilm=hilm
        else:
            self.hilm = Hazardinputltreemodel(hilmshortname=hilmsname,
                             hilmname=hilmsname,
                             hilmdesc=hilmsname,
                             hilmremarks=hilmsname,
                             hilmcvrgtypecode = 1,
                             hilmareapolygon = polygonwkt,
                             ltsid = self.lts,
                             hilmpgareapolygon = GEOSGeometry(polygonwkt))
        hsresults = Hazardsoftware.objects.filter(hscode=hazsoftware)
        if (hsresults):
            for hs in hsresults:
                self.hs=hs
        else:
            self.hs = Hazardsoftware(hscode=hazsoftware,
                            hsname=hazsoftware,
                            hsdesc=hazsoftware,
                            hsremarks=hazsoftware,
                            hsadddate = datenow)
        cgresults=Calculationgroup.objects.filter(cgcode=calcgrpcode)
        if (cgresults):
            for cg in cgresults:
                self.cg=cg
        else:
            self.cg = Calculationgroup(cgcode=calcgrpcode,
                                   cgname=calcgrpcode,
                                   cgdesc=calcgrpcode,
                                   cgadddate=datenow,
                                   cgauthlevel="1",
                                   cgremarks=calcgrpcode)
        coresults = Calculationowner.objects.filter(cocode=calcownercode)
        if (coresults):
            for coval in coresults:
                self.co=coval
        else:
            self.co = Calculationowner(cocode=calcownercode,
                             coname=calcownercode,
                             codesc=calcownercode,
                             coauthlevel = "1",
                             coremarks=calcownercode,
                             coadddate = datenow,
                             cgcode=self.cg)
        self.hc = Hazardcalculation(hcshortname=hazcalcname,
                             hcname=hazcalcname,
                             hcdesc=hazcalcname,
                             hcstarttimestamp = datenow,
                             hcprobdettag = "P",
                             hcgemgentag = True,
                             hcareapolygon=polygonwkt,
                             hcremarks=hazcalcname,
                             hilmid=self.hilm,
                             hscode=self.hs,
                             cocode=self.co,
                             hcpgareapolygon=GEOSGeometry(polygonwkt))
    def testCreate(self):
        hcresults = Hazardcalculation.objects.filter(hcname=hazcalcname)
        for hcfromdb in hcresults:
            self.assertEquals(hcfromdb, self.hc)

class GeopointTestCase(unittest.TestCase):
    def setUp(self):
       self.gp = Geopoint(gppoint=pointwkt,
                      gppgpoint=GEOSGeometry(pointwkt))

    def testCreate(self):
        gpresults = Geopoint.objects.filter(gppoint=pointwkt)
        for gpfromdb in gpresults:
            self.assertEquals(gpfromdb, self.gp)

class HazardcurveTestCase(unittest.TestCase):
    def setUp(self):
        gpresults = Geopoint.objects.filter(gppoint=pointwkt)
        if (gpresults):
            for gp in gpresults:
                self.gp=gp
        else:
            self.gp = Geopoint(gppoint=pointwkt,
                      gppgpoint=GEOSGeometry(pointwkt))
        
        imtresults = Intensitymeasuretype.objects.filter(imcode=intmeasuretype)
        if (imtresults):
            for imt in imtresults:
                self.imt=imt
        else:
            self.imt = Intensitymeasuretype(imcode=intmeasuretype,
                         imname=imtname,imdesc= imtdesc,imvaluemin=imtvalmin,
                         imvaluemax=imtvalmax,imunittype=imtunittype,
                         imunitdescr="g for pga",imremarks=imtremarks)
        
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

        hilmresults = Hazardinputltreemodel.objects.filter(
                             hilmshortname=hilmsname)
        if (hilmresults):
            for hilm in hilmresults:
                 self.hilm=hilm
        else:
            self.hilm = Hazardinputltreemodel(hilmshortname=hilmsname,
                             hilmname=hilmsname,
                             hilmdesc=hilmsname,
                             hilmremarks=hilmsname,
                             hilmcvrgtypecode = 1,
                             hilmareapolygon = polygonwkt,
                             ltsid = self.lts,
                             hilmpgareapolygon =GEOSGeometry(polygonwkt))
        
        hsresults = Hazardsoftware.objects.filter(hscode=hazsoftware)
        if (hsresults):
            for hs in hsresults:
                self.hs=hs
        else:
            self.hs = Hazardsoftware(hscode=hazsoftware,
                            hsname=hazsoftware,
                            hsdesc=hazsoftware,
                            hsremarks=hazsoftware,
                            hsadddate = datenow)
        
        cgresults=Calculationgroup.objects.filter(cgcode=calcgrpcode)
        if (cgresults):
            for cg in cgresults:
                self.cg=cg
        else:
            self.cg = Calculationgroup(cgcode=calcgrpcode,
                                   cgname=calcgrpcode,
                                   cgdesc=calcgrpcode,
                                   cgadddate=datenow,
                                   cgauthlevel="1",
                                   cgremarks=calcgrpcode)
        
        coresults = Calculationowner.objects.filter(cocode=calcownercode)
        if (coresults):
            for coval in coresults:
                self.co=coval
        else:
            self.co = Calculationowner(cocode=calcownercode,
                             coname=calcownercode,
                             codesc=calcownercode,
                             coauthlevel = "1",
                             coremarks=calcownercode,
                             coadddate = datenow,
                             cgcode=self.cg)
        
        hcresults = Hazardcalculation.objects.filter(hcname=hazcalcname)
        if (hcresults):
            for hc in hcresults:
                self.hc=h
        else:
            self.hc = Hazardcalculation(hcshortname=hazcalcname,
                             hcname=hazcalcname,
                             hcdesc=hazcalcname,
                             hcstarttimestamp = datenow,
                             hcprobdettag = "P",
                             hcgemgentag = True,
                             hcareapolygon=polygonwkt,
                             hcremarks=hazcalcname,
                             hilmid=self.hilm,
                             hscode=self.hs,
                             cocode=self.co,
                             hcpgareapolygon=GEOSGeometry(polygonwkt))

        self.hcrv = Hazardcurve(hcrvshortname=hazcrvname,
                             hcrvname=hazcrvname,
                             hcrvdesc=hazcrvname,
                             hcrvtimestamp = datenow,
                             hcrvremarks=hazcrvname,
                             hcid=self.hc,
                             gpid=self.gp,
                             imcode=self.imt)

    def testCreate(self):
        hcrvresults = Hazardcurve.objects.filter(hcrvshortname=hazcrvname)
        for hcrvfromdb in hcrvresults:
            self.assertEquals(hcrvfromdb, self.hcrv)

class HazardpointvalueTestCase(unittest.TestCase):
    def setUp(self):
        gpresults = Geopoint.objects.filter(gppoint=pointwkt)
        if (gpresults):
            for gp in gpresults:
                self.gp=gp
        else:
            self.gp = Geopoint(gppoint=pointwkt,
                      gppgpoint=GEOSGeometry(pointwkt))
        
        imtresults = Intensitymeasuretype.objects.filter(imcode=intmeasuretype)
        if (imtresults):
            for imt in imtresults:
                self.imt=imt
        else:
            self.imt = Intensitymeasuretype(imcode=intmeasuretype,
                         imname=imtname,imdesc= imtdesc,imvaluemin=imtvalmin,
                         imvaluemax=imtvalmax,imunittype=imtunittype,
                         imunitdescr="g for pga",imremarks=imtremarks)
        
        ltsresults = Logictreestruc.objects.filter(ltsshortname=logtreestrname)
        if (ltsresults):
            for ltsval in ltsresults:
                self.lts=ltsval
        else:
            self.lts = Logictreestruc(ltsshortname=logtreestrname,
                             ltsname=logtreestrname,
                             ltsdesc=logtreestrname,
                             ltsremarks=logtreestrname,
                             ltsnumlevels=2)
        
        hilmresults = Hazardinputltreemodel.objects.filter(
                             hilmshortname=hilmsname)
        if (hilmresults):
            for hilm in hilmresults:
                 self.hilm=hilm
        else:
            self.hilm = Hazardinputltreemodel(hilmshortname=hilmsname,
                             hilmname=hilmsname,
                             hilmdesc=hilmsname,
                             hilmremarks=hilmsname,
                             hilmcvrgtypecode=1,
                             hilmareapolygon=polygonwkt,
                             ltsid=self.lts,
                             hilmpgareapolygon=GEOSGeometry(polygonwkt))
        
        hsresults = Hazardsoftware.objects.filter(hscode=hazsoftware)
        if (hsresults):
            for hs in hsresults:
                self.hs=hs
        else:
            self.hs = Hazardsoftware(hscode=hazsoftware,
                            hsname=hazsoftware,
                            hsdesc=hazsoftware,
                            hsremarks=hazsoftware,
                            hsadddate=datenow)
        
        cgresults=Calculationgroup.objects.filter(cgcode=calcgrpcode)
        if (cgresults):
            for cg in cgresults:
                self.cg=cg
        else:
            self.cg = Calculationgroup(cgcode=calcgrpcode,
                                   cgname=calcgrpcode,
                                   cgdesc=calcgrpcode,
                                   cgadddate=datenow,
                                   cgauthlevel="1",
                                   cgremarks=calcgrpcode)
        
        coresults = Calculationowner.objects.filter(cocode=calcownercode)
        if (coresults):
            for coval in coresults:
                self.co=coval
        else:
            self.co = Calculationowner(cocode=calcownercode,
                             coname=calcownercode,
                             codesc=calcownercode,
                             coauthlevel="1",
                             coremarks=calcownercode,
                             coadddate=datenow,
                             cgcode=self.cg)
        
        hcresults = Hazardcalculation.objects.filter(hcname=hazcalcname)
        if (hcresults):
            for hc in hcresults:
                self.hc=h
        else:
            self.hc = Hazardcalculation(hcshortname=hazcalcname,
                             hcname=hazcalcname,
                             hcdesc=hazcalcname,
                             hcstarttimestamp = datenow,
                             hcprobdettag="P",
                             hcgemgentag=True,
                             hcareapolygon=polygonwkt,
                             hcremarks=hazcalcname,
                             hilmid=self.hilm,
                             hscode=self.hs,
                             cocode=self.co,
                             hcpgareapolygon=GEOSGeometry(polygonwkt))
        
        self.hpv = Hazardpointvalue(hpvalue=hpval,
                             hpexceedprob=hpep,
                             hpexceedyears=hpey,
                             hcid=self.hc,
                             gpid=self.gp,
                             imcode=self.imt)

    def testCreate(self):
        hpvresults = Hazardpointvalue.objects.filter(gpid=self.gp.gpid,
                          hpexceedprob=hpep, hpexceedyears=hpey,
                          hcid=self.hc.hcid, imcode=self.imt.imcode )
        for hpvfromdb in hpvresults:
            self.assertEquals(hpvfromdb, self.hpv)


