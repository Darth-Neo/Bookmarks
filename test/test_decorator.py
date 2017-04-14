#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

def stopwatch(func):
    def fw(*args, **kwargs):
        st = startTimer()
        logger.info("***********************************Before calling %s" % func.__name__)
        func(*args, **kwargs)
        logger.info("***********************************After calling %s" % func.__name__)
        stopTimer(st)
    return fw

@stopwatch
def bookmark(b):
    bookmarks = loadList("run/bookmarks.pl")
    logger.info("Bookmarks : %d" % len(bookmarks))

if __name__ == "__main__":
    b = "Hello James"
    bookmark(b)
