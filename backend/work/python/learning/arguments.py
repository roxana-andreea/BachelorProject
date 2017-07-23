#!/usr/local/bin/python3

def connect(**options):
    params= {
        'host': options.get('host', '127.0.0.1'),
        'port': options.get('port', '3306'),
        'user': options.get('user', 'user'),
        'pwd': options.get('pwd','pwd')
    }
    print(params)

connect()
connect(host='8.8.8.8',port='1111', user='USER', pwd='PASS')
