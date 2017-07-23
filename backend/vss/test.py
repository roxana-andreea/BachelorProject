# -*- coding: utf8 -*-

import requests
import json
from faker import Factory
import random

#API_PATH = 'http://vss.lupu.online:8080/api'
API_PATH = 'http://localhost:5000'
API_LOGIN = 'cristianlupu@gmail.com'
API_PASSWORD = 'secret'
def print_response(res):
    print('response={} {}'.format(res.status_code, res.reason))
    print('headers={}'.format(res.headers))
    print('json={}'.format(res.json()))

def generate_random_items(user_num = 1, device_num = 1, data_num = 1):
    d = {}
    for i in range(user_num):
        user = {}
        user['name']=fake.name()
        user['email']=fake.email()
        user['password']=fake.sha1()
        user['token']=fake.md5()
        res = requests.post('{}/user'.format(API_PATH),
                        data=json.dumps(user),
                        headers={'Content-Type': 'application/json'})
        print_response(res)
        user['id']=res.json()['id']
        for j in range(device_num):
            device = {}
            device['id_user'] = user ['id']
            device['name'] = fake.first_name()
            device['serial'] = fake.uuid4()
            device['paired'] = fake.pybool()
            res = requests.post('{}/device'.format(API_PATH),data=json.dumps(device), headers={'Content-Type': 'application/json'})
            print_response(res)
            device['id'] = res.json()['id']
            for k in range(data_num):
                data = {}
                data['id_device'] = device['id']
                parameters = ['Vehicle speed', 'Engine RPM', 'Intake air temperature', 'Fuel Tank Level Input', 'Calculated engine load']
                data['type'] = random.choice(parameters)
                data['value'] = fake.pyint()
                res = requests.post('{}/data'.format(API_PATH),data=json.dumps(data), headers={'Content-Type': 'application/json'})
                print_response(res)
def test_data():
    """Insert sample data"""
    users = [
        {'name': 'Test User1', 'login': 'test@domain1', 'password': 'secret1'},
        {'name': 'Test User2', 'login': 'test@domain2', 'password': 'secret2'},
    ]
    devices = [
        {'name': 'Test Device11', 'serial': '0011', 'id_user': '1'},
        {'name': 'Test Device12', 'serial': '0012', 'id_user': '1'},
        {'name': 'Test Device21', 'serial': '0021', 'id_user': '2'},
        {'name': 'Test Device22', 'serial': '0022', 'id_user': '2'},
    ]
    inputs = [
        {'pid': '05', 'value': '11', 'id_user': '1', 'id_device': '1'},
        {'pid': '05', 'value': '12', 'id_user': '1', 'id_device': '2'},
        {'pid': '05', 'value': '21', 'id_user': '2', 'id_device': '1'},
        {'pid': '05', 'value': '22', 'id_user': '2', 'id_device': '2'},
    ]

    headers = {'Content-type': 'application/json'}
    url = '{}/users'.format(API_PATH)
    for user in users:
        data = json.dumps(user)
        res = requests.post(url, data=data, headers=headers)
        print_response(res)
        #view new user details
        auth = (user['login'],user['password'])
        res = requests.get(url, data=data, auth=auth, headers=headers)
        print_response(res)

    url = '{}/devices'.format(API_PATH)
    for device in devices:
        #create new device
        data=json.dumps(device)
        auth = ('test@domain'+device['id_user'],'secret'+device['id_user'])
        res = requests.post(url, data=data, headers=headers, auth=auth)
        # import pdb; pdb.set_trace()
        print_response(res)

    url = '{}/inputs'.format(API_PATH)
    for input in inputs:
        #create new device
        data=json.dumps(input)
        auth = ('test@domain'+input['id_user'],'secret'+input['id_user'])
        res = requests.post(url, data=data, headers=headers, auth=auth)
        # import pdb; pdb.set_trace()
        print_response(res)
if __name__ == "__main__":
    fake = Factory.create()
    test_data()
    # generate_random_items(10,2,20)

    # res = requests.get('{}/User'.format(API_PATH))
    # print_response(res)
    #
    # res = requests.get('{}/Device'.format(API_PATH))
    # print_response(res)
    #
    # res = requests.get('{}/Data'.format(API_PATH))
    # print_response(res)


