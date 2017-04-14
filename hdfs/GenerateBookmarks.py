#!/usr/bin/env python

import os
import sys
import time
import pytest
import platform
from yaml import load as yload
from urlparse import urlparse
# from DownloadPage import *

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


class Bookmarks(object):
    pickleBookmarks = None
    pickleFolders = None
    error_count = 0
    url_count = 0
    folders = list()
    bookmarks = list()

    # Weed out URLs that are from LAN
    url_skip = ["192.168.1.1", "192.168.1.3", "192.168.1.6",
                "192.168.1.75", "192.168.1.137", "192.168.1.250",
                "192.168.0.100", "127.0.0.1", "localhost", "chrome"]

    def __init__(self, BookmarkFile=None, DumpBookmarksFolders=False):
        home = os.getcwd()
        logger.debug("cwd : %s" % os.getcwd())

        now = time.strftime("%Y%d%m_%H%M%S")
        runDir = "{}{}{}".format(home, os.sep, "run_" + now)
        if not os.path.isdir(runDir):
            os.makedirs(runDir)
        os.chdir(runDir)

        self.pickleFolders = runDir + os.sep + "folders.pl"
        self.pickleBookmarks = runDir + os.sep + "bookmarks.pl"

        startDir = os.getcwd() + os.sep + "data"
        os.makedirs(startDir)
        os.chdir(startDir)

        logger.debug("cwd : %s" % os.getcwd())

        if BookmarkFile is None:
            self.BookmarkFile = self._determine_bookmark_file()
        else:
            self.BookmarkFile = BookmarkFile

        if DumpBookmarksFolders is False:
            self.dump_bookmarks = False
        else:
            self.dump_bookmarks = True

    def traverse_bookmark_folders(self, y, n=0, folder=None):
        n += 1
        spaces = " \t" * n

        try:
            if isinstance(y, dict):
                logger.debug("%sdict.len[%d]" % (spaces, len(y)))

                if "folder" in y.values():
                    if folder is None:
                        folder = y["name"].encode("utf-8", errors="replace")
                    else:
                        name = y["name"].replace("\\", "-")
                        folder += os.sep + name.encode("utf-8", errors="replace")

                    self.folders.append(folder)

                    try:
                        if not os.path.isdir(folder):
                            os.makedirs(folder)
                        os.chdir(folder)

                    except Exception, msg:
                        logger.error("%s" % msg)
                        self.error_count += 1

                    logger.debug("New folder : %s cwd : %s" % (folder, os.getcwd()))
                    logger.debug("Children : %d" % len(y["children"]))
                    self.traverse_bookmark_folders(y["children"], n, folder)
                    self.url_count += 1
                    os.chdir("..")
                    logger.debug("Old folder : %s cwd : %s" % (folder, os.getcwd()))

                if "url" in y.values():
                    uri = None
                    name = None

                    try:
                        uri = y["url"].encode("utf-8", errors="replace")
                        name = y["name"].encode("utf-8", errors="replace")
                    except Exception, msg:
                        logger.debug("%s" % msg)
                        self.error_count += 1

                    logger.debug("%sFolder --%s" % (spaces, os.getcwd()))

                    url = "{},{}{}".format(name, uri, os.linesep)
                    self.bookmarks.append(url)

                    # Dump file into directory
                    with open(y["id"], "wb") as f:
                        f.write(url)

                    try:
                        urp = urlparse(uri)[1].split(":")[0]
                        if urp not in self.url_skip:
                            # w = list([name, uri])
                            logger.debug("%sURL : %s : %s" % (spaces, y["name"], y["url"]))

                    except Exception, msg:
                        logger.debug("%s" % msg)
                        self.error_count += 1

            elif isinstance(y, list):
                logger.debug("%slist.Len[%d]" % (spaces, len(y)))
                for v in y:
                    self.traverse_bookmark_folders(v, n)
                    self.url_count += 1

        except Exception, msg:
            logger.debug("%s" % msg)
            self.error_count += 1

        return folder

    def read_bookmarks(self):
        for url in self.bookmarks:
            yield url

    def output_bookmarks(self):
        for x in self.read_bookmarks():
            try:
                s = x.split(",")
                url = s[1][:-1]

                if url[:4] == "http":
                    output = "{}\t{}{}".format(s[0], url, os.linesep)
                    sys.stdout.write(output)

            except Exception, msg:
                logger.debug("%s" % msg)
                self.error_count += 1

    def process_bookmarks(self):

        with open(self.BookmarkFile, "rb") as f:
            bk = f.readlines()

            try:
                data = " ".join([xx.decode("utf-8", errors="replace") for xx in bk])
                ym = yload(data)

                if isinstance(ym, dict):
                    ymd = ym["roots"]["bookmark_bar"]["children"]
                    self.traverse_bookmark_folders(ymd)

            except Exception, msg:
                logger.error("%s" % msg)

            logger.debug("Saving : %s" % self.pickleBookmarks)
            saveList(self.bookmarks, self.pickleBookmarks)

            fld = sorted(list(set([x.lower() for x in self.folders])))
            logger.debug("Saving : %s" % self.pickleFolders)
            saveList(fld, self.pickleFolders)

        return self.bookmarks

    @pytest.mark.Bookmarks
    def test_Bookmarks(self):

        bookmarks = os.getcwd() + os.sep + "test" + os.sep + "TestBookmarks"

        with open(bookmarks, "rb") as f:
            bk = f.readlines()

            data = " ".join([xx.decode("utf-8", errors="replace") for xx in bk])
            ym = yload(data)

        assert (ym is not None)

    @staticmethod
    def _determine_bookmark_file():

        # Determine bookmark file
        pltfrm = platform.platform()
        if re.search("^Linux.*", pltfrm, re.M | re.I):
            browserBookmarks = "{}/.config/google-chrome/Default/Bookmarks".format(os.environ["HOME"])
        else:
            logger.error("Unknown OS")
            sys.exit()

        return browserBookmarks

def checkBookmarks():

    fileBookmarks = "{}/.config/google-chrome/Default/Bookmarks".format(os.environ["HOME"])
    bookmark = Bookmarks(BookmarkFile=fileBookmarks)
    bookmark.process_bookmarks()
    bookmark.output_bookmarks()

if __name__ == "__main__":
    checkBookmarks()
