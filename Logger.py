#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import logging.handlers
import pickle
import sys
import time

#
# Logging and utilities
#
import os

DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARN
ERROR = logging.ERROR


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


def setupLogging(name):
    #
    # Logging setup
    #
    directory = u"logs"
    if not os.path.isdir(directory):
        os.makedirs(directory)

    logger = logging.getLogger(name)
    logFile = u"./logs/log.txt"

    # Note: Levels - DEBUG INFO WARN ERROR CRITICAL
    logger.setLevel(logging.INFO)

    logFormatter = logging.Formatter(u"%(asctime)s [%(levelname)-5.5s] [%(filename)s:%(lineno)s ] %(message)s")

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    fileHandler = logging.handlers.RotatingFileHandler(logFile, maxBytes=262144, backupCount=2)
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    h = NullHandler()
    logger.addHandler(h)

    return logger


# Simple way to include common functions
logger = setupLogging(__name__)
logger.setLevel(INFO)


def ConfigSectionMap(section, Config):
    dictV1 = dict()
    options = Config.options(section)

    for option in options:
        try:
            dictV1[option] = Config.get(section, option)

            if dictV1[option] == -1:
                logger.debug(u"skip: %s" % option)

        except Exception, msg:
            logger.debug(u"%s on %s!" % (msg, option))
            dictV1[option] = None

    logger.debug(u"dict : %s" % dictV1)

    return dictV1


def startTimer():
    # measure process time, wall time
    t0 = time.clock()
    start_time = time.time()
    strStartTime = time.asctime(time.localtime(start_time))
    logger.debug(u"Start time : %s" % strStartTime)

    return start_time


def stopTimer(start_time):
    # measure wall time
    strStartTime = time.asctime(time.localtime(start_time))
    logger.debug(u"Start time : %s" % strStartTime)

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

    logger.info(u"Process Time = %4.2f seconds, of %d Hours, %d Minute(s), %d Seconds" %
                (timeTaken, hours, minutes, seconds))


def stopwatch(func):
    def fw(*args, **kwargs):
        st = startTimer()
        logger.debug(u"Before calling %s" % func.__name__)
        func(*args, **kwargs)
        logger.debug(u"After calling %s" % func.__name__)
        stopTimer(st)

    return fw


def dict_count(d, v):
    if v in d:
        d[v] += 1
    else:
        d[v] = 1


def saveList(pl, listFile):
    try:
        logger.debug(u"Save : %s" % listFile)

        cf = open(listFile, "w")
        pickle.dump(pl, cf)
        cf.close()

    except IOError, msg:
        logger.error(u"%s - %s " % (msg, str(sys.exc_info()[0])))


def loadDict(dictFile):
    pl = None

    if not os.path.exists(dictFile):
        logger.error(u"%s : Does Not Exist!" % dictFile)

    try:
        cf = open(dictFile, u"rb")
        pl = pickle.load(cf)
        logger.debug(u"Loaded : %s" % dictFile)
        cf.close()

    except Exception, msg:
        logger.error(u"%s" % msg)

    return pl


def saveDict(pl, dictFile):
    try:
        logger.debug(u"Save : %s" % dictFile)

        cf = open(dictFile, "wb")
        pickle.dump(pl, cf)
        cf.close()

    except IOError, msg:
        logger.error(u"%s - %s " % (msg, str(sys.exc_info()[0])))


def loadList(listFile):
    pl = None

    if not os.path.exists(listFile):
        logger.error(u"%s : Does Not Exist!" % listFile)

    try:
        cf = open(listFile, "r")
        pl = pickle.load(cf)
        logger.debug(u"Loaded : %s" % listFile)
        cf.close()

    except Exception, msg:
        logger.error(u"%s" % msg)

    return pl

def logList(l):
    for n, x in enumerate(l):
        logger.info("%d : %s" % (n, x))


def logDict(d):
    for k, v in d.items():
        logger.info("%d : %s" % (k, k))


def force_unicode(value):
    """
    Forces a bytestring to become a Unicode string.
    """

    if isinstance(value, str):
        value = value.decode('utf-8', 'replace')
    elif not isinstance(value, basestring):
        value = unicode(value)

    return value
