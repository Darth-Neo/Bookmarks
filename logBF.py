#!/usr/bin/env python

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


if __name__ == u"__main__":

    runDir = u"run"
    home = os.getcwd()

    if not os.path.isdir(runDir):
        os.makedirs(runDir)

    fileFolders = home + os.sep + runDir + os.sep + u"folders.pl"
    fileBookmarks = home + os.sep + runDir + os.sep + u"bookmarks.pl"

    folders = loadList(fileFolders)
    logList(folders)

    bookmarks = loadList(fileBookmarks)
    logList(bookmarks)

