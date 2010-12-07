# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
""" 
This code is intended to use SQLAlchemy to write hazard curves from the OpenQuake engine to a database. The SQLAlchemy Object Relational Mapper presents a method of associating user-defined Python classes with database tables, and instances of those classes (objects) with rows in their corresponding tables."""


class HazardCurveGenerator(object):

    def __init__(self, model_id, endBranchLabel, values, imt, timeSpanDuration
                    imlValues):
        self.model_id = Model_ID
        self.endBranchLabel = End_Branch_Label
        self.values = Values
        self.imt = IMT
        self.timeSpanDuration = Time_Span_Duration
        
    def __repr__(self):
        return "<User('%s','%s', '%s', '%s', '%s')>" % (self.model_id, self.endBranchLabel,
        self.values, self.imt, self.timeSpanDuration)
        