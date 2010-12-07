# -*- coding: utf-8 -*-

import os
import unittest

from openquake import hazard
#from openquake.seismicsources import HazardCurveGenerator

class HazardCurveTestCase(unittest.TestCase):
    
    def test_simple_hazard_curve_witten_to_db(self):
        
        hazard_curve_test = HazardCurve('FIXED', 'label', [6.0999999999999996, 6.2000000000000002, 6.2999999999999998], 'PGA', '50.0', [1.0, 2.0, 3.0])
        