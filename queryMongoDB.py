#! /usr/bin/env python
from pymongo import MongoClient

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(DEBUG)

MONGODB_SERVER = u"localhost"
MONGODB_PORT = 27017
MONGO_URI = u"mongodb://" + MONGODB_SERVER + u":%s" % MONGODB_PORT + u"/"
MONGODB_DB = u"local"
MONGODB_COLLECTION = u"Bookmarks"


def query_mongodb(query=u"", Collection=u"Bookmarks", MONGODB_DB=u"local", LOG=False):
    client = MongoClient(MONGO_URI)
    db = client[MONGODB_DB]
    collection = db[MONGODB_COLLECTION]

    directory = u"./run"
    if not os.path.isdir(directory):
        os.makedirs(directory)
    os.chdir(directory)

    texts = list()
    n = 0

    # filter = {u"$where": u"this.Documents.length > 0"}
    # cursor = collection.find(filter)
    cursor = collection.find()

    rv = [page for page in cursor]

    return rv


def showResult(rv):
    assert rv is not None

    for n, page in enumerate(rv):

        if isinstance(page, dict):
            for k, v in page.items():
                if isinstance(v, list):
                    for m, v1 in enumerate(v):
                        logger.debug(u"\t{}V : {}".format(m, v1))
                else:
                    logger.debug(u"{}. K : {}    V : {}".format(n, k, v))

        logger.debug(u"===========================================================================================")


if __name__ == u"__main__":

    try:
        query_mongodb()

    except KeyboardInterrupt:
        logger.debug(u"Bye..")
