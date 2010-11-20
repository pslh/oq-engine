import os
import unittest

from opengem import logs

class LogsTestCase(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_validation_logger_write(self):
        """Test procedure:
        1) Make up some fake job_id
        2) Call logs.make_job_logger(job_id) to make a logger obj
        3) Write one line to the file (file can just be in the CWD)
        4) Verify the contents of the log file
        """

        job_id = "8675309"
        # delete the log file (from previous tests) if exists
        log_file_path = os.path.join(os.getcwd(), '%s.log' % job_id)
        if os.path.exists(log_file_path):
            os.system('rm %s' % log_file_path)

        logger = logs.make_job_logger(job_id)
        expected_log_text = "This is a test log entry for job_id = %s." % job_id
        # write to the log using a monkey patched validate() logging method
        logger.validate(expected_log_text)
       
        self.assertTrue(os.path.exists(log_file_path)) 
        # open the log file
        # read contents and compare
        log_file = open(log_file_path, 'r')
        
        actual_log_text = log_file.readlines()
        # should only be 1 line of text
        self.assertEqual(1, len(actual_log_text))
        self.assertEqual(actual_log_text[0], expected_log_text + '\n')
