#!/usr/local/bin/python3

def minimum( *n ):
    print(n)
    mn=99
    for value in n[:]:
        if value < mn:
            mn = value
    return mn

def func( **kwargs):
    print(kwargs)


print(minimum(1,2,3,4,-10))
func(a=1,b=42)
func(**{'a': 1, 'b': 42})
func(**dict(a=1,b=42))