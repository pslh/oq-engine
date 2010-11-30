# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""
    Basic deployment script for openquake.
"""

import getpass
import sys

from fabric.api import env, run, sudo, cd, hosts, local
from fabric.state import output as fabric_output
from time import gmtime, strftime

# We really don't care about warnings.
fabric_output.warnings = False

# temporary
OPENQUAKE_DEMO_PKG_URL = "http://gemsun04.ethz.ch/geonode-client/temp/\
openquake-0.11.tar.gz"

@hosts('gemsun04.ethz.ch')
def server():
    """Restart redis-server and rabbitmq-server.

    Note: This function assumes rabbitmq and redis are already installed."""
    # Note: the target host of this deploy script should configure sudoer
    # privileges of env.user such that the following commands (such as 
    # rabbitmqctl, apt-get, etc.) can be run as sudo without a password.
    env.user = 'gemadmin'
    if not _pip_is_installed():
        _install_pip()

    redis = 'redis-server'
    rabbitmq = 'rabbitmq-server'
    
    stop = '/etc/init.d/%s stop'
    start = '/etc/init.d/%s start'

    # stop server processes
    _sudo_no_shell(stop % redis)
    _sudo_no_shell(stop % rabbitmq)

    # update the openquake package
    _install_openquake()

    # restart server processes
    _sudo_no_shell(start % redis)
    _sudo_no_shell(start % rabbitmq) 


@hosts('gemsun03.ethz.ch', 'gemsun04.ethz.ch')
def worker():
    """Update and restart celery.

    Note: This function assumes that celery is already installed and configured
    on the client."""
    
    env.user = 'gemadmin'
    if not _pip_is_installed():
        _install_pip()
    # kill celeryd processes
    _sudo_no_shell('/etc/init.d/celeryd stop')
    
    # update openquake package
    _install_openquake() 
    
    # restart celery
    _sudo_no_shell('/etc/init.d/celeryd start')

def _pip_is_installed():
    return _warn_only(run, 'which pip')

def _install_pip():
    _sudo_no_shell('apt-get install python-pip -y')

def _install_openquake():
    _sudo_no_shell('pip install openquake -f %s' % OPENQUAKE_DEMO_PKG_URL)

def _sudo_no_shell(command):
    sudo(command, shell=False)

def development():
    """ Specify development hosts """
    env.user = getpass.getuser()
    env.hosts = ["localhost"] #"host1", "host2", "host3"]

def production():
    """ Specify production hosts """
    env.user = "deploy"
    env.hosts = ["productionhost1", "productionhost2",
                 "productionhost3", "productionhost4"]

def bootstrap(deploy_dir="/tmp/openquake/"):
    """ Bootstraps an environment for runtime """
    if not ls("%s/releases" % deploy_dir):
        run("mkdir -p %s/releases" % deploy_dir)

def usage():
    print "OpenGEM deployment."
    print "To bootstrap run: fab [environment] bootstrap"
    print "To deploy run: fab [environment] deploy"
    print
    print "available environments:"
    print "development"
    print "production"

def ls(file):
    env.warn_only = True
    res = run("ls %s" % file)
    env.warn_only = False
    
    print type(res)

    return res


def _warn_only(fn, command):
    env.warn_only = True
    output = fn(command)
    env.warn_only = False
    return output

