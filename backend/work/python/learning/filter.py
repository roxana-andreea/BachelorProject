#!/usr/local/bin/python3

# def is_multiple_of_five(n):
#     return not n % 5

def get_multiples_of_five(n):
    return list(filter(lambda k: not k % 5, range(n)))

print(get_multiples_of_five(50))
