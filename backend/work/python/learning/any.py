#!/usr/local/bin/python3

items = [0, None, 0.0, True, 0, 7]
found = False
for item in items:
    print('scanning item',item)
    if item:
        found = True
        break

if found:
    print("At least one item is true")
else:
    print("All items evaluated to False")