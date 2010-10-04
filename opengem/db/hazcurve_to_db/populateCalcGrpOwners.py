#!/usr/bin/env python

# This file shows how to use the OR mapping to directly create
# Calculationgroup records and related Calculationowner records
# For testing/illustration purposes only.
# author: Aurea Moemke
# date: 4 October 2010

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from psycopg2 import IntegrityError

import datetime
from hazcurvetodb.models import Calculationgroup, Calculationowner

# To create database records
cg = Calculationgroup(cgcode="OPENGEMDEV", cgname="OPENGEMDEV", 
        cgdesc="Opengem Development Team", cgauthlevel="1", 
        cgadddate=datetime.datetime.now(), cgremarks="Opengem Development Team,\        ETH Zurich, Zurich, Switzerland and EU Center, Pavia, Italy")
cg.save()
cg = Calculationgroup(cgcode="SHAREDEV", cgname="SHAREDEV", 
        cgdesc="Share Development Team", cgauthlevel="1", \
        cgadddate=datetime.datetime.now(), cgremarks="Share Development Team, \
        ETH Zurich, Zurich, Switzerland")
cg.save()

# If record with same primary key is written, it will overwrite an existing
# record with same primary key. Therefore, first filter, then if non-existent 
# create
# To delete
# cg = Calculationgroup.objects.filter(pk="")
# cg.delete()

# To show all objects
Calculationgroup.objects.all()
# Out[44]: [<Calculationgroup: OPENGEMDEV>, <Calculationgroup: SHAREDEV>]

# To get a record using a filter, either pk for primary key or field name itself
cg = Calculationgroup.objects.get(pk="SHAREDEV")
cg = Calculationgroup.objects.get(cgname="OPENGEMDEV")

# Create Calculation Owner records corresponding to Calculation Group
cg.calculationowner_set.all()
# returns []

# Creates 5 calculation owner records (foreign key field is automatically 
# created) 
# First get Calculation group object
cg = Calculationgroup.objects.get(cgname="OPENGEMDEV")

# Set relations to calc owner
cg.calculationowner_set.create(cocode="JMK", coname="JOSHUA MCKENTY",\
        codesc="OPENGEM IT MANAGER, EU Center, Pavia, Italy", coauthlevel="1",\
        coadddate=datetime.datetime.now(),\
        coremarks="With Opengem dev team, top level")

cg.calculationowner_set.create(cocode="AM", coname="AUREA MOEMKE",\
        codesc="DB Architect, SED, ETH Zurich", coauthlevel="1",\
        coadddate=datetime.datetime.now(), \
        coremarks="With Opengem dev team, top level")

cg.calculationowner_set.create(cocode="DM", coname="DAMIANO MONELLI", \
        codesc="Hazard/Risk Scientist, SED, ETH Zurich", coauthlevel="1",\ 
        coadddate=datetime.datetime.now(),\
        coremarks="With Opengem dev team, top level")

cg.calculationowner_set.create(cocode="PK", coname="PHILIPP KAESTLI", \
        codesc="IT Coordinator, SED, ETH Zurich", coauthlevel="1",\ 
        coadddate=datetime.datetime.now(),\
        coremarks="With Opengem dev team, top level")

# Test deletes
cg = Calculationgroup.objects.get(cgname="SHAREDEV")

cg.calculationowner_set.create(cocode="AC", coname="ANDREA CERISARA", \
        codesc="Software Engineer, EU Center, Pavia, Italy", coauthlevel="1", \
        coadddate=datetime.datetime.now(), \
        coremarks="With Opengem dev team, top level")

cg.calculationowner_set.create(cocode="VS", coname="VITOR SILVA",\ 
        codesc="Risk Scientist, EU Center, Pavia, Italy", coauthlevel="1",\
        coadddate=datetime.datetime.now(), \
        coremarks="With Opengem dev team, top level")

# Delete from SHAREDEV and add to OPENGEMDEV
co = Calculationowner.objects.get(pk="AC")
co.delete()
co = Calculationowner.objects.get(pk="VS")
co.delete()

# NOW add to OPENGEMDEV
cg = Calculationgroup.objects.get(cgname="OPENGEMDEV")

cg.calculationowner_set.create(cocode="AC", coname="ANDREA CERISARA",\
        codesc="Software Engineer, EU Center, Pavia, Italy", coauthlevel="1",\ 
        coadddate=datetime.datetime.now(),\
        coremarks="With Opengem dev team, top level")

cg.calculationowner_set.create(cocode="VS", coname="VITOR SILVA", \
        codesc="Risk Scientist, EU Center, Pavia, Italy", coauthlevel="1",\ 
        coadddate=datetime.datetime.now(),\
        coremarks="With Opengem dev team, top level")
 
# Now add Calculation Owners to SHAREDEV Calculation Group

cg = Calculationgroup.objects.get(cgname="SHAREDEV")

cg.calculationowner_set.create(cocode="LD", coname="LAURENTIU DANCIU", \
        codesc="Hazard/Risk Scientist, SED, ETH Zurich", coauthlevel="1",\ 
        coadddate=datetime.datetime.now(),\
        coremarks="With Share dev team, top level")
cg.calculationowner_set.create(cocode="RK",\
        coname="RAMAKRISHNAN KRISHNAMURTHY", \
        codesc="Software Architect, SED, ETH Zurich", coauthlevel="1",\
        coadddate=datetime.datetime.now(),\
        coremarks="With Share dev team, top level")

