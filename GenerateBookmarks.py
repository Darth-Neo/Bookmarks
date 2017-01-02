#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pytest
import platform
from yaml import load as yload
import urllib2
from DownloadPage import *

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

error_count = 0
url_count = 0
folders = list()
bookmarks = list()

# Weed out URLs that from sdevjmmlinux
url_skip = ["192.168.1.1", "192.168.1.3", "192.168.1.6",
            "192.168.1.75", "192.168.1.137", "192.168.1.250",
            "192.168.0.100", "127.0.0.1", "localhost", ]


def dumpCollection(y, n=0, folder=None):
    n += 1
    spaces = " \t" * n
    global error_count
    global url_count
    global folders
    global bookmarks

    try:
        if isinstance(y, dict):
            logger.debug(u"%sdict.len[%d]" % (spaces, len(y)))

            if  u"folder" in y.values():
                if folder is None:
                    folder = y[u"name"].encode(u"utf-8", errors=u"replace")
                else:
                    name = y[u"name"].replace(u"\\", u"-")
                    folder += os.sep + name.encode(u"utf-8", errors=u"replace")

                folders.append(folder)

                try:
                    if not os.path.isdir(folder):
                        os.makedirs(folder)
                    os.chdir(folder)

                except Exception, msg:
                    logger.error(u"%s" % msg)
                    error_count += 1

                logger.info(u"New folder : %s cwd : %s" % (folder, os.getcwd()))
                logger.info(u"Children : %d" % len(y[u"children"]))
                dumpCollection(y[u"children"], n, folder)
                url_count += 1
                os.chdir(u"..")
                logger.info(u"Old folder : %s cwd : %s" % (folder, os.getcwd()))

            if  u"url" in y.values():
                uri = None
                name = None

                try:
                    uri = y[u"url"].encode(u"utf-8", errors=u"replace")
                    name = y[u"name"].encode(u"utf-8", errors=u"replace")
                except Exception, msg:
                    logger.error(u"%s" % msg)
                    error_count += 1

                logger.info(u"%sFolder --%s" % (spaces, os.getcwd()))

                # Dump file into directory
                url = "{},{}{}".format(name, uri, os.linesep)
                with open(y[u"id"], "wb") as f:
                    f.write(url)

                urp = urlparse(uri)[1].split(":")[0]
                if urp not in url_skip:
                    w = list([name, uri])
                    bookmarks.append(w)
                    logger.info(u"%sURL : %s : %s" % (spaces, y[u"name"], y[u"url"]))

        elif isinstance(y, list):
            logger.debug(u"%slist.Len[%d]" % (spaces, len(y)))
            for v in y:
                dumpCollection(v, n)
                url_count += 1

    except Exception, msg:
        logger.error(u"%s" % msg)
        error_count += 1

    return folder


class Bookmarks(object):
    fileBookmarks = None
    fileFolders = None

    def __init__(self, bookmarks=None):
        home = os.getcwd()
        logger.info(u"cwd : %s" % os.getcwd())

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

        logger.info(u"cwd : %s" % os.getcwd())

        if bookmarks is None:
            self.bookmarks = self._determineBookmarkFile()
        else:
            self.bookmarks = bookmarks

    def processBookmarks(self):

        with open(self.bookmarks, "rb") as f:
            bk = f.readlines()

            try:
                data = u" ".join([xx.decode(u"utf-8", errors=u"replace") for xx in bk])
                ym = yload(data)

                if isinstance(ym, dict):
                    ymd = ym[u"roots"][u"bookmark_bar"][u"children"]
                    dumpCollection(ymd)

            except Exception, msg:
                logger.error(u"%s" % msg)

        logger.info(u"Saving : %s" % self.fileBookmarks)
        saveList(bookmarks, self.fileBookmarks)

        fld = sorted(list(set([x.lower() for x in folders])))
        logger.info(u"Saving : %s" % self.fileFolders)
        saveList(fld, self.fileFolders)


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
            bookmarks = u"{}/.config/google-chrome/Default/Bookmarks".format(os.environ[u"HOME"])
        else:
            logger.error(u"Unknown OS")
            sys.exit()

        return bookmarks


def checkBookmarks():

    st = startTimer()

    bookmark = Bookmarks()
    bookmark.processBookmarks()

    if logger.isEnabledFor(logging.DEBUG):
        logList(folders)
        logList(bookmarks)

    logger.info(u"Found %d folders" % len(folders))
    logger.info(u"Found %d bookmarks" % len(bookmarks))
    logger.info(u"Errors : {}".format(error_count))

    stopTimer(st)

if __name__ == u"__main__":
    checkBookmarks()
