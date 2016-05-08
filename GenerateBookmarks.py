#!/usr/bin/env python
import pytest
import platform
from yaml import load as yload

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(DEBUG)


class Bookmarks(object):
    fileBookmarks = None
    filefolders = None

    def __init__(self, fileBookmarks=None):
        runDir = u"run"

        home = os.getcwd()

        if not os.path.isdir(runDir):
            os.makedirs(runDir)

        if fileBookmarks is None:
            self.fileBookmarks = self._determineBookmarkFile()
        else:
            self.fileBookmarks = fileBookmarks

        self.fileFolders = home + os.sep + runDir + os.sep + u"folders.pl"

    def processBookmarks(self):
        flds = None
        bkms = None

        with open(self.fileBookmarks, "rb") as f:
            bk = f.readlines()

            try:

                data = u" ".join([xx.decode(u"utf-8", errors=u"replace") for xx in bk])
                ym = yload(data)

                if isinstance(ym, dict):
                    url = ym[u"roots"][u"bookmark_bar"][u"children"]
                    flds, bkms = dumpCollection(url)
                else:
                    raise SystemExit()

            except Exception, msg:
                logger.error(u"%s" % msg)

        logger.info(u"Saving : %s" % self.fileFolders)
        saveList(flds, self.fileFolders)

        return flds, bkms

    @pytest.mark.Bookmarks
    def testBookmarks(self):

        bookmarks = os.getcwd() + os.sep + u"test" + os.sep + u"TestBookmarks"

        with open(bookmarks, "rb") as f:
            bk = f.readlines()

            data = u" ".join([xx.decode(u"utf-8", errors=u"replace") for xx in bk])
            ym = yload(data)

        assert (ym is not None)

    @staticmethod
    def _determineBookmarkFile():

        # Determine bookmark file
        pltfrm = platform.platform()
        if re.search(u"^Linux.*", pltfrm, re.M | re.I):
            bookmarks = u"/home/james.morris/.config/google-chrome/Default/Bookmarks"
        else:
            logger.error(u"Unknown OS")
            sys.exit()

        return bookmarks


def checkBookmarks():
    st = startTimer()

    bookmark = Bookmarks()
    folders, bookmarks = bookmark.processBookmarks()

    logger.info(u"Found %d folders" % len(folders))
    logger.info(u"Found %d bookmarks" % len(bookmarks))

    for x in folders:
        logger.debug(u"%s" % x)

    for x in bookmarks:
        logger.debug(u"%s" % x)

    stopTimer(st)

if __name__ == u"__main__":
    checkBookmarks()
