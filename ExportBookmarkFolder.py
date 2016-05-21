#!/usr/bin/env python

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


def getFolderBookmarks(pl, dumpFolder):
    if pl is None:
        return

    for link in pl:
        logger.info(u"Link :%s" % link)

        if link == dumpFolder:
            logger.info(u"%s" % link)
            return link
        else:
            link = getFolderBookmarks(link, dumpFolder)

        return link

if __name__ == u"__main__":

    dumpFolder = u"Disney"
    listFile = os.getcwd() + os.sep + u"run" + os.sep + u"folders.pl"

    pl = loadList(listFile)

    bookmarks = getFolderBookmarks(pl, dumpFolder)

    saveList(bookmarks, u"%s.pl" % dumpFolder)
