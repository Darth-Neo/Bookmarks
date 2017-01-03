#!/usr/bin/env python

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


def logWordID(fileWords = u"word_ip.pd"):

    with open(fileWords, u"rb") as cf:
        wd = pickle.load(cf)
        logger.debug(u"Loaded : %s" % fileWords)
        cf.close()

        # s = sorted(m, key=lambda n: n[1])
        t = [(k, len(v)) for k, v in wd.items()]
        ts = sorted(t, key=lambda c: c[1], reverse=True)

        for v in ts:
            logger.info(u"{}".format(v[0]))
            for n, v1 in enumerate(v):
                logger.info(u"    {}. {}".format(n, v1))


if __name__ == u"__main__":
    logWordID()