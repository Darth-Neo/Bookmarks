#!/usr/bin/env python
# __author__ = u"james.morris"
# __VERSION__ = u'0.1'
import os
import sys
import time
import requests
from yaml import load, dump
import pickle
from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


def startTimer():
    # measure process time, wall time
    t0 = time.clock()
    start_time = time.time()
    strStartTime = time.asctime(time.localtime(start_time))
    logger.info(u"Start time : %s" % strStartTime)

    return start_time


def stopTimer(start_time):
    # measure wall time
    strStartTime = time.asctime(time.localtime(start_time))
    logger.info(u"Start time : %s" % strStartTime)

    end_time = time.time()

    strEndTime = time.asctime(time.localtime(end_time))
    logger.info(u"End   time : %s" % strEndTime)

    # measure process time
    timeTaken = end_time - start_time
    seconds = timeTaken % 60
    minutes = timeTaken / 60
    if minutes < 60:
        hours = 0
    else:
        hours = minutes / 60
        minutes %= 60

    logger.info(u"Process Time = %4.2f seconds, of %d Hours, %d Minute(s), %d Seconds" % (timeTaken, hours, minutes, seconds))


def dumpBookmarks(y, folders=None, n=0):

    if folders is None:
        folders = list()

    n += 1
    spaces = U" " * n

    if isinstance(y, dict):
        logger.debug(u"%sdict[%d]" % (spaces, len(y)))
        for k, v in y.items():
            if k == u"type" and v == u"folder":
                fld = list()
                fld.append(y[u"name"])
                folders.append(fld)
                logger.debug(u"%sFolder %s" % (spaces, y[u"name"]))
                folders = dumpBookmarks(v, fld, n)

            elif k == u"type" and v == u"url":
                folders.append(y[u"url"])
                logger.debug(u"%sURL    %s" % (spaces, y[u"url"]))

            else:
                if k not in (u"type", u"folder"):
                    logger.debug(u"%s" % y[k])

            folders = dumpBookmarks(v, folders, n)

    elif isinstance(y, list):
        logger.debug(u"%slist[%d]" % (spaces, len(y)))
        for v in y:
            dumpBookmarks(v, folders, n)
    else:
        if isinstance(y, int):
            logger.debug(u"%s%d" % (spaces, y))
        elif isinstance(y, float):
            logger.debug(u"%s%f" % (spaces, y))
        elif isinstance(y, str):
            logger.debug(u"%s%s" % (spaces, y))
        else:
            logger.debug(u"%s%s" % (spaces, type(y)))

    return folders


def saveList(pl, listFile):
    try:
        logger.info(u"Loaded : %s" % listFile)
        cf = open(listFile, u"wb")
        pickle.dump(pl, cf)
        cf.close()

    except IOError, msg:
        logger.error(u"%s - %s " % (msg, str(sys.exc_info()[0])))


def loadList(listFile):
    concepts = None

    if not os.path.exists(listFile):
        logger.error(u"%s : Does Not Exist!" % listFile)

    try:
        cf = open(listFile, u"rb")
        pl = pickle.load(cf)
        logger.info(u"Loaded : %s" % listFile)
        cf.close()

    except Exception, msg:
        logger.error(u"%s" % msg)

    return concepts


if __name__ == u"__main__":

    st = startTimer()

    ym = None
    bookmarks = u"/home/james.morris/.config/google-chrome/Default/Bookmarks"
    listFile = os.getcwd() + os.sep + u"folders.pl"

    with open(bookmarks, "rb") as f:
        bk = f.readlines()

        data = u" ".join([x.decode(u"utf-8", errors=u"replace") for x in bk])
        ym = load(data)

        url = ym[u"roots"][u"bookmark_bar"][u"children"]
        folders = dumpBookmarks(url)

    for x in folders:
        print x

    logger.info(u"Saving : %s" % listFile)
    saveList(folders, listFile)
    stopTimer(st)
