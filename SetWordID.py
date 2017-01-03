#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymongo import *

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

client = MongoClient(u'mongodb://localhost:27017/')
db = client[u"local"]
bookmarks = db[u'Bookmarks']
words = db[u'Words']
# collection.remove()

def normalizeWords(dictWords=None, threshold=5.0, saveWords=False):

    if dictWords is None:
        dictWords = dict()

    for m, url in enumerate(bookmarks.find()):
        # logger.info(u"{}.Name : {}".format(m, url[u"url"]))

        for word in url[u"words"]:
            # logger.debug(u"  {:20s} \t {:5} \t {:3.2f}".format(word[2], word[1], word[0]))
            l = list([url[u"Name"], url[u"url"], word[0], word[1]])
            if word[0] > threshold:
                if word[2] in dictWords:
                    dictWords[word[2]].append(l)
                else:
                    dictWords[word[2]] = list([l])

    if saveWords is True:
        with open(u"word_ip.pd", u"wb") as cf:
            pickle.dump(dictWords, cf)

    return dictWords

@stopwatch
def calcWord():

    for threshold in range(1,20):
        dictWords = dict()
        normalizeWords(dictWords=dictWords, threshold=threshold)
        logger.info(u"Threshold {:3} {:5,d}".format(threshold, len(dictWords)))

if __name__ == u"__main__":
    calcWord()

