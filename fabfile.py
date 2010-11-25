# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""
    Basic deployment script for opengem.
"""

import getpass
import sys

from fabric.api import env, run, sudo, cd, hosts
from fabric.state import output as fabric_output
from time import gmtime, strftime

# We really don't care about warnings.
fabric_output.warnings = False

@hosts('gemsun04.ethz.ch')
def deploy_server():
    """Install/update and restart redis-server and rabbitmq-server."""
    env.user = 'gemadmin'
    apt_get_pkgs = ['redis-server', 'rabbitmq-server']
    for pkg in apt_get_pkgs:
        # Check if the app is installed
        if not _warn_only(run, 'which %s' % pkg):
            # If it's not installed, install it
            sudo('apt-get install -y %s' % pkg, shell=False)
        else:
            # If the app is installed, kill it and update it
            sudo('/etc/init.d/%s stop' % pkg, shell=False)
            sudo('apt-get install -y --upgrade %s' % pkg, shell=False)
        # Now start/restart the app
        sudo('/etc/init.d/%s restart'% pkg, shell=False) 

def deploy_worker():
    """Install/udpate and restart celery."""
    env.user = 'gemadmin'
    # env.hosts = ["gemsun03.ethz.ch", "gemsun04.ethz.ch"]
    env.hosts = ["184.106.220.98", "184.106.248.104"] # TODO: remove  me; for testing only
    # gemsun02.ethz.ch not currently included because it has a weird distro
    # location of openquake tarball from which we can install/update celery
    openquake_tarball_url = "http://opengem.globalquakemodel.org/job/OpenGEM\
/lastSuccessfulBuild/artifact/dist/opengem-0.1.0.tar.gz"
    # check if pip is installed:
    if not _warn_only(run, 'which %s' % 'pip'):
        # install it
        sudo('apt-get install pip-python')
    run('pip install celery --upgrade -f %s' % openquake_tarball_url)
    # TODO: should we check if celery is already installed?    

def deploy():
    """Deploy, configure, and start server/worker processes on the specified
    nodes.
    
    Currently, node hosts are hard-coded into this script."""
    server_deploy()
    worker_deploy()

def development():
    """ Specify development hosts """
    env.user = getpass.getuser()
    env.hosts = ["localhost"] #"host1", "host2", "host3"]

def production():
    """ Specify production hosts """
    env.user = "deploy"
    env.hosts = ["productionhost1", "productionhost2",
                 "productionhost3", "productionhost4"]

def bootstrap(deploy_dir="/tmp/opengem/"):
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
