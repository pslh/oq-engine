# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""
    Basic deployment script for opengem.
"""

import getpass
import sys

from fabric.api import env, run, sudo, cd, hosts, local
from fabric.state import output as fabric_output
from time import gmtime, strftime

# We really don't care about warnings.
fabric_output.warnings = False

@hosts('gemsun04.ethz.ch')
def deploy_server():
    """Restart redis-server and rabbitmq-server.

    Note: This function assumes rabbitmq and redis are already installed."""
    # Note: the target host of this deploy script should configure sudoer
    # privileges of env.user such that the following commands (such as 
    # rabbitmqctl, apt-get, etc.) can be run as sudo without a password.
    env.user = 'gemadmin'
    apt_get_pkgs = ['redis-server', 'rabbitmq-server']
    for pkg in apt_get_pkgs:
        # Kill it
        sudo('/etc/init.d/%s stop' % pkg, shell=False)
        # Now start/restart the app
        sudo('/etc/init.d/%s restart'% pkg, shell=False)
    # as a final action, configure rabbitmq
    #rabbit_cfg = ['rabbitmqctl delete_vhost celeryvhost',\
    #    'rabbitmqctl add_vhost celeryvhost',\
    #    'rabbitmqctl delete_user celeryuser',\
    #    'rabbitmqctl add_user celeryuser celery',\
    #    'rabbitmqctl set_permissions -p celeryvhost celeryuser ".*" ".*" ".*"']
    #for command in rabbit_cfg:
    #    env.warn_only = True
    #    sudo(command, shell=False)
    #    env.warn_only = False

@hosts('gemsun03.ethz.ch') #, 'gemsun04.ethz.ch')
def deploy_worker():
    """Update and restart celery.

    Note: This function assumes that celery is already installed and configured
    on the client. It is also assumed that the host of the worker has a clone
    of the OpenQuake source in /home/gemadmin/proj/openquake/."""
    
    env.user = 'gemadmin'
    # location of openquake tarball from which we can update celery
    openquake_tarball_url = "http://opengem.globalquakemodel.org/job/OpenQuake/\
lastSuccessfulBuild/artifact/dist/openquake-0.1.0.tar.gz"
    # check if pip is installed:
    if not _warn_only(run, 'which %s' % 'pip'):
        # install it
        sudo('apt-get install python-pip -y', shell=False)
    # kill celeryd processes
    run("for pid in `ps aux | grep [c]elery | awk '{ print $2 }'`; do kill -9 \
$pid; done")
    #sudo('pip install openquake --upgrade -f %s' % openquake_tarball_url,\
    #    shell=False)
    # restart celery
    # must be run from the source root
    # TODO(LMB): I don't like this hard-coded path, nor do I like executing from
    # this dir.
    with cd('/home/gemadmin/proj/openquake/'):
        local('./celeryd.sh')

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

