#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""
A smoketest suite running framework.

Usage Examples:

    # to run a single suite
    python smoketest.py examplesuitename

    # to run a suite not from the OpenGemModel
    python run_tests.py git@github.com:gem/otherrepo.git/othersuite
"""

import os
import sys
import unittest

import git
from git import Git, Repo

from openquake import logs
from openquake import flags
from openquake import job

from openquake.hazard import job as hazjob
from openquake.hazard import opensha
from openquake.risk import job as riskjob
from openquake.risk.job import probabilistic
FLAGS = flags.FLAGS

flags.DEFINE_boolean('profile', False, 'Run profiler?')
flags.DEFINE_boolean('load_profile', False, 'Load profiler data?')
flags.DEFINE_string('profile_log', 'gem-risk.profile', 'Profiling log')

CHECKOUT_DIR = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../OpenGemModel'))

REPO_URL = "git@github.com:gem/OpenGemModel.git"

if __name__ == '__main__':
    args = FLAGS(sys.argv)  
    logs.init_logs()
    
    # Make sure there's a checkout and it's up to date (of OpenGemModel)
    if not os.path.exists(CHECKOUT_DIR):
        repo = Repo.clone_from(REPO_URL, CHECKOUT_DIR)
    job_path = os.path.join(CHECKOUT_DIR, "tests", args[1], "config.gem")
    if FLAGS.profile:
        import cProfile
        cProfile.run('job.run_job(job_path)', FLAGS.profile_log)
    elif FLAGS.load_profile:
        import pstats
        p = pstats.Stats(FLAGS.profile_log)
        p.sort_stats('time').print_stats(100)   
        p.print_callees(1.0, 'recv')
    else:
        job.run_job(job_path)