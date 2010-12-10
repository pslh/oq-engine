# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4


""" 
This code is intended to use SQLAlchemy to write hazard curves from the OpenQuake engine to a database. The SQLAlchemy Object Relational Mapper presents a method of associating user-defined Python classes with database tables, and instances of those classes (objects) with rows in their corresponding tables."""


from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper
from sqlalchemy import Integer, String
from openquake import shapes

#TODO BW create a 'real' connection to a DB for mapping hazard curves.
#TODO Change echo to False when you’re ready to put the code into production.
engine = create_engine('sqlite:///test.db', echo=True)
"""sqlEngine/connection object, temporary connection to in-memory-only
       SQLite database"""

#Table definition
metadata = MetaData(bind=engine)
#Table generation
hazard_curve_table = Table('hazard_curve', metadata,
                        Column('model_id', String, primary_key=True),
                        Column('end_branch_label', String),
                        Column('_values', String),
                        Column('imt', String(40)),
                        Column('time_span_duration', String),
                        Column('iml_values', String),
                    )
metadata.create_all()

#SQLAlchemy SQL construction method

class HazardCurveGenerator(object):
    
    def __init__(self, model_id, end_branch_label, values, imt,
        time_span_duration, iml_values):
        self.model_id = model_id
        self.end_branch_label = end_branch_label
        self.values = values
        self.imt = imt
        self.time_span_duration = time_span_duration
        self.iml_values = iml_values
        
    def __repr__(self):
        return "<User('%s','%s', '%s', '%s', '%s')>" % (self.model_id,
            self.endBranchLabel, self.values, self.imt, self.timeSpanDuration)
        
hcg = HazardCurveGenerator('1', 'test_endBranchLabel', 'test_valuse',
    'test_IMT', 'test_timeSpan', 'test_IMLValues')
    
print hcg.model_id

print hcg.end_branch_label

print hcg.values
print hcg.imt
print hcg.time_span_duration
print hcg.iml_values


# create an Insert object        
ins = hazard_curve_table.insert()

# add values to the Insert object
new_curve = ins.values(model_id=hcg.model_id,
    end_branch_label=hcg.end_branch_label, _values=hcg.values, imt=hcg.imt,
    time_span_duration=hcg.time_span_duration, iml_values=hcg.iml_values)

# create a database connection
conn = engine.connect()
# add user to database by executing SQL
conn.execute(new_curve)
# close the db connection
conn.close()
        