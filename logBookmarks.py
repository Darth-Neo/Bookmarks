#!/usr/bin/python
#
# Natural Language Processing of Information
#
import os
import pickle
from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


def loadList(listFile):

    pl = None

    if not os.path.exists(listFile):
        logger.error(u"%s : Does Not Exist!" % listFile)

    try:
        cf = open(listFile, u"rb")
        pl = pickle.load(cf)
        logger.info(u"Loaded : %s" % listFile)
        cf.close()

    except Exception, msg:
        logger.error(u"%s" % msg)

    return pl

if __name__ == u"__main__":
    listFile = u"/home/james.morris/PythonDev/Bookmarks/src/folders.pl"
    pl = loadList(listFile)

    for x in pl:
        print x






