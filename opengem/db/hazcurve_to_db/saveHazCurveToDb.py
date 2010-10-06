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

def main(argv):
    imname = "PGA"
    logtreename = "GSHAP_SEA_LTree"
    hazswcode = "OPENSHA"
    calcownercode = "DM"
    calcgrpcode = "OPENGEMDEV"
    hilmsname = "GSHAP_SEA_Model"
    hilmlongname = "GSHAP Southeast Asia Model"
    hazcalcsname = "GSHAP_SEA_Calc"
    gshapeapolygon = "POLYGON ((50 5, 50 60, 150 60, 150 5, 50 5))"
    
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



if __name__ == "__main__":
    main(sys.argv[1:])
