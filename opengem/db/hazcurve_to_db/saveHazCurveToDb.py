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
#      If logictree endpath, create corresponding hilmpath record
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

def main(argv):
    logtreename = "GSHAP_SEA_LTree"
    hazswstr = "OPENSHA"
    calcownerStr = "DM"
    ltmodelname = "GSHAP_SEA_Model"
    ltmodellongname = "GSHAP Southeast Asia Model"
    imtname = "PGA"
    hazcalcname = "GSHAP_SEA_Calc"
    hazcalcpolygon = "POLYGON((40 0,160 0,160 60, 40 60,40 0))"
 
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
        
    # Create Logic Tree Structure record
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
     
if __name__ == "__main__":
    main(sys.argv[1:])
