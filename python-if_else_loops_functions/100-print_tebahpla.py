#!/usr/bin/python3
for i in range(26):
    c = 122 - i
    if i % 2 == 0:
        print("{:c}".format(c), end="")
    else:
        print("{:c}".format(c - 32), end="")
