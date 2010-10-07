#!/usr/bin/env python2
# This file shows how to map the hazcurve object to the DB
# Needed files: 
# HazardInputLtreeModel
# HazardCalculation
# Hilmpath
# Hazardcurve
# For testing/illustration purposes only.
# author: Aurea Moemke
# date: 4 October 2010
"""Load/OR Mapping from Hazardcurve object to database

@author: Aurea Moemke

This program maps hazardcurve object to the opengem db using
OR mapping.

Usage: python saveHazCurveToDb.py [options] [source]

Options:
  -l ..., --logictreestruc=...     specify logic tree structure id
  -s ..., --hazsoftware=...         specify hazard software to use
  -c ..., --calcowner=...       specify calculation owner
  -i ..., --intmeastype=...     specify intensity measure type
  -h ..., --hazinputltreemodel=... specify hazard input ltree model
  -a ..., --hazardcalc=...    specify hazard calculation name
  -z ..., --hazardcurve=...   specify hazard curve name
  
  -h, --help                  show this help

Example:
  saveHazCurveToDb.py -l 'GSHAPSEA_LTREE' -s 'OPENSHA' ...  

"""
__author__ = "Aurea Moemke (aurea.moemke@yahoo.com, aurea.moemke@sed.ethz.ch)"
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2010/10/05 $"
__copyright__ = "Copyright (c) 2010 Aurea Moemke"
__license__ = "Python"

import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from psycopg2 import IntegrityError
from django.contrib.gis.geos import *
#from shapely.geometry import Polygon, Point

import ordereddict
import datetime
from hazcurvetodb.models import Logictreestruc, Hazardsoftware, \
     Calculationowner, Intensitymeasuretype, Hazardinputltreemodel, \
     Hazardcalculation, Hazardinputltreemodel, Hilmpath, Hazardcurve, \
     Hazardpointvalue, Geopoint
# if not yet existent, create logic tree structure record
# if not yet existent, create hazard software record
# if not yet existent, create calculation owner record
# if not yet existent, create intensity measure type record
# if not yet existent, Create hazardinputltreemodel record
#za      If logictree endpath, create corresponding hilmpath record
# Create hazardcalculation with this related hazardinputltreemodel
#      and/or endpath 
# Hardcode values in hazard curve object and repository
#      for this hazardcalculation
# Save hazard curve object to database
#    1. check if a geopoint already exists, if not, create one
#    2. save hazard point values to model object
#    3. write to db

def usage():
    print __doc__

def create_access_imt(imtname):
    # Create intensity measure type if not yet existing   
    imtresults = Intensitymeasuretype.objects.filter(pk=imtname)
    # imtresults = Intensitymeasuretype.objects.all() //prints all
    if (imtresults):
        print imtname, "exists"
        for imt in imtresults:
            print imt.imname, "max value:", imt.imvaluemax
    else:
        imt = Intensitymeasuretype(imcode=imtname, imname=imtname,
                                   imdesc = imtname, imvaluemin=0.0,
                                   imvaluemax=12.0, imunittype="none",
                                   imunitdescr="none", imremarks=imtname)
        imt.save()
    return imt 

def create_access_lts(logtreename):
    ltsresults = Logictreestruc.objects.filter(ltsshortname=logtreename)
    if (ltsresults):
        print logtreename, "exists"
        for lts in ltsresults:
            print lts.ltsname
    else:
        lts = Logictreestruc(ltsshortname=logtreename, ltsname=logtreename,
                             ltsdesc=logtreename, ltsremarks=logtreename, 
                             ltsnumlevels = 2)
        lts.save()
    return lts

def create_access_hs(hazswcode):
    hsresults = Hazardsoftware.objects.filter(hscode=hazswcode)
    if (hsresults):
        print hazswcode, "exists"
        for hs in hsresults:
            print hs.hsname
    else:
        hs = Hazardsoftware(hscode=hazswcode, hsname=hazswcode,
                             hsdesc=hazswcode, hsremarks=hazswcode, 
                             hsadddate = datetime.datetime.now())
	hs.save()
    return hs

