""" Django settings for openquake project.  """

import os
CURRENT_DIR = os.path.dirname(__file__)

TEST_RUNNER = 'django.contrib.gis.tests.run_gis_tests'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Aurea Moemke', 'aurea.moemke@sed.ethz.ch'),
)

MANAGERS = ADMINS

# # DATABASE_ENGINE = 'sqlite3'
# # DATABASE_NAME = 'openquake.db' # Or path to database file if using sqlite3.


DATABASES = {
    'default': {
        'NAME': 'openquakeTWO',
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'USER': 'postgres',
        'PASSWORD': '',
    }
}


# GOOGLE_MAPS_API_KEY = 'abcdefg'
#GOOGLE_API_KEY = 'ABQIAAAAUmKamSWZRmEhhP1zT_-NmRRi_j0U6kJrkFvY4-OX2XYmEAa76BQs6eb3-LqZNwFaEoUNSON8Td_ryw'
GOOGLE_API_KEY = 'ABQIAAAAUmKamSWZRmEhhP1zT_-NmRRq0gCy63DKMlRvFU2-Hbvb8HpD9RSfIqFkOwQ1UzDtj94EFdKXaSoaqQ'
# YAHOO_APP_ID
# CLOUDMADE_API_KEY

GIS_DATA_DIR = os.path.join(CURRENT_DIR, '../media/gis')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '../media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

OL_API = '/media/OpenLayers/OpenLayers.js'
# OSM_API = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '!!0h0h*84l#&e*ki(t1f#)8h0wnj9!#r=w!3wxqy$e7o$3=@b&'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(CURRENT_DIR, '../templates'),
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.databrowse',
    'django.contrib.gis',
    'south',
    'olwidget',
    'openquake.faults',
    # 'openquake.seismicsources',
)

LOSS_CURVES_OUTPUT_FILE = 'loss-curves-jobber.xml'

KVS_PORT = 6379
KVS_HOST = "localhost"

SOURCEGEOM_SHP = 'seismicsources/data/sourcegeometrycatalog.shp'
WORLD_SHP = 'world/data/TM_WORLD_BORDERS-0.3.shp'
