# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
""" 
This code is intended to use SQLAlchemy to describe the tables that are to be mapped to the database"""

import sqlalchemy

if sqlalchemy.__version__.split('.')[1] == '6':
    SQLALCHEMY_VER = 6
elif sqlalchemy.__version__.split('.')[1] == '5':
    SQLALCHEMY_VER = 5
else:
    SQLALCHEMY_VER = 0
        
if SQLALCHEMY_VER not in [5, 6]:
    raise Exception('Sorry but SqlAlchemy different than 5 or 6 is not supported')
import sys
def _output(str):
    sys.stderr.write(str + '\n')
    sys.stderr.flush()
    
_output('## Models for SqlAlchemy version %s' % SQLALCHEMY_VER)   

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper
from openquake.seismicsources import HazardCurveGenerator


#TODO BW create a 'real' connection to a DB for mapping hazard curves.

engine = create_engine('sqlite:///:memory:', echo=True)
    """sqlEngine/connection object, temporary connection to in-memory-only
     SQLite database"""

metadata = MetaData()
hazard_curve_table = hazard_curve_table('users', metadata,
                        Column('IDmodel', String),
                        Column('endBranchLabel', String),
                        Column('Values', String),
                        Column('IMT', String),
                        Column('timeSpanDuration', String),
                        Column('IMLValues', String),
                    )
mapper(HazardCurveGenerator, hazard_curve_table)                   
