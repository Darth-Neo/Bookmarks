#!/usr/bin/env python
from operator import itemgetter
import sys
import os

current_word = None
current_count = 0
word = None

if __name__ == "__main__":
    # input comes from STDIN
    lines = sys.stdin.readlines()

    for line in lines:
        # remove leading and trailing whitespace
        line = line.strip()

        sys.stdout.write("=================== >%s%s" % (line, os.linesep))
