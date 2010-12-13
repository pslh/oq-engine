# -*- coding: utf-8 -*-

import os
import unittest

from openquake.seismicsources import hazard_curve_generator
from openquake import hazard


class HazardCurveTestCase(unittest.TestCase):
    
    def test_simple_hazard_curve_witten_to_db(self):
        
        #SELECT * FROM hazard_curve_table iml_values  
        s = hazard_curve_table.select(hazard_curve_table.c.iml_valses)
        run(s)
        
        #Return a result set
        rs = s.execute
        
        self.assertEqual(s, test_IMLValues)