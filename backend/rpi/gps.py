# -*- coding: utf-8 -*-

"""
Testing playground for python serial modules
"""
timeout=5
from telnetlib import Telnet
from datetime import datetime
import time
import re
import requests
import logging
import json

API_PATH = 'http://vss.lupu.online:8080'
USER_LOGIN = 'test@domain1'
USER_PASSWORD = 'secret1'
GPS_PID='99'
USER_ID=1
DEVICE_ID=1
#number of seconds between updates
FREQUENCY_OK=600
FREQUENCY_NOK=30


def print_response(res):
    debug('response={} {}'.format(res.status_code, res.reason))
    debug('headers={}'.format(res.headers))
    debug('json={}'.format(res.json()))

def decode(response):
    return re.sub(r'[\r\n:]|AT|OK|\+CGPSINFO',"",response.decode('UTF-8'))

def debug(str):
    # str =  re.sub(r'[\r\n]|AT',"",response.decode('UTF-8'))
    print(str)
    # print('DEBUG|{}|{}'.format(str(datetime.now()), str))
    logger.debug(str)

def info(str):
    # str =  re.sub(r'[\r\n:]|AT|OK|\+CGPSINFO',"",response.decode('UTF-8'))
    print(str)
    logger.info(str)

"""Logging"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create a file handler
handler = logging.FileHandler('/var/log/rpi-gps.log')
handler.setLevel(logging.DEBUG)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)

"""API"""
def upload_input(value):
    headers={'Content-Type': 'application/json'}
    auth = (USER_LOGIN,USER_PASSWORD)
    input={
        'pid': GPS_PID,
        'value': value,
        'id_user': USER_ID,
        'id_device': DEVICE_ID,
    }
    res = requests.post(
        '{}/inputs'.format(API_PATH),
        data=json.dumps(input),
        headers=headers,
        auth=auth,
    )
    print_response(res)


"""Telnet"""
tn = Telnet('127.0.0.1', 2000)  # connect to finger port
tn.write(b'AT\r\n')
debug(tn.read_until(b'OK', timeout=timeout))
tn.write(b'AT+CREG?\r\n')
debug(tn.read_until(b'+CREG', timeout=timeout))
time.sleep(2)
tn.write(b'AT+CGSOCKCONT=1,"IP","internet"\r\n')
debug(tn.read_until(b'OK', timeout=timeout))
# tn.write(b'AT+CSOCKAUTH=1,1,\"Internet\",\"Orange\"\r\n')
# debug(tn.read_until(b'OK', timeout=timeout))
tn.write(b'AT+CGPSURL="supl.google.com:7276"\r\n')
debug(tn.read_until(b'OK', timeout=timeout))
tn.write(b'AT+CGPSSSL=0\r\n')
debug(tn.read_until(b'OK', timeout=timeout))
tn.write(b'AT+CGPS=1,1\r\n')
debug(tn.read_until(b'OK', timeout=timeout))
tn.close()
time.sleep(2)

while True:
    debug("Starting LOOP")
    tn = Telnet('127.0.0.1', 2000)  # connect to finger port
    tn.write(b'AT+CGPSINFO\r\n')
    # print('{}|{}'.format(str(datetime.now()),tn.read_until(b'OK', timeout=timeout)))
    try:
        response=tn.read_until(b'OK', timeout=timeout)
    except BrokenPipeError:
        info("BrokenPipeError")
        continue
    tn.close()
    value=decode(response)
    info('Got value from modem for location: {}'.format(value))
    #valid coordinates
    try:
        valid_coords=value.split(',',2)[1] in ['N', 'S']
    except IndexError:
        valid_coords=False
    debug('valid_coords={}'.format(valid_coords))

    if not valid_coords:
        info("GPS during init phase, retrying in {} seconds".format(FREQUENCY_NOK))
        time.sleep(FREQUENCY_NOK)
    else:
        upload_input(value)
        info("Uploaded location to API '{}', next update in {} seconds".format(value,FREQUENCY_OK))
        time.sleep(FREQUENCY_OK)
