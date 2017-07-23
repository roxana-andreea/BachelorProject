import os
PWD = os.path.abspath(os.curdir)
DEBUG = True
#SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/api/api.db'.format(PWD)
SQLALCHEMY_DATABASE_URI = 'mysql://vss:1!vss@vss.lupu.online/db'
SECRET_KEY = 'enydM2ANhdcoKwdVa0jWvEsbPFuQpMjf' # Create your own.
SESSION_PROTECTION = 'strong'
# SERVER_NAME = 'lupu.online'
# API_SUBDOMAIN = 'api'
SEND_FILE_MAX_AGE_DEFAULT = 7200
SQLALCHEMY_TRACK_MODIFICATIONS = True
ERROR_404_HELP = True

