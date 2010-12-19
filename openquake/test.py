# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
"""
Helper functions for our unit and smoke tests.
"""


import json
import os
import random
import subprocess
import time

from celery.decorators import task
import guppy

from openquake.logs import LOG
from openquake import producer
from openquake import flags
from openquake import kvs

FLAGS = flags.FLAGS

flags.DEFINE_boolean('download_test_data', True, 
        'Fetch test data files if needed')
        
DATA_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../tests/data'))

OUTPUT_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../tests/data/output'))

SCHEMA_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../docs/schema'))


WAIT_TIME_STEP_FOR_TASK_SECS = 0.5
MAX_WAIT_LOOPS = 10
MAX_WAIT_TIME_MILLISECS = 1200


def test_file(file_name):
    return os.path.join(DATA_DIR, file_name)

def test_output_file(file_name):
    return os.path.join(OUTPUT_DIR, file_name)

def smoketest_file(file_name):
    """ Take a file name and return the full path to the file in the smoketests
    directory """
    return os.path.join(os.path.dirname(__file__), "../smoketests", file_name)

class WordProducer(producer.FileProducer):
    """Simple File parser that looks for three 
    space-separated values on each line - lat, long and value"""
    def _parse(self):
        for line in self.file:
            col, row, value = line.strip().split(' ', 2)
            yield ((int(col), int(row)), value)


def guarantee_file(path, url):
    """Based on flag, download test data file or raise error."""
    if not os.path.isfile(path):
        if not FLAGS.download_test_data:
            raise Exception("Test data does not exist")
        LOG.info("Downloading test data for %s", path)
        retcode = subprocess.call(["curl", url, "-o", path])
        if retcode:
            raise Exception("Test data could not be downloaded from %s" % (url))


def timeit(method):
    """Decorator for timing methods"""
    def _timed(*args, **kw):
        """Wrapped function for timed methods"""
        timestart = time.time()
        result = method(*args, **kw)
        timeend = time.time()

        print '%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, timeend-timestart)
        return result
    try:
        import nose
        return nose.tools.make_decorator(method)(_timed)
    except ImportError, _e:
        pass
    return _timed    


def skipit(method):
    """Decorator for skipping tests"""
    try:
        import nose
        from nose.plugins.skip import SkipTest
    except ImportError, _e:
        def skip_me(*_args, **_kw):
            """The skipped method"""
            print "Can't raise nose SkipTest error, silently skipping %r" % (
                method.__name__)
        return skip_me
    def skipme(*_args, **_kw):
        """The skipped method"""
        print "Raising a nose SkipTest error"
        raise SkipTest("skipping method %r" % method.__name__)
    return nose.tools.make_decorator(method)(skipme)


def measureit(method):
    """Decorator that profiles memory usage"""
    def _measured(*args, **kw):
        """Decorator that profiles memory usage"""
        result =  method(*args, **kw)
        print guppy.hpy().heap()
        return result
    try:
        import nose
        return nose.tools.make_decorator(method)(_measured)
    except ImportError, _e:
        pass
    return _measured  


def wait_for_celery_tasks(celery_results, 
                          max_wait_loops=MAX_WAIT_LOOPS, 
                          wait_time=WAIT_TIME_STEP_FOR_TASK_SECS):
    """celery_results is a list of celery task result objects.
    This function waits until all tasks have finished.
    """

    # if a celery task has not yet finished, wait for a second
    # then check again
    counter = 0
    while (False in [result.ready() for result in celery_results]):
        counter += 1

        if counter > max_wait_loops:
            raise RuntimeError, "wait too long for celery worker threads"

        time.sleep(wait_time)
    

@task
def simple_task_return_name(name, **kwargs):

    # wait for random time interval between 0 and MAX_WAIT_TIME_SECS seconds,
    # to ensure that results are returned in arbitrary order
    logger = simple_task_return_name.get_logger(**kwargs)

    wait_time = _wait_a_bit()
    logger.info("processing %s, waited %s milliseconds" % (name, wait_time))
    return name

@task
def simple_task_return_name_to_memcache(name, **kwargs):

    logger = simple_task_return_name_to_memcache.get_logger(**kwargs)

    memcache_client = kvs.get_client(binary=False)

    wait_time = _wait_a_bit()
    logger.info("processing %s, waited %s milliseconds" % (name, wait_time))

    memcache_client.set(name, name)
    logger.info("wrote to memcache key %s" % (name))

@task
def simple_task_list_dict_to_memcache(name, **kwargs):

    logger = simple_task_list_dict_to_memcache.get_logger(**kwargs)

    memcache_client = kvs.get_client(binary=False)

    wait_time = _wait_a_bit()
    logger.info("processing list/dict.%s, waited %s milliseconds" % (name, wait_time))

    memcache_client.set("list.%s" % name, [name, name])
    memcache_client.set("dict.%s" % name, {name: name})
    logger.info("wrote to list/dict for memcache key %s" % (name))

@task
def simple_task_json_to_memcache(name, **kwargs):

    logger = simple_task_json_to_memcache.get_logger(**kwargs)

    memcache_client = kvs.get_client(binary=False)

    wait_time = _wait_a_bit()
    logger.info("processing json.%s, waited %s milliseconds" % (name, wait_time))

    test_dict = {"list.%s" % name: [name, name], 
                 "dict.%s" % name: {name: name}}
    test_dict_serialized = json.JSONEncoder().encode(test_dict)

    memcache_client.set(name, test_dict_serialized)
    logger.info("wrote to json for memcache key %s" % (name))

def _wait_a_bit():
    wait_time = random.randrange(0, MAX_WAIT_TIME_MILLISECS)
    time.sleep(wait_time/1000)
    return wait_time
