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

#TODO BW create a 'real' connection to a DB for mapping hazard curves.
#TODO Change echo to False when you’re ready to put the code into production.
#engine = create_engine('sqlite:///hazard_result_table_test.db', echo=True)
"""sqlEngine/connection object, temporary connection to in-memory-only
       SQLite database"""
engine = create_engine('sqlite:///:memory:', echo=True)

metadata = MetaData(bind=engine)
                  
#SQLAlchemy SQL construction method
""" The hazard curve need to be split into thee classes: HazardResult,
HazardCurveList and HazardCurve in order reduce duplicate saved information
to the DB"""
Base = declarative_base()
class HazardResult(object):
    #Table generation
    __tablename__ = hazard_result_table
    
    id_key = Column(Integer, primary_key=True),
    model_id = Column(String),
    time_span_duration = Column(String),
    sa_period = Column(String),
    sa_damping = Column(String)
    
    #Table definition
    def __init__(self, model_id, time_span_duration, sa_period, sa_damping):
        #self.id_key = id_key
        self.model_id = model_id
        self.time_span_duration = time_span_duration
        self.sa_period = sa_period
        self.sa_damping = sa_damping
        
    def __repr__(self):
        return "<User('%s','%s', '%s', '%s', '%s')>" % (self.id_key,
        self.model_id, self.timeSpanDuration, self.sa_period, self.sa_damping)
            
class HazardCurveList(object):
    #Table generation
    __tablename__ = hazard_curve_list_table
    
    id_key = Column(Integer, primary_key=True),
    parent_id = Column('parent_id', Integer, ForeignKey('hazard_curve.id_key'))
    
    def __init__(self, id_key, parent_id):
        self.id_key = id_key
        self.parent_id = parent_id
    
class HazardCurve(object):
    pass
  
mapper(HazardResult, hazard_result_table, properties={
   'children': relationship(HazardCurveList)
})

mapper(HazardCurveList, hazard_curve_list_table)

metadata.drop_all()
metadata.create_all()     
        
hr = HazardResult('56', 'test_timeSpan', 'test_sa_period', 'test_sa_damping')

#hcl = HazardCurveList('1', '56')

print hr.id_key    
print hr.model_id
print hr.time_span_duration
print hr.sa_period
print hr.sa_damping

"""
# create an Insert object        
ins = hazard_result_table.insert()

# add values to the Insert object
new_curve = ins.values(id_key=hr.id_key, model_id=hr.model_id, 
    time_span_duration=hr.time_span_duration, sa_period=hr.sa_period, 
    sa_damping=hr.sa_damping )
"""
# create a database connection
conn = engine.connect()
# add user to database by executing SQL
conn.execute(new_curve)
# close the db connection
conn.close()
        