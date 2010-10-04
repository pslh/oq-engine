#!/usr/bin/env python

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from psycopg2 import IntegrityError

import datetime
from hazcurvetodb.models import Calculationgroup, Calculationowner

#or from django.db import models

# To create database records
cg = Calculationgroup(cgcode="GEMDEV2", cgname="OPENGEMDEV", 
        cgdesc="Opengem Development Team", cgauthlevel="1", 
        cgadddate=datetime.datetime.now(),cgremarks="Opengem Development Team, ETH Zurich, Zurich, Switzerland and EU Center, Pavia, Italy")
cg.save()
cg = Calculationgroup(cgcode="SHAREDEV2", cgname="SHAREDEV", 
        cgdesc="Share Development Team", cgauthlevel="1", cgadddate=datetime.datetime.now(), cgremarks="Share Development Team, \
        ETH Zurich, Zurich, Switzerland")
cg.save()

