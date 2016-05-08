#!/usr/bin/env python

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


if __name__ == u"__main__":

    listFile = os.getcwd() + os.sep + u"run" + os.sep + u"folders.pl"
    fileBookmarks = os.getcwd() + os.sep + u"run" + os.sep + u"bookmarks.pl"
    pl = loadList(listFile)

    folders, bookmarks = dumpCollection(pl)

    listBookmarks = list()
    for link in bookmarks:
        if link[:4] == u"http":
            listBookmarks.append(link)
            logger.info(u"%s" % link)

    saveList(listBookmarks, fileBookmarks)

