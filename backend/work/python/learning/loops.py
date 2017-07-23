#!/usr/local/bin/python3

n = 39
remainders = []
while n > 0:
    n, r = divmod(n,2)
    remainders.append(r)

remainders = remainders[::-1]
print(remainders)