#!/usr/bin/env python
import os
import requests
import random
import time
from urlparse import urlparse
from a3_SolrImport import import_doc
import tika
from tika import parser
from pymongo import *

from Logger import *
# logger = setupLogging(__name__)
logger.setLevel(INFO)

client = MongoClient(u"mongodb://localhost:27017/")
db = client[u"local"]
mongo_collection = db[u"Bookmarks"]
# collection.remove()

stop_words = None


def get_stop_words():
    global stop_words

    if stop_words is None:
        with open("stop-word-list.csv", "rb") as f:
            sw = f.readlines()

        nsw = [x.split(",") for x in sw][0]
        stop_words = [unicode(x.strip()) for x in nsw]

    return stop_words


def compute_tf_idf(url, text):
    sw = get_stop_words()
    output = list()
    doc = dict()

    ti = text.items()
    s = sorted(ti, key=lambda n: n[1] * 100.0, reverse=True)
    len_s = len(s) + 1

    # logger.debug("Words : %d" % len_s)
    # logger.debug("tfidf \t count \t text")

    for n, v in enumerate(s):
        # logger.debug(u"%s : %d" % v)
        word = v[0]
        count = v[1]
        if not (word in sw) and (len(word) > 0) and (count > 1):
            tfidf = float(float(count / float(len_s)) * 100.0)
            # logger.debug("%3.2f \t %4d \t .%s." % (tfidf, count, word))
            p = list([tfidf, count, word])
            output.append(p)

    doc[u"url"] = url[1]
    doc[u"words"] = output
    doc[u"name"] = url[0]
    return doc


def persist_url_words(message):
    mongo_collection.insert_one(message)


def export_doc(message):
    import_doc([message])


def tika_parse(html, show_content=False):
    parsed = None
    try:
        ServerEndpoint = u"http://localhost:9998"
        parsed = parser.from_buffer(html, serverEndpoint=ServerEndpoint)

        n = 0
        if show_content is True:
            for k, v in parsed[u"metadata"].items():
                logger.debug(u"    {} {} = {}".format(n, k, v))
                n += 1

            logger.debug(u"  {} Content = {} ...".format(n, parsed[u"content"].strip()))

    except Exception, msg:
        logger.error(u"{}".format(msg))
        # sys.exit(1)

    return parsed


def download_page(url):
    global stop_words
    text = dict()

    html = requests.get(url[1], timeout=10).text

    tp = tika_parse(html)
    df = [x.lower() for x in tp[u"content"].split(os.linesep) if x != os.linesep and len(x) > 2]

    try:
        for words in df:
            # logger.info(".{}.".format(words))
            for word in words.split(u" "):
                if len(word) > 1:
                    w = word.strip().strip(u"\t").lower()
                    # logger.debug(u"    .{}.".format(w))
                    dict_count(text, w)

    except Exception, msg:
        logger.warn(u"%s" % msg)

    f = compute_tf_idf(url, text)
    persist_url_words(f)
    export_doc(f)


@stopwatch
def main(test=False):
    processed = 0
    error_count = 0
    delay = 5.0
    rows = 5

    if test is False:
        bookmarks = loadList(u"run/bookmarks.pl")
    else:
        bookmarks = loadList(u"run/bookmarks.pl")
        bookmarks = bookmarks[:5]

    try:
        for url in bookmarks:
            try:
                logger.info(u"Downloading URL : {}".format(url[1]))
                download_page(url)

                r = (int(random.random() * delay) + 1)
                # logger.info(u"Sleep : {}".format(r))
                time.sleep(r)

                processed += 1

            except Exception, msg:
                logger.warn(u"%s" % msg)
                error_count += 1

    except KeyboardInterrupt:
        logger.info(u"Complete")

    logger.info(u"Found {} bookmarks".format(processed))
    logger.info(u"Errors : {}".format(error_count))

if __name__ == u"__main__":
    os.environ[u"DEBUG_PYSOLR"] = u"0"
    main(test=False)