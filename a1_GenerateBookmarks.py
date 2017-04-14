#!/usr/bin/env python

# from __future__ import unicode_literals
import os
import pytest
import platform
from yaml import load as yload
import urllib2
from a2_DownloadPage import *

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
            logger.debug("%sdict.len[%d]" % (spaces, len(y)))

            if "folder" in y.values():
                if folder is None:
                    folder = y["name"].encode("utf-8", errors="replace").lower()
                else:
                    name = y["name"].replace("\\", "-")
                    folder += os.sep + name.encode("utf-8", errors="replace").lower()

                folders.append(folder)

                try:
                    if not os.path.isdir(folder):
                        os.makedirs(folder)
                    os.chdir(folder)

                except Exception, msg:
                    logger.error("{0} : {1}".format(msg, folder))
                    error_count += 1

                logger.info("New folder : %s cwd : %s" % (folder, os.getcwd()))
                logger.info("Children : %d" % len(y["children"]))
                dumpCollection(y["children"], n, folder)
                url_count += 1
                os.chdir("..")
                logger.info("Old folder : %s cwd : %s" % (folder, os.getcwd()))

            elif "url" in y.values():
                uri = None
                name = None

                try:
                    uri = y["url"].encode("utf-8", errors="replace")
                    name = y["name"].encode("utf-8", errors="replace")
                except Exception, msg:
                    logger.error("%s" % msg)
                    error_count += 1

                logger.info("%sFolder --%s" % (spaces, os.getcwd()))

                # Dump file into directory
                url = "{},{}{}".format(uri, name, folder, os.linesep)
                with open(y["id"], "wb") as f:
                    f.write(url)

                urp = urlparse(uri)[1].split(":")[0]
                if urp not in url_skip:
                    w = list([name, uri])
                    bookmarks.append(w)
                    logger.info("%sURL : %s : %s" % (spaces, y["name"], y["url"]))

        elif isinstance(y, list):
            logger.debug("%slist.Len[%d]" % (spaces, len(y)))
            for v in y:
                dumpCollection(v, n, folder)
                url_count += 1

    except Exception as e:
        logger.error("Error on line {0}".format(sys.exc_info()[-1].tb_lineno), type(e), e)
        error_count += 1

    return folder


class Bookmarks(object):
    fileBookmarks = None
    fileFolders = None

    def __init__(self, bookmarks=None):
        home = os.getcwd()
        logger.info("cwd : %s" % os.getcwd())

        runDir = "{}{}{}".format(home, os.sep, "run")
        if not os.path.isdir(runDir):
            os.makedirs(runDir)
        os.chdir(runDir)

        self.fileFolders = runDir + os.sep + "folders.pl"
        self.fileBookmarks = runDir + os.sep + "bookmarks.pl"

        startDir = os.getcwd() + os.sep + "data"
        if not os.path.isdir(startDir):
            os.makedirs(startDir)
        os.chdir(startDir)

        logger.info("cwd : %s" % os.getcwd())

        if bookmarks is None:
            self.bookmarks = self._determineBookmarkFile()
        else:
            self.bookmarks = bookmarks

    def processBookmarks(self):

        with open(self.bookmarks, "rb") as f:
            bk = f.readlines()

            try:
                data = " ".join([xx.decode("utf-8", errors="replace") for xx in bk])
                ym = yload(data)

                if isinstance(ym, dict):
                    ymd = ym["roots"]["bookmark_bar"]["children"]
                    dumpCollection(ymd)

            except Exception, msg:
                logger.error("%s" % msg)

        logger.info("Saving : %s" % self.fileBookmarks)
        saveList(bookmarks, self.fileBookmarks)

        fld = sorted(list(set([x.lower() for x in folders])))
        logger.info("Saving : %s" % self.fileFolders)
        saveList(fld, self.fileFolders)

    @pytest.mark.Bookmarks
    def testBookmarks(self):

        bookmarks = os.getcwd() + os.sep + "test" + os.sep + "TestBookmarks"

        with open(bookmarks, "rb") as f:
            bk = f.readlines()

            data = " ".join([xx.decode("utf-8", errors="replace") for xx in bk])
            ym = yload(data)

        assert (ym is not None)

    @staticmethod
    def _determineBookmarkFile():

        # Determine bookmark file
        pltfrm = platform.platform()
        if re.search("^Linux.*", pltfrm, re.M | re.I):
            bookmarks = "{}/.config/google-chrome/Default/Bookmarks".format(os.environ["HOME"])
        else:
            logger.error("Unknown OS")
            sys.exit()

        return bookmarks

@stopwatch
def checkBookmarks():

    st = startTimer()

    bookmark = Bookmarks()
    bookmark.processBookmarks()

    if logger.isEnabledFor(logging.DEBUG):
        logList(folders)
        logList(bookmarks)

    logger.info("Found %d folders" % len(folders))
    logger.info("Found %d bookmarks" % len(bookmarks))
    logger.info("Errors : {}".format(error_count))

    stopTimer(st)

if __name__ == "__main__":
    checkBookmarks()
