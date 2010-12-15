# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

""" 
This code is intended to use SQLAlchemy to write hazard curves from the OpenQuake engine to a database. The SQLAlchemy Object Relational Mapper presents a method of associating user-defined Python classes with database tables, and instances of those classes (objects) with rows in their corresponding tables."""

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper, relationship
from sqlalchemy import Integer, String
from openquake import shapes
from sqlalchemy.ext.declarative import declarative_base


#SQLAlchemy SQL construction method

""" 
The hazard curve is split into thee classes: HazardResult,
HazardCurveList and HazardCurve in order avoid duplicate saved information
to the DB"""
Base = declarative_base()

class HazardResult(Base):
    __tablename__ = "hazard_result"

    # table metadata
    id = Column(Integer, primary_key=True)
    model_id = Column(String)
    sa_period = Column(Integer)
    sa_damping = Column(Integer)
    time_span_duration = Column(Integer)

    # one to many relationship with HazardCurveList
    children = relationship("HazardCurveList", backref="hazard_result")

    def __init__(self, model_id, time_span_duration, sa_period, sa_damping):
        self.model_id = model_id
        self.sa_period = sa_period
        self.sa_damping = sa_damping
        self.time_span_duration = time_span_duration

    def __eq__(self, other):
        return self.model_id == other.model_id and self.sa_period == other.sa_period and self.sa_damping == other.sa_damping and self.time_span_duration == other.time_span_duration


class HazardCurveList(Base):
    __tablename__ = "hazard_curve_list"

    # table metadata
    id = Column(Integer, primary_key=True)
    result_id = Column(Integer, ForeignKey('hazard_result.id'))
    end_branch_label = Column(String)
    abscissae = Column(String)
    imt = Column(String)
    
    # one to many relationship with HazardCurve
    #children = relationship("HazardCurve", backref="hazard_curve_list")
    
    def __init__(self, end_branch_label, abscissae, imt):
        self.end_branch_label = end_branch_label
        self.abscissae = abscissae
        self.imt = imt
    
    def __eq__(self, other):
        return self.end_branch_label == other.end_branch_label and self.abscissae == other.abscissae and imt == other.imt

class HazardCurve(object):
    __tablename__ = "hazard_curve"
    
    # table metadata
    id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey('hazard_curve_list.id'))
    lat = Column(Integer),
    long =Column(Integer)
    
    def __init__(self, list_id):
        self.list_id = list_id
        