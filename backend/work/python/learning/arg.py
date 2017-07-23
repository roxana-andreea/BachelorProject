#!/usr/local/bin/python3

def func(a,b,c=7, *args, **kwargs):
    print(a,b,c)
    print(args)
    print(kwargs)

func(1, 2, 3, *(5, 7, 9), **{'A': 'a', 'B': 'b'})
func(1, 2, 3, 5, 7, 9, A='a', B='b')  # same as previous one

