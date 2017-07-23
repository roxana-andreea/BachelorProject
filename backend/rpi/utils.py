import requests
import json
import logging
import os
import configparser


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



