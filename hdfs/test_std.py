#!/usr/bin/env python
import sys
import os

file = "test_bookmarks.txt"

with open(file, "r") as f:
    l = f.readlines()

for line in l:
    nl = line[:-1].split("\t")
    print("{} \t {}".format(nl[0], nl[1]))
