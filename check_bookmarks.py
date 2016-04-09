#!/usr/bin/env python
# __author__ = u"james.morris"
# __VERSION__ = u'0.1'

import os
import sys
import time
import tempfile
from lxml import etree
from yaml import load, dump

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

import requests

folder = list()


def dumpBookmarks(y, n=0):

    n += 1
    spaces = U" " * n

    if isinstance(y, dict):
        logger.debug(u"%sdict[%d]" % (spaces, len(y)))
        for k, v in y.items():
            if k == u"type" and v == u"folder":
                logger.info(u"%sFolder %s" % (spaces, y[u"name"]))
            elif k == u"type" and v == u"url":
                logger.info(u"%sURL    %s" % (spaces, y[u"url"]))
            else:
                if k not in (u"type", u"folder"):
                    logger.debug(u"%s" % y[k])

            dumpBookmarks(v, n)

    elif isinstance(y, list):
        logger.debug(u"%slist[%d]" % (spaces, len(y)))
        for v in y:
            dumpBookmarks(v, n)
    else:
        if isinstance(y, int):
            logger.debug(u"%s%d" % (spaces, y))
        elif isinstance(y, float):
            logger.debug(u"%s%f" % (spaces, y))
        elif isinstance(y, str):
            logger.debug(u"%s%s" % (spaces, y))
        else:
            logger.debug(u"%s%s" % (spaces, type(y)))

if __name__ == u"__main__":
    ym = dict()
    bookmarks = u"/home/james.morris/.config/google-chrome/Default/Bookmarks"

    with open(bookmarks, "rb") as f:
        bk = f.readlines()

        data = u" ".join([x.decode(u"utf-8", errors=u"replace") for x in bk])
        ym = load(data)

    dumpBookmarks(ym)

    url = ym[u"roots"][u"bookmark_bar"][u"children"]

    pass
