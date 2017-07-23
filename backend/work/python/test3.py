#!/usr/bin/python
#

from random import *

def modify_string(original):
    original += "has been modified"

def modify_string_return(original):
    original += "has been modified"
    return original

test_string = "This is a test string"
modify_string(test_string)
print test_string
test_string = modify_string_return(test_string)
print test_string

cont = False
var = 0

if cont:
    var = 1234
    print var

try:
    assert cont == True

