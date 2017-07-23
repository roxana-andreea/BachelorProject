#!/usr/bin/python3

import sys
import logging
import requests

ERROR_SMS_FORMAT = 101
ERROR_PINCODE_VALIDATION = 102
ERROR_UNKNOWN_ACTION = 103
ERROR_UNKNOWN_PARAMETER = 104
ERROR_FEATURE_ACTIVATION = 105
URL = 'http://vss.lupu.online:8080'
LOGIN = 'test@domain1'
PASSWORD = 'secret1'
USER_ID = 1
DEVICE_ID = 1

def debug(str):
    print("[DEBUG] {}".format(str))
    logger.debug(str)

def info(str):
    print("[INFO] {}".format(str))
    logger.info(str)

def error(str):
    print("[ERROR] {}".format(str))
    logger.error(str)

def print_response(res):
    debug('response={} {}'.format(res.status_code, res.reason))
    debug('headers={}'.format(res.headers))
    debug('json={}'.format(res.json()))

def get_user_info():
    """API"""
    headers={'Content-Type': 'application/json'}
    auth = (LOGIN,PASSWORD)
    res = requests.get(
        '{}/users'.format(URL),
        headers=headers,
        auth=auth,
    )
    print_response(res)
    # import pdb; pdb.set_trace()
    return res.json()["_items"][0]['sms'],res.json()["_items"][0]['pincode']


"""Logging"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create a file handler
handler = logging.FileHandler('/var/log/rpi-sms.log')
handler.setLevel(logging.DEBUG)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)


# IN20160618_233927_00_+40753174860_00.txt

filename = sys.argv[1]
dirname = "/var/spool/gammu/inbox/"
phone = filename.split('_')[3]

debug('filename={}'.format(filename))
debug('dirname={}'.format(dirname))

sms=open(dirname+filename)
text = sms.readline()
sms.close()

info("Received SMS from number: '{}' with text: '{}'".format(phone, text))

actions = ['START', 'STOP', 'UP', 'DOWN']
parameters = ['ENGINE', 'ALARM']

sms, pincode = get_user_info()

info("For user with login '{}', the sms feature is: '{}' and pincode is: '{}'".format(LOGIN,sms,pincode))

if sms == False:
    error('SMS Feature not enabled')
    exit(ERROR_FEATURE_ACTIVATION)

try:
    action = text.split()[0]
    parameter = text.split()[1]
    pin = text.split()[2]
except IndexError:
    error('SMS Format not validated')
    exit(ERROR_SMS_FORMAT)
else:
    debug('action={}'.format(action))
    debug('parameter={}'.format(parameter))
    debug('pin from SMS={}'.format(pin))
    debug('pin from API={}'.format(pincode))


# String[] commands = {"LOCK CAR", "UNLOCK CAR", "START ENGINE", "STOP ENGINE", "UP WINDOWS", "DOWN WINDOWS", "OPEN TRUNK", "ALARM START"};

# import pdb; pdb.set_trace()

if str(pincode) == pin:
    info('Pincode validated')
    if action in ['START','STOP','LOCK','UNLOCK','UP','DOWN','OPEN','CLOSE']:
        if parameter in ['ENGINE','CAR','WINDOWS','TRUNK','ALARM']:
            info('Received action {} for {}'.format(action,parameter))
        else:
            error('Parameter not implemented')
            exit(ERROR_UNKNOWN_PARAMETER)
    else:
        error('Action not implemented')
        exit(ERROR_UNKNOWN_ACTION)
else:
    error('Pincode not validated')
    exit(ERROR_PINCODE_VALIDATION)

exit(0)