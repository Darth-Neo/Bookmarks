#!/usr/bin/env python
from random import *

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


def collect_folders(folders, n=0):
    f = list()

    for fld in folders:
        n += 1
        if isinstance(fld, "list"):
            ff = collect_folders(fld, n)
            f.append(ff)
        else:
            f.append(fld)

    return f


def directory_check(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)
    os.chdir(directory)


if __name__ == u"__main__":

    home = os.getcwd()
    logger.info(u"dir : {}".format(home))

    runDir = u"run"
    directory_check(runDir)
    os.chdir(runDir)

    learnDir = u"Learn"
    directory_check(learnDir)

    testDir = u"Test"
    directory_check(testDir)

    fileFolders = home + os.sep + runDir + os.sep + u"folders.pl"
    fileBookmarks = home + os.sep + runDir + os.sep + u"bookmarks.pl"

    folders = loadList(fileFolders)
    urls = loadList(fileBookmarks)

    logger.info(u"dir : {}".format(os.getcwd()))

    folders_size = len(folders)
    bookmarks_size = len(urls)

    group_learn_size = int(random() * folders_size)
    group_test_size = int(random() * bookmarks_size)

    pass
