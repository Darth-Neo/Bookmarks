#!/usr/bin/env python

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


if __name__ == u"__main__":

    listFile = os.getcwd() + os.sep + u"run" + os.sep + u"folders.pl"
    pl = loadList(listFile)

    folders, bookmarks = dumpCollection(pl)

    for link in bookmarks:
        if link[:4] == u"http":
            logger.info(u"%s" % link)
