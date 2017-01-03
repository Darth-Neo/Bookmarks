#!/usr/bin/env python

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


def logWordID(fileWords = u"word_ip.pd"):

    with open(fileWords, u"rb") as cf:
        wd = pickle.load(cf)
        logger.debug(u"Loaded : %s" % fileWords)
        cf.close()

        for k, v in wd.items():
            logger.info(u"{}".format(k))
            for n, v1 in enumerate(v):
                logger.info(u"    {}.{}".format(n, v1[0]))


if __name__ == u"__main__":
    logWordID()