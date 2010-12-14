# -*- coding: utf-8 -*-


import os
import unittest

from sqlalchemy import *
from openquake.serializer import hazard_curve_serializer as gen

from sqlalchemy.orm import sessionmaker


class HazardResultTestCase(unittest.TestCase):
    
    def setUp(self):
        engine = create_engine("sqlite:///:memory:", echo=False)
        gen.Base.metadata.drop_all(engine)
        gen.Base.metadata.create_all(engine)

        self.session = sessionmaker(bind=engine)()
    
    def tearDown(self):
        # delete the table
        #self.session.delete()
        # flush the session
        self.session.flush()

    def test_can_store_a_hazard_result(self):
        hazard_result = gen.HazardResult("MODEL_ID",
                "TIME_SPAN", "SA_PERIOD", "SA_DAMPING")

        self.session.add(hazard_result)

        stored_hazard_result = self.session.query(
                gen.HazardResult).filter_by(model_id="MODEL_ID").first()
        
        self.assertEqual(hazard_result, stored_hazard_result)