def create_access_co(calcownercode):
    coresults = Calculationowner.objects.filter(cocode=calcownercode)
    if (coresults):
        print calcownercode, "exists"
        for co in coresults:
            print co.coname
    else:
        co = Calculationowner(cocode=calcownercode, coname=calcownercode,
                             codesc=calcownercode, coauthlevel = "1",
                             coremarks=calcownercode,
                             coadddate = datetime.datetime.now(),
                             cgcode=calcgrpcode)
	co.save()
    return co

def create_access_hilm_shapely(hilmsname,hilmpolygonwkt, lts):
    hilmresults = Hazardinputltreemodel.objects.filter(hilmshortname=hilmsname)
    if (hilmresults):
        print hilmsname, "exists"
        for hilm in hilmresults:
            print hilm.hilmname
    else:
        hilm = Hazardinputltreemodel(hilmshortname=hilmsname, 
                             hilmname=hilmsname, hilmdesc=hilmsname, 
                             hilmremarks=hilmsname, 
                             hilmcvrgtypecode = 1,
                             hilmareapolygon = hilmpolygonwkt,
                             ltsid = lts,
                             hilmpgareapolygon = Polygon(hilmpolygonwkt)) 
	hilm.save()
    return hilm

def create_access_hilm(hilmsname,hilmpolygonwkt, lts):
    hilmresults = Hazardinputltreemodel.objects.filter(hilmshortname=hilmsname)
    if (hilmresults):
        print hilmsname, "exists"
        for hilm in hilmresults:
            print hilm.hilmname
    else:
        hilm = Hazardinputltreemodel(hilmshortname=hilmsname, 
                             hilmname=hilmsname, hilmdesc=hilmsname, 
                             hilmremarks=hilmsname, 
                             hilmcvrgtypecode = 1,
                             hilmareapolygon = hilmpolygonwkt,
                             ltsid = lts,
                             hilmpgareapolygon = GEOSGeometry(hilmpolygonwkt)) 
	hilm.save()
    return hilm

def create_access_hc(hcsname, hcpolygonwkt, hilm, hs, co):
    hcresults = Hazardcalculation.objects.filter(hcshortname=hcsname)
    if (hcresults):
        print hcsname, "exists"
        for hc in hcresults:
            print hc.hcname
    else:
        hc = Hazardcalculation(hcshortname=hcsname, hcname=hcsname,
                             hcdesc=hcsname, 
                             hcstarttimestamp = datetime.datetime.now(),
                             hcprobdettag = "P",
                             hcgemgentag = True,
                             hcareapolygon=hcpolygonwkt,
                             hcremarks=hcsname,
                             hilmid=hilm,
                             hscode=hs,
                             cocode=co,
                             hcpgareapolygon=GEOSGeometry(hcpolygonwkt))
        hc.save()
    return hc


def create_access_gp(gppointwkt, hilm, hs, co):
    gpresults = Geopoint.objects.filter(gppoint=gppointwkt)
    if (gpresults):
        print gppointwkt, "exists"
        for gp in gpresults:
            print gp.gpid
    else:
        gp = Geopoint(gppoint=gppointwkt,
                      gppgpoint=GEOSGeometry(gppgpoint))
        gp.save()
    return gp

def create_access_hcrv(hcrvsname, hc, gp, imt):
    hcrvresults = Hazardcurve.objects.filter(hcrvshortname=hcrvsname)
    if (hcresults):
        print hcrvsname, "exists"
        for hcrv in hcrvresults:
            print hcrv.hcrvsname
    else:
        hcrv = Hazardcalculation(hcrvshortname=hcrvsname, hcrvname=hcrvsname,
                             hcrvdesc=hcrvsname, 
                             hcrvstarttimestamp = datetime.datetime.now(),
                             hcrvremarks=hcrvsname,
                             hcid=hc,
                             gpid=gp,
                             imcode=imt)
        hcrv.save()
    return hcrv

