import requests
import json
from faker import Factory
import random

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
        res = requests.post('{}/User'.format(API_PATH),
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
            res = requests.post('{}/Device'.format(API_PATH),data=json.dumps(device), headers={'Content-Type': 'application/json'})
            print_response(res)
            device['id'] = res.json()['id']
            for k in range(data_num):
                data = {}
                data['id_device'] = device['id']
                parameters = ['Vehicle speed', 'Engine RPM', 'Intake air temperature', 'Fuel Tank Level Input', 'Calculated engine load']
                data['type'] = random.choice(parameters)
                data['value'] = fake.pyint()
                res = requests.post('{}/Data'.format(API_PATH),data=json.dumps(data), headers={'Content-Type': 'application/json'})
                print_response(res)


API_PATH = 'http://vss.lupu.online:8080/api'
if __name__ == "__main__":
    fake = Factory.create()
    generate_random_items(10,2,20)

    # res = requests.get('{}/User'.format(API_PATH))
    # print_response(res)
    #
    # res = requests.get('{}/Device'.format(API_PATH))
    # print_response(res)
    #
    # res = requests.get('{}/Data'.format(API_PATH))
    # print_response(res)


