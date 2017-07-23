# -*- coding: utf-8 -*-

"""
Script that sends OBD commands to ELM327
"""
timeout=5
from telnetlib import Telnet
from datetime import datetime
import time
import re
import requests
import logging
import json
import configparser
import os
from utils import *
from socket import timeout

def create_logger(log_file):
    """Logging"""
    global logger
    logger = logging.getLogger(__name__)
    if config['LOG']['LEVEL'] == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    elif config['LOG']['LEVEL'] == 'ERROR':
        logger.setLevel(logging.ERROR)
    else:
        logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_file)
    if config['LOG']['LEVEL'] == 'DEBUG':
        handler.setLevel(logging.DEBUG)
    elif config['LOG']['LEVEL'] == 'ERROR':
        handler.setLevel(logging.ERROR)
    else:
        handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def print_response(res):
    debug('response={} {}'.format(res.status_code, res.reason))
    # debug('headers={}'.format(res.headers))
    debug('json={}'.format(res.json()))

def debug(str):
    if config['LOG']['LEVEL'] == 'DEBUG':
        print("[DEBUG] {}".format(str))
        logger.debug(str)

def info(str):
    print("[INFO] {}".format(str))
    logger.info(str)

def error(str):
    print("[ERROR] {}".format(str))
    logger.error(str)

def upload_input(value):
    """Upload input value to RESTful API"""
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

def read_config():
    global config
    global path
    path = os.path.dirname(os.path.realpath(__file__))+"/config.ini"
    config = configparser.ConfigParser()
    config.read(path)
    # info('Reading config file from: {}'.format(path))


def upload_input(pid,value):
    """API"""
    headers={'Content-Type': 'application/json'}
    auth = (config['API']['LOGIN'],config['API']['PASSWORD'])
    input={
        'pid': pid,
        'value': value,
        'id_user': config['TESTING']['USER_ID'],
        'id_device': config['TESTING']['DEVICE_ID'],
    }
    res = requests.post(
        '{}/inputs'.format(config['API']['URL']),
        data=json.dumps(input),
        headers=headers,
        auth=auth,
    )
    print_response(res)



read_config()
create_logger(config['LOG']['FILE_OBD'])

while True:
    """Telnet"""
    debug('Connecting to {}:{}'.format(config['TELNET']['IP'],config['TELNET']['PORT']))
    try:
        tn = Telnet(config['TELNET']['IP'], config['TELNET']['PORT'], float(config['TELNET']['TIMEOUT']))
    except (ConnectionResetError,TimeoutError,ConnectionRefusedError,timeout):
         info('Connection to {}:{} not available, retrying in {} seconds...'.format(
             config['TELNET']['IP'],
             config['TELNET']['PORT'],
             config['TELNET']['FREQUENCY_LOW']
         ))
         time.sleep(int(config['TELNET']['FREQUENCY_LOW']))
         continue
    # import pdb; pdb.set_trace()
    # Engine RPM 010C
    tn.write(b'01 0C\r\n')
    time.sleep(1)
    engine_rpm=re.sub(r'01 0C41 0C | ',"",re.sub(r'[\r\n>]',"",tn.read_some().decode('UTF-8')))
    info('Received value 0x{} from Engine RPM PID 01 0C'.format(engine_rpm))
    engine_rpm = str(round(int("0x"+engine_rpm,16)/4,2))
    upload_input('010C',engine_rpm)
    info('Sent value {} for Engine RPM PID 01 0C to API {}'.format(engine_rpm,config['API']['URL']))
    #Throttle Position 0111
    tn.write(b'01 11\r\n')
    time.sleep(1)
    throttle_position=re.sub(r'01 1141 11 | ',"",re.sub(r'[\r\n>]',"",tn.read_some().decode('UTF-8')))
    info('Received value 0x{} from Throttle Position PID 01 11'.format(throttle_position))
    throttle_position = str(round(int("0x"+throttle_position,16)*100/255,2))
    upload_input('0111',throttle_position)
    info('Sent value {} for Throttle Position PID 01 11 to API {}'.format(throttle_position,config['API']['URL']))
    #Engine Temperature 0105
    tn.write(b'01 05\r\n')
    time.sleep(1)
    engine_temperature=re.sub(r'01 0541 05 | ',"",re.sub(r'[\r\n>]',"",tn.read_some().decode('UTF-8')))
    info('Received value 0x{} from Engine Temperature PID 01 05'.format(engine_temperature))
    engine_temperature = str(round(int("0x"+engine_temperature,16)-40,2))
    upload_input('0105',engine_temperature)
    info('Sent value {} for Engine Temperature PID 01 05 to API {}'.format(engine_temperature,config['API']['URL']))
    #Mass Airflow 0110
    tn.write(b'01 10\r\n')
    time.sleep(1)
    mass_airflow=re.sub(r'01 1041 10 | ',"",re.sub(r'[\r\n>]',"",tn.read_some().decode('UTF-8')))
    info('Received value 0x{} from Mass Airflow PID 01 10'.format(mass_airflow))
    mass_airflow = str(round(int("0x"+mass_airflow,16)/100,2))
    upload_input('0110',mass_airflow)
    info('Sent value {} for Mass Airflow PID 01 10 to API {}'.format(mass_airflow,config['API']['URL']))
    #Vehicle Speed 010D
    tn.write(b'01 0D\r\n')
    time.sleep(1)
    vehicle_speed=re.sub(r'01 0D41 0D | ',"",re.sub(r'[\r\n>]',"",tn.read_some().decode('UTF-8')))
    info('Received value 0x{} from Vehicle Speed PID 01 0D'.format(vehicle_speed))
    vehicle_speed = str(int("0x"+vehicle_speed,16))
    upload_input('010D',vehicle_speed)
    info('Sent value {} for Vehicle Speed PID 01 0D to API {}'.format(vehicle_speed,config['API']['URL']))
    #DTC 03
    tn.write(b'03\r\n')
    time.sleep(1)
    dtc=re.sub(r'0343 |43 | |00',"",re.sub(r'[\r\n>]',"",tn.read_some().decode('UTF-8')))
    info('Received value 0x{} from DTC PID 03'.format(dtc))
    # len=int(len(dtc)/4)
    if dtc == "03NODATA":
        upload_input('03','OK')
        info('DTC check OK: no errors found')
    else:
        upload_input('03',dtc)
        info('Sent value {} for DTC PID 03 to API {}'.format(dtc,config['API']['URL']))
    tn.close()
    info('Sleeping for {} seconds...'.format(config['TELNET']['FREQUENCY_LOW']))
    time.sleep(int(config['TELNET']['FREQUENCY_LOW']))

