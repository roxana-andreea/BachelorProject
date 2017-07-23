#!/usr/local/bin/python3

def try_syntax(numerator, denominator):
    try:
        print('In the try block. {} {}'.format(numerator,denominator))
        result = numerator /denominator
    except ZeroDivisionError as zde:
        print(zde)
    else:
        print("The result is:", result)
        return result
    finally:
        print('Exiting')

print(try_syntax(12,3))
print(try_syntax(5,0))
