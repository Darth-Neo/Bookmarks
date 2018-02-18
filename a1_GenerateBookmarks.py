#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import platform
import pytest
import re
import urlparse
from yaml import load as yload
from a2_DownloadPage import *

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


class Bookmarks(object):
    fileBookmarks = None
    fileFolders = None

    error_count = 0
    url_count = 0
    folders = list()
    bookmarks = list()

    # Weed out URLs that from sdevjmmlinux
    url_skip = ["192.168.1.1", "192.168.1.3", "192.168.1.6",
                "192.168.1.75", "192.168.1.137", "192.168.1.250",
                "192.168.0.100", "127.0.0.1", "localhost", ]

    def __init__(self, chromeBookmarks=None):
        home = os.getcwd()
        logger.debug(u"cwd : %s" % home)

        runDir = u"{}{}{}".format(home, os.sep, u"run")
        if not os.path.isdir(runDir):
            os.makedirs(runDir)
        os.chdir(runDir)

        self.fileFolders = runDir + os.sep + u"folders.pl"
        self.fileBookmarks = runDir + os.sep + u"bookmarks.pl"

        startDir = os.getcwd() + os.sep + u"data"
        if not os.path.isdir(startDir):
            os.makedirs(startDir)
        os.chdir(startDir)

        logger.debug(u"cwd : %s" % os.getcwd())

        if chromeBookmarks is None:
            self.chromeBookmarks = self._determineBookmarkFile()
        else:
            self.chromeBookmarks = chromeBookmarks

    @staticmethod
    def _determineBookmarkFile():

        # Determine bookmark file
        pltfrm = platform.platform()
        if re.search("^Linux.*", pltfrm, re.M | re.I):
            bookmarks = u"{}/.config/google-chrome/Default/Bookmarks".format(os.environ[u"HOME"])
        else:
            logger.error(u"Unknown OS")
            sys.exit()

        return bookmarks

    def dumpCollection(self, y, n=0, folder=None):
        n += 1
        spaces = " \t" * n

        try:
            if isinstance(y, dict):
                logger.debug(u"%sdict.len[%d]" % (spaces, len(y)))

                if u"folder" in y.values():
                    if folder is None:
                        folder = y[u"name"].encode(u"utf-8", errors=u"replace")
                    else:
                        name = y[u"name"].replace(u"\\", u"-")
                        folder += os.sep + name.encode(u"utf-8", errors=u"replace")

                    self.folders.append(folder)

                    try:
                        if not os.path.isdir(folder):
                            os.makedirs(folder)
                        os.chdir(folder)

                    except Exception, msg:
                        logger.error("%s" % msg)
                        self.error_count += 1

                    logger.debug(u"New folder : %s cwd : %s" % (folder, os.getcwd()))
                    logger.debug(u"Children : %d" % len(y[u"children"]))
                    self.dumpCollection(y[u"children"], n, folder)
                    self.url_count += 1
                    os.chdir(u"..")
                    logger.debug(u"Old folder : %s cwd : %s" % (folder, os.getcwd()))

                if u"url" in y.values():
                    uri = None
                    name = None

                    try:
                        uri = y[u"url"].encode(u"utf-8", errors=u"replace")
                        name = y[u"name"].encode(u"utf-8", errors=u"replace")

                    except Exception, msg:
                        logger.error("%s" % msg)
                        self.error_count += 1

                    logger.debug(u"%sFolder --%s" % (spaces, os.getcwd()))

                    # Dump file into directory
                    url = u"{},{}{}".format(name, uri, os.linesep)
                    with open(y["id"], "w") as f:
                        f.write(url)

                    urp = urlparse(uri)[1].split(":")[0]
                    if urp not in self.url_skip:
                        w = list([name, uri])
                        self.bookmarks.append(w)
                        logger.debug(u"%sURL : %s : %s" % (spaces, y[u"name"], y[u"url"]))

            elif isinstance(y, list):
                logger.debug(u"%slist.Len[%d]" % (spaces, len(y)))
                for v in y:
                    self.dumpCollection(v, n)
                    self.url_count += 1

        except Exception, msg:
            logger.error(u"%s" % msg)
            self.error_count += 1

        return folder

    def processBookmarks(self):

        with open(self.chromeBookmarks, "r") as f:
            bk = f.readlines()

            try:
                data = u" ".join([xx.decode(u"ascii", u"ignore") for xx in bk])
                ym = yload(data)

                if isinstance(ym, dict):
                    ymd = ym[u"roots"][u"bookmark_bar"][u"children"]
                    self.dumpCollection(ymd)

            except Exception, msg:
                logger.error(u"%s" % msg)
                sys.exit(-1)

        logger.info(u"Saving : %s" % self.fileBookmarks)
        saveList(self.bookmarks, self.fileBookmarks)

        fld = sorted(list(set([x.lower() for x in self.folders])))
        logger.info(u"Saving : %s" % self.fileFolders)
        saveList(fld, self.fileFolders)

    @pytest.mark.Bookmarks
    def testBookmarks(self):

        bookmarks = os.getcwd() + os.sep + "test" + os.sep + "TestBookmarks"

        with open(self.chromeBookmarks, "r") as f:
            bk = f.readlines()

            data = " ".join([xx.decode("utf-8", errors="replace") for xx in bk])
            ym = yload(data)

        assert (ym is not None)


@stopwatch
def checkBookmarks():
    st = startTimer()
    fb = u"{}/.config/google-chrome/Default/Bookmarks".format(os.getenv(u"HOME"))
    # fb = u"/home/james/PythonDev/Bookmarks/Bookmarks/_ChromeBookmarks"

    bookmark = Bookmarks(chromeBookmarks=fb)
    bookmark.processBookmarks()

    if logger.isEnabledFor(logging.DEBUG):
        logList(bookmark.folders)
        logList(bookmark.bookmarks)

    logger.info(u"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    logger.info(u"Found %d folders" % len(bookmark.folders))
    logger.info(u"Found %d bookmarks" % len(bookmark.bookmarks))
    logger.info(u"Errors : {}".format(bookmark.error_count))

    stopTimer(st)


if __name__ == u"__main__":
    checkBookmarks()
