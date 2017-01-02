#!/usr/bin/env python

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


if __name__ == u"__main__":


    fileWords = u"word_ip.pd"

    cf = open(fileWords, u"rb")
    wd = pickle.load(cf)
    logger.debug(u"Loaded : %s" % fileWords)
    cf.close()

    for k, v in wd:
        logger.info(u"{} : ()".format(k, v))