def create_access_hpv(hpval, hpep, hpey, hc, gp, imt):
    hpvresults = Hazardpointvalue.objects.filter(gpid = gp.gpid)
    if (hpvresults):
        print hpv.hpid, "exists"
        for hpv in hpvresults:
            print hpv.hpid
    else:
        hpv = Hazardpointvalue(gpid = gp, 
                      hpvalue=hpval, 
                      hpexceedprob = hpexcprob,
                      hpexceedyears = hpey,
                      hcid = hc,
                      imcode = imt)
        hpv.save()
    return hpv

#curvetodict
def curvestodict(imlevels,pgavalues):
    hcdict = {}
    i = 0
    while i < len(imlevels):
        hcdict[imlevels[i]] = pgavalues[i]
        i += 1
    return hcdict
        
def main(argv):
    imname = "PGA"
    logtreename = "GSHAP_SEA_LTree"
    hazswcode = "OPENSHA"
    calcownercode = "DM"
    calcgrpcode = "OPENGEMDEV"
    hilmsname = "SGSHAPSEAModel"
    hilmlongname = "GSHAPSoutheastAsiaModel"
    hazcalcsname = "GSHAP_SEA_Calc"
    gshapeapolygon = "POLYGON ((50 5, 50 60, 150 60, 150 5, 50 5))"
    #SHAPELY no need to close polygon
    #shapelypolygon = "[(50, 5), (50 60), (150 60), (150 5)]"
    
    # hazardcurve from ~/workspace/gemHazardResults/europe
    # /results_Europe_2010_03-26-14:49:07
    # hazcrvpt is a point
    #hazcrvpt = -3.1000 +72.6000   
    #intmeaslvl is a list of 19 values
    intmeaslvls = [5.0000e-03, 7.0000e-03, 9.8000e-03, 1.3700e-02, 1.9200e-02,
                   2.6900e-02, 3.7600e-02, 5.2700e-02, 7.3800e-02, 1.0300e-01,
                   1.4500e-01, 2.0300e-01, 2.8400e-01, 3.9700e-01, 5.5600e-01,
                   7.7800e-01, 1.0900e+00, 1.5200e+00, 2.1300e+00]
   #pgaval corr to intmeaslvl
    pgavals = [9.9967e-01, 9.9618e-01, 9.7180e-01, 8.7730e-01, 6.7090e-01,
            4.0944e-01, 1.9946e-01, 7.8763e-02, 2.6100e-02, 7.4365e-03,
            1.7184e-03, 3.2060e-04, 4.1469e-05, 2.4926e-06, 4.7401e-09,
            0.0000e+00, 0.0000e+00, 0.0000e+00, 0.0000e+00] 
  
    # Create intensity measure type if not yet existing   
    imt = create_access_imt(imname)
    print "in main, imt is", imt
 
    # Create Logic Tree Structure record
    lts = create_access_lts(logtreename)

    print "in main, lts is", lts

    # Create/access Hazard Software record
    hs = create_access_hs(hazswcode)
    print "in main, hs is", hs

    # Create/access Calculation Owner 
    co = create_access_co(calcownercode)
    print "in main, co is", co

   # Create/access Hazard Input Logic Tree Model Record
    hilm = create_access_hilm(hilmsname, gshapeapolygon, lts)
    print "in main, hilm is", hilm

   # Create/access Hazard Calc Model 
    hc = create_access_hc(hazcalcsname, gshapeapolygon, hilm, hs, co)
    print "in main, hc is", hc

   # Create/access Hazard Curve Model 
    #hc = create_access_hcrv(hazcurvename, gshapeapolygon, hilm, hs, co)
    #print "in main, hcrv is", hcrv
    hcdict = curvestodict(intmeaslvls,pgavals)
    print hcdict

    odict = ordereddict.OrderedDict(sorted(hcdict.items(),key=lambda t:t[0]))
    print "Ordered dictionary of imlevel, pgavalue"
    print odict

if __name__ == "__main__":
    main(sys.argv[1:])
