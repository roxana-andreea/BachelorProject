#!/usr/local/bin/python3

def get_squares_gen(n):
    for x in range(n):
        yield x ** 2

def counter(start=0):
    n=start
    while True:
        yield n
        n+= 1




sq = get_squares_gen(4)
print(sq)
print(next(sq))
print(next(sq))
print(next(sq))
print(next(sq))


c = counter()
print(next(c))
print(next(c))
print(next(c))
print(next(c))
print(next(c))
print(next(c))
