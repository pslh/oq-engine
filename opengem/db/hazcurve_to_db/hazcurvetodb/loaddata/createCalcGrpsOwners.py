#!/usr/bin/env python

import datetime
from django.db import models
#from hazcurve_to_db.hazcurvetodb.models import Calculationgroup
#from hazcurve_to_db.hazcurvetodb.models import Calculationowner

#or from django.db import models

# To create database records
cg = Calculationgroup(cgcode="OPENGEMDEV2", cgname="OPENGEMDEV", 
        cgdesc="Opengem Development Team", cgauthlevel="1", 
        cgadddate=datetime.datetime.now(),cgremarks="Opengem Development Team, ETH Zurich, Zurich, Switzerland and EU Center, Pavia, Italy")
cg.save()
cg = Calculationgroup(cgcode="SHAREDEV2", cgname="SHAREDEV", 
        cgdesc="Share Development Team", cgauthlevel="1", cgadddate=datetime.datetime.now(), cgremarks="Share Development Team, \
        ETH Zurich, Zurich, Switzerland")
cg.save()

