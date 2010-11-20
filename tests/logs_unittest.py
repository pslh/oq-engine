import os
import unittest

from opengem import logs

FAKE_JOB_ID = "8675309"
LOG_FILE_PATH = os.path.join(os.getcwd(), '%s.log' % FAKE_JOB_ID)

class LogsTestCase(unittest.TestCase):
    
    def setUp(self):
        # clean up the log file
        if os.path.exists(LOG_FILE_PATH):
            os.system('rm %s' % LOG_FILE_PATH)

    def tearDown(self):
        pass

    def test_validation_logger_write_single_line(self):
        """Test procedure:
1) Make up some fake job ID
2) Call logs.make_job_logger(job_id) to make a logger obj
3) Write one line to the file (file can just be in the CWD) using the 'validate'
logger method
4) Verify the contents of the log file
        """
        logger = logs.make_job_logger(FAKE_JOB_ID)
        expected_log_text = "This is a test log entry for job_id = %s." % \
FAKE_JOB_ID
        # write to the log using a monkey patched validate() logging method
        logger.validate(expected_log_text)
       
        self.assertTrue(os.path.exists(LOG_FILE_PATH)) 
        # open the log file
        # read contents and compare
        log_file = open(LOG_FILE_PATH, 'r')
        
        actual_log_text = log_file.readlines()
        # should only be 1 line of text
        self.assertEqual(1, len(actual_log_text))
        self.assertEqual(actual_log_text[0], expected_log_text + '\n')


    def test_validation_logger_write_many_lines(self):
        """Test procedure:
Basically the same as the single line logger test, except we'll log multiple
lines of text."""
        logger = logs.make_job_logger(FAKE_JOB_ID)
        # generate 100 fake log entries
        expected_log_text = [ 'Log entry number %d' % \
x for x in range(100)]
        
        # add the example log text to the log file
        for entry in expected_log_text:
            logger.validate(entry)

        self.assertTrue(os.path.exists(LOG_FILE_PATH))
        # open the log file
        # read the contents and compare
        log_file = open(LOG_FILE_PATH, 'r')

        actual_log_text = log_file.readlines()
        # verify the log file contents
        # append a '\n' to each item of the expected_log_text; this should make
        # the expected and actual match
        self.assertEqual([x + '\n' for x in expected_log_text],\
actual_log_text)
