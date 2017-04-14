#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymongo import *

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

client = MongoClient(u'mongodb://localhost:27017/')
db = client[u"local"]
Bookmarks = db[u'Bookmarks']
Words = db[u'Words']
# collection.remove()

error_count = 0
processed_count = 0

pf = u"word_ip.pd"


def normalize_words(threshold=5.0):
    global processed_count
    global error_count
    global pf

    dictWords = dict()

    for m, url in enumerate(Bookmarks.find()):
        try:
            # logger.info(u"%6d, %s" % (m, url[u"url"]))
            for word in url[u"words"]:
                l = list([url[u"name"], url[u"url"], word[0], word[1]])
                # logger.info(u"%s\t%3.2f\t%d\t%s" % (l[0], l[3], l[2], l[1]))
                if word[0] > threshold:
                    if word[2] in dictWords:
                        dictWords[word[2]].append(l)
                    else:
                        dictWords[word[2]] = list([l])
            processed_count += 1

        except Exception, msg:
            # logger.error(u"%s" % msg)
            error_count += 1

        with open(pf, u"wb") as cf:
            pickle.dump(dictWords, cf)

    logger.info(u"Found {} bookmarks".format(processed_count))
    logger.info(u"Errors : {}".format(error_count))

    return dictWords


@stopwatch
def insert_word_counts():
    global pf

    with open(pf, u"rb") as cf:
        pd = pickle.load(cf)

    for k, v in pd.items():
        logger.info(u"%d \t%s" % (len(v), k))

        for v1 in v:
            logger.info(u"\t%s\t %s" % (v1[0], v1[1]))

        wl = dict({k.replace(".", "-") : v})
        Words.insert(wl)

if __name__ == u"__main__":

    # d = normalize_words(threshold=5.0)

    insert_word_counts()
