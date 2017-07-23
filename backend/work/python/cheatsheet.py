#!/usr/bin/python
#
#
import sys  # uses for sys.exit function

hello_str = "Hello World"
hello_int = 21
hello_bool = True
hello_tuple = (21, 22)
hello_list = ["Hello, ", "this", "is", "a", "list"]
int_condition = 6

hello_list = list()
hello_list.append("Hello, ")
hello_list.append("this")
hello_list.append("is")
hello_list.append("a")
hello_list.append("list")

hello_dict = {"first_name": "Cristian",
              "last_name": "Lupu",
              "eye_color": "brown"}


print hello_str
print hello_int
print hello_bool
print hello_tuple
print hello_list
print hello_dict

hello_list[0] += "!"  # this is a comment
print hello_list[0]

print str(hello_tuple[0])
print hello_dict["first_name"] + " " + hello_dict["last_name"] +\
        " has " + hello_dict["eye_color"] + " eyes"

print("{0} {1} has {2} eyes".format(hello_dict["first_name"],
                                    hello_dict["last_name"],
                                    hello_dict["eye_color"]))

if int_condition < 6:
    sys.exit("int_condition must be >=6")
else:
    print("int_condition was >=6, continuing")

target_int = raw_input("How many integers?")

try:
    target_int = int(target_int)
except ValueError:
    sys.exit("You must enter an integer")

ints = list()
count = 0

while count < target_int:
    new_int = raw_input("Please input integer {0}:".format(count + 1))
    isint = True
    try:
        new_int = int(new_int)

    except:
        isint = False
        print("You must enter an integer")

    if isint:
        ints.append(new_int)
        count += 1
    print "Using a for loop"
    for value in ints:
        print(str(value))

    print "Using a while loop"
    total = len(ints)
    count = 0
    while count < total:
        print str(ints[count])
        count += 1
