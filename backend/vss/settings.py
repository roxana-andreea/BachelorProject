# -*- coding: utf-8 -*-
"""
    Normal settings file for Eve.

    Differently from a configuration file for an Eve application backed by Mongo
    we need to define the schema using the registerSchema decorator.

"""
from eve_sqlalchemy.decorators import registerSchema
from models import Device, User, Input
from api import Sha1Auth
from eve.utils import config
import os


# LOG_FILE = 'api.log'
DEBUG = True

# if not DEBUG:
#

AUTH_FIELD = 'id_user'
# ALLOWED_FILTERS = True
# VALIDATE_FILTERING = True

API_NAME = 'VSS API'
API_PATH = 'localhost:5000'

ID_FIELD = 'id'
ITEM_LOOKUP_FIELD = ID_FIELD
config.ID_FIELD = ID_FIELD
config.ITEM_LOOKUP_FIELD = ID_FIELD

# TRANSPARENT_SCHEMA_RULES = True

SQLALCHEMY_TRACK_MODIFICATIONS = True
# SQLALCHEMY_DATABASE_URI = 'sqlite://'
# SQLALCHEMY_DATABASE_URI = 'mysql://vss:1!vss@vss.lupu.online/db'
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'mysql://vss:1!vss@vss.lupu.online/db')

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

# The following two lines will output the SQL statements executed by SQLAlchemy. Useful while debugging
# and in development. Turned off by default
# --------
SQLALCHEMY_ECHO = True
SQLALCHEMY_RECORD_QUERIES = True


registerSchema('users')(User)
registerSchema('devices')(Device)
# registerSchema('locations')(Location)
registerSchema('inputs')(Input)



# The default schema is generated by the decorator
DOMAIN = {
    'users': User._eve_schema['users'],
    'devices': Device._eve_schema['devices'],
    # 'locations': Location._eve_schema['locations'],
    'inputs': Input._eve_schema['inputs'],
    }

DOMAIN['users'].update({
#     'item_title': 'name',
    'authentication': Sha1Auth,
    'public_methods': ['POST'],
    'public_item_methods': ['PUT'],
    'additional_lookup': {
        'url': 'regex("[\w@]+")',
        'field': 'login',
    },
    'schema': {
        'name': {
            'type': 'string',
            'required': True,
        },
        'login': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'password': {
            'type': 'string',
            'required': True,
        },
    },

    # 'transparent_schema_rules': True,
    # 'auth_field': 'id',
    #  'additional_lookup': {
    #      'url': '[0-9]+',
    #      'field': 'id_user'
    #      },
#     'cache_control': 'max-age=10,must-revalidate',
#     'cache_expires': 10,
#     'resource_methods': ['GET', 'POST', 'DELETE']
    })
DOMAIN['devices'].update({
    'schema': {
        'name': {
            'type': 'string',
            'required': True,
        },
        'serial': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'id_user': {
            'type': 'objectid',
            'required': True,
            'field': 'id',
            'data_relation': {
                'resource': 'users',
                # make the owner embeddable with ?embedded={"owner":1}
                'embeddable': True
            },
        },
        # 'id_user': {
        #     'type': 'string',
        # },
    },
    'public_methods': [],
    # 'transparent_schema_rules': True,
    # 'authentication': Sha1Auth,
    'auth_field': 'id_user',
})
# DOMAIN['locations'].update({
#     # 'public_methods': [],
#     # 'auth_field': 'id_user',
# })
DOMAIN['inputs'].update({
    'schema': {
        'value': {
            'type': 'string',
            'required': True,
        },
        'id_user': {
            'type': 'objectid',
            'required': True,
            'field': 'id',
            'data_relation': {
                'resource': 'users',
                'embeddable': True
            },
        },
        'pid': {
            'type': 'string',
            'required': True,
        },

        'id_device': {
            'type': 'objectid',
            'required': True,
            'field': 'id_device',
            'data_relation': {
                'resource': 'devices',
                'embeddable': True
            },
        },
    },
    'public_methods': [],
    # 'authentication': Sha1Auth,
    'auth_field': 'id_user',
})


# PUBLIC_METHODS = ['GET', 'POST']
# PUBLIC_ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']
PUBLIC_METHODS = ['GET']
PUBLIC_ITEM_METHODS = []
# ALLOW_UNKNOWN = True
# SCHEMA_ENDPOINT = 'schema'

# DATE_CREATED = 'created'
# LAST_UPDATED = 'updated'
# ETAG = 'etag'
