# -*- coding: utf-8 -*-

import os
import unittest

from sqlalchemy import *
from openquake.seismicsources.hazard_curve_generator import *



class HazardResult(unittest.TestCase):
    
    def setUp(self):
        # create the table
        session = create_session()
        metadata.drop_all()
        metadata.create_all()
    
    def tearDown(self):
        # delete the table
        session.delete(hc)
        # flush the session
        session.flush()
        
"""   
    def test_simple_hazard_curve_witten_to_db(self):
        
        def run(stmt):
            rs = stmt.execute()
            for row in rs:
                print row
        
        #SELECT * FROM hazard_curve_table iml_values  
        s = hazard_result_table.select(hazard_result_table.c.model_id == '56')
        rs = s.execute()
        results = rs.fetchall()
        
        self.assertTrue(len(results) > 0)
        


        #Return a result set
        
        #print rs.rowcount
        #print s
        
        
        # creating a session
        session = create_session()
""" 

    def test_db_accepts_hazard_curve_vauels(self):
        
        # creating the hazard curve object
        hc = HazardResult('1', '56', 'test_timeSpan', 'test_sa_period',
                    'test_sa_damping')
            
                    # end_branch_label == 'TEST'
        
        #hc = session.query(HazardResult).selectfirst(hazard_result_table.c.model_id=='56')
            
session.save(hc)
        
# load the object from database
hazard_curve_table.select(end_branch_label == 'TEST')
        # query the database
        # assert the hazard curve has been stored into the database
        
"""     
