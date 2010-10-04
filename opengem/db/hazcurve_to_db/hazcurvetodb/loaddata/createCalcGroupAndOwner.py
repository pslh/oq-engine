#!/usr/bin/env python

import datetime
from django.db import models
#from hazcurve_to_db.hazcurvetodb.models import Calculationgroup
#from hazcurve_to_db.hazcurvetodb.models import Calculationowner

#or from django.db import models

# To create database records
cg = Calculationgroup(cgcode="OPENGEMDEV", cgname="OPENGEMDEV", 
        cgdesc="Opengem Development Team", cgauthlevel="1", 
        cgadddate=datetime.datetime.now(),cgremarks="Opengem Development Team, ETH Zurich, Zurich, Switzerland and EU Center, Pavia, Italy")
cg.save()
cg = Calculationgroup(cgcode="SHAREDEV", cgname="SHAREDEV", 
        cgdesc="Share Development Team", cgauthlevel="1", cgadddate=datetime.datetime.now(), cgremarks="Share Development Team, \
        ETH Zurich, Zurich, Switzerland")
cg.save()

#If create same, with same primary key, it will be overwritten so first filter, then if non-existent create
# To delete
#cg = Calculationgroup.objects.filter(pk="")
#cg.delete()

# to show all objects
Calculationgroup.objects.all()
#Out[44]: [<Calculationgroup: OPENGEMDEV>, <Calculationgroup: SHAREDEV>]

# to get by a filter
cg = Calculationgroup.objects.get(pk="SHAREDEV")
cg = Calculationgroup.objects.get(cgname="OPENGEMDEV")

#Create related keys
cg.calculationowner_set.all()
# returns []

#Creates 3 calculation owner records related (auto create of relation to calculation group)
# first get calcuation group object
cg = Calculationgroup.objects.get(cgname="OPENGEMDEV")
# set relations to calc owner
cg.calculationowner_set.create(cocode="AM", coname="AUREA MOEMKE", 
        codesc="DB Architect, SED, ETH Zurich", coauthlevel="1", 
        coadddate=datetime.datetime.now(), coremarks="With Opengem dev team, top level")
cg.calculationowner_set.create(cocode="DM", coname="DAMIANO MONELLI", 
        codesc="Hazard/Risk Scientist, SED, ETH Zurich", coauthlevel="1", 
        coadddate=datetime.datetime.now(), coremarks="With Opengem dev team, top level")
cg.calculationowner_set.create(cocode="PK", coname="PHILIPP KAESTLI", 
        codesc="IT Coordinator, SED, ETH Zurich", coauthlevel="1", 
        coadddate=datetime.datetime.now(), coremarks="With Opengem dev team, top level")

cg = Calculationgroup.objects.get(cgname="SHAREDEV")
cg.calculationowner_set.create(cocode="AC", coname="ANDREA CERISARA", 
        codesc="Software Engineer, EU Center, Pavia, Italy", coauthlevel="1", 
        coadddate=datetime.datetime.now(), coremarks="With Opengem dev team, top level")
cg.calculationowner_set.create(cocode="VS", coname="VITOR SILVA", 
        codesc="Risk Scientist, EU Center, Pavia, Italy", coauthlevel="1", 
        coadddate=datetime.datetime.now(), coremarks="With Opengem dev team, top level")

#delete and add to opengemdev
co = Calculationowner.objects.get(pk="AC")
co.delete()
co = Calculationowner.objects.get(pk="VS")
print co
co.delete()

#NOW add to OPENGEMDEV
cg = Calculationgroup.objects.get(cgname="OPENGEMDEV")
cg.calculationowner_set.create(cocode="AC", coname="ANDREA CERISARA", 
        codesc="Software Engineer, EU Center, Pavia, Italy", coauthlevel="1", 
        coadddate=datetime.datetime.now(), coremarks="With Opengem dev team, top level")
cg.calculationowner_set.create(cocode="VS", coname="VITOR SILVA", 
        codesc="Risk Scientist, EU Center, Pavia, Italy", coauthlevel="1", 
        coadddate=datetime.datetime.now(), coremarks="With Opengem dev team, top level")
cg.calculationowner_set.create(cocode="JMK", coname="JOSHUA MCKENTY", 
        codesc="OPENGEM IT MANAGER, EU Center, Pavia, Italy", coauthlevel="1", 
        coadddate=datetime.datetime.now(), coremarks="With Opengem dev team, top level")
#Out[73]: < Calculationowner: JOSHUA MCKENTY > 
#OK, alles funktionert!
#Add to SHAREDEV
cg = Calculationgroup.objects.get(cgname="SHAREDEV")
cg.calculationowner_set.create(cocode="LD", coname="LAURENTIU DANCIU", 
        codesc="Hazard/Risk Scientist, SED, ETH Zurich", coauthlevel="1", 
        coadddate=datetime.datetime.now(), coremarks="With Share dev team, top level")
#Out[75]: <Calculationowner: LAURENTIU DANCIU>
cg.calculationowner_set.create(cocode="RK", coname="RAMAKRISHNAN KRISHNAMURTHY", 
        codesc="Software Architect, SED, ETH Zurich", coauthlevel="1", 
        coadddate=datetime.datetime.now(), coremarks="With Share dev team, top level")

