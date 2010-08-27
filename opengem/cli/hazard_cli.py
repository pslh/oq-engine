# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""This module contains the Python command line interface for the hazard
engine. Uses getopt for parsing of commandline parameters.

Requires a configuration file that has to be in properties format.
Requires package ConfigObj (http://www.voidspace.org.uk/python/configobj.html).
Requires package jpype (http://jpype.sourceforge.net/).

Usage: python hazard_cli.py --config='/path/to/myconfig.properties' \
                            --replace='KEY1:Value1;KEY2:VALUE2' \
                            --save='/path/to/newfile.properties'

TODO(roland): replace getopt with gflags

Usage: python hazard_cli.py [OPTION]
    Options
    -c FILE, --configuration=<file>      Name of configuration file
    -r VALUE, --replace=<value>          Replace configuration items
                                         VALUE has to be in the format
                                         KEY1=VALUE1;KEY2=VALUE2;...
    -s FILE, --save=<file>               Filename to save modified config to
    -h, --help                           Print help
"""

from configobj import ConfigObj
import cStringIO
import getopt
import jpype
import os
import sys

JAVA_PREFIX_CC = 'org.opensha.gem.GEM1.calc.gemCommandLineCalculator'

class HazardCli(object):
    """This class represents the command line interface for the hazard 
calculator.
    """

    def __init__(self, config_file, save_file=None, **kwargs):
        """Instantiate class with property entries as keyword arguments
        """

        self._config_base = ConfigObj(config_file)
        if len(self._config_base) == 0:
            raise IOError, "cannot load properties file %s" % kwargs['config']

        for prop_key in kwargs:
            self._config_base[prop_key] = kwargs[prop_key]

        # save modified properties file to disk, if requested
        if save_file is not None:
            self._save_prop_file(save_file)

    def _save_prop_file(self, path):
        self._config_base.filename = path
        self._config_base.write()

    def run(self):
        jarpath = os.path.join(os.path.abspath('..'), 'lib')
        classpath = os.path.abspath('..')
        jpype.startJVM(jpype.getDefaultJVMPath(), '-Djava.ext.dirs=%s:%s' % (jarpath, classpath))

        serialize_to = cStringIO.StringIO()
        self._config_base.write(serialize_to)

        properties_j = jpype.JClass('%s.CalculatorProperties' % JAVA_PREFIX_CC)
        properties = properties_j(serialize_to.getvalue())

        cc = jpype.JClass('%s.CommandLineCalculator' % JAVA_PREFIX_CC)
        calc = cc()
        calc.doCalculation()


def print_help():
    print __doc__


def main():
    cmdParams = sys.argv[1:]
    if len(cmdParams) == 0:
        print_help()
        sys.exit()

    opts, args = getopt.gnu_getopt(cmdParams,
                                   'hc:r:s:',
                                   [ 'help', 
                                     'config=', 
                                     'replace=',
                                     'save='])

    replace_pars = None
    replace_dict = {}
    save_filename = None

    for option, parameter in opts:

        if option == '-c' or option == '--config':
            config_filename = parameter

        if option == '-r' or option == '--replace':
            replace_pars = parameter

        if option == '-s' or option == '--save':
            save_filename = parameter

        if option == '-h' or option == '--help':
            print_help()
            sys.exit()

    if replace_pars is not None:
        replace_dict = dict([(x.split('=')[0], x.split('=')[1])
            for x in replace_pars.strip().split(';')])

    hz = HazardCli(config_filename, save_file=save_filename, **replace_dict)
    hz.run()


if __name__ == "__main__":
    main()

