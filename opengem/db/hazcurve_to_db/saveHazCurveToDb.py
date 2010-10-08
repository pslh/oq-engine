#!/usr/bin/env python2
# Load/OR Mapping from Hazardcurve object to database
# Author: Aurea Moemke
# Date: 8 October 2010
# 
# Description: 
# This program maps hazardcurve object to the opengem db using
# OR mapping.
#
# Usage: python saveHazCurveToDb.py
# 
# Steps to follow:
# If not yet existent, create intensity measure type record
# If not yet existent, create logic tree structure record
# If not yet existent, create hazard software record
# If not yet existent, create calculation owner record
# If not yet existent, Create hazardinputltreemodel record
#      If logictree endpath, create corresponding hilmpath record
# Create hazardcalculation with this related hazardinputltreemodel
#      and/or endpath 
# Hardcode values in hazard curve object and repository
#      for this hazardcalculation
# Save hazard curve object to database
#    1. check if a geopoint already exists, if not, create one
#    2. save hazard point values to model object
#    3. write to db


import sys
sys.path.append('/home/apm/Projects/opengem')
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from psycopg2 import IntegrityError
from django.contrib.gis.geos import *
#from shapely.geometry import Polygon, Point

from ordereddict import *
import datetime
from opengem.shapes import *
from hazcurvetodb.models import Logictreestruc, Hazardsoftware, \
     Calculationowner, Intensitymeasuretype, Hazardinputltreemodel, \
     Hazardcalculation, Hazardinputltreemodel, Hilmpath, Hazardcurve, \
     Hazardpointvalue, Geopoint
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


def create_access_gp(gppointwkt):
    gpresults = Geopoint.objects.filter(gppoint=gppointwkt)
    if (gpresults):
        print gppointwkt, "exists"
        for gp in gpresults:
            print gp.gpid
    else:
        gp = Geopoint(gppoint=gppointwkt,
                      gppgpoint=GEOSGeometry(gppointwkt))
        gp.save()
    return gp

def create_access_hcrv(hcrvsname, hc, gp, imt):
    hcrvresults = Hazardcurve.objects.filter(hcrvshortname=hcrvsname)
    if (hcrvresults):
        print hcrvsname, "exists"
        for hcrv in hcrvresults:
            print hcrv.hcrvname
    else:
        hcrv = Hazardcurve(hcrvshortname=hcrvsname, 
                             hcrvname=hcrvsname,
                             hcrvdesc=hcrvsname, 
                             hcrvtimestamp = datetime.datetime.now(),
                             hcrvremarks=hcrvsname,
                             hcid=hc,
                             gpid=gp,
                             imcode=imt)
        hcrv.save()
    return hcrv

def create_access_hpv(hpval, hpep, hpey, hc, gp, imt):
    hpvresults = Hazardpointvalue.objects.filter(gpid = gp.gpid,
                          hpexceedprob=hpep, hpexceedyears=hpey,
                          hcid = hc.hcid, imcode = imt.imcode )
    if (hpvresults):
        print hpval, "exists"
        for hpv in hpvresults:
            print hpv.hpid
    else:
        hpv = Hazardpointvalue(hpvalue=hpval, 
                      hpexceedprob = hpep,
                      hpexceedyears = hpey,
                      hcid = hc,
                      gpid = gp,
                      imcode = imt)
        hpv.save()
    return hpv
   
def main(argv):
    imname = "PGA"
    logtreename = "GSHAP_SEA_LTree"
    hazswcode = "OPENSHA"
    calcownercode = "DM"
    calcgrpcode = "OPENGEMDEV"
    hilmsname = "SGSHAPSEAModel"
    hilmlongname = "GSHAPSoutheastAsiaModel"
    hazcalcsname = "GSHAP_SEA_Calc"
    hazcurvename = "GSHAP_SEA_Crv1"
    # Polygon in WKT
    gshapeapolygon = "POLYGON ((50 5, 50 60, 150 60, 150 5, 50 5))"
    # hazardcurve from ~/workspace/gemHazardResults/europe
    # /results_Europe_2010_03-26-14:49:07
    # hazcrvpt is a point in WKT
    hazcrvpt = "POINT (-3.1000 72.6000)"   
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

    # Create/access Geopoint 
    gp= create_access_gp(hazcrvpt)
    print "in main, gp is", gp

    # Create/access Hazard Curve Model 
    hcrv= create_access_hcrv(hazcurvename, hc, gp, imt)
    print "in main, hcrv is", hcrv

    # Create hazardpointvalues for given hazardcurve calculation
    hazardcurve_data = []
    hazardcurve_data = zip(intmeaslvls, pgavals)
    #for iml, pga in hazardcurve_data:
    #      print iml, pga
    #Fastcurve returns an ordered dict of imlevels and pgavals
    values =FastCurve(hazardcurve_data)       
    print values
    
    hazcurve = HazardCurve(hazardcurve_data)
    print "id model", hazcurve.id_model
#   Ordered dict is returned, not iterable
#   
#   method 1 to iterate over dictionaries
#   for key in hazcurve.values.iterkeys():
#       print key, hazcurve.values[key]
#   method 2 to iterate over dictionaries
#   for key in hazcurve.values.keys():
#       print key, hazcurve.values[key]
#   method 3 to iterate over dictionaries
#   for key, value in hazcurve.values.items():
#       print key, value
    for key in hazcurve.values.iterkeys():
        print key, hazcurve.values[key]
        hpep = float(key)              # intensity measure level
        hpval = hazcurve.values[key]   # pga val
        hpey = 1
        hpv = create_access_hpv(hpval, hpep, hpey, hc, gp, imt) 
        print "in main, hpv is", hpv

if __name__ == "__main__":
    main(sys.argv[1:])
