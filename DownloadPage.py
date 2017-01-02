#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import random
import time
from urlparse import urlparse
from BeautifulSoup import *
from pymongo import *

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

client = MongoClient(u'mongodb://localhost:27017/')
db = client[u"local"]
collection = db[u'Bookmarks']
# collection.remove()


def load_stop_words():
    with open(u"stop-word-list.csv", u"rb") as f:
        sw = f.readlines()
    nsw = [unicode(x.split(u",")) for x in sw]
    return nsw[0]

stop_words = load_stop_words()

def clean_word(v):
    nw = u""
    vv = v.lower()
    for n in range(0, len(vv)):
        if vv[n].isalpha():
            nw += vv[n]
    return nw

def log_messsage(url, text):
    output = list()
    doc = dict()

    ti = text.items()
    s = sorted(ti, key=lambda n: n[1] * 100.0, reverse=True)
    len_s = len(s) + 1

    logger.info(u"Words : %d" % len_s)
    logger.info(u"tfidf \t count \t text")

    for n, v in enumerate(s):
        if not (v[0] in stop_words) and len(v[0]) > 0 and v[1] > 1:
            tfidf = float(float(v[1] / float(len_s)) * 100.0)
            logger.info("%3.2f \t %4d \t .%s." % (tfidf, v[1], v[0]))
            p = list([tfidf, v[1], v[0]])
            output.append(p)

    doc[u"url"] = url[1]
    doc[u"words"] = output
    doc[u"name"] = url[0]
    return doc

def persist_url_words(message):
    collection.insert_one(message)

def checkHTML(ds):
    r = re.match(r"^<!.+>", unicode(ds), re.M | re.I)
    s = re.match(r"^<script>.+</script>", unicode(ds), re.M | re.I)
    t = re.match(r"^<style>.+</style>", unicode(ds), re.M | re.I)
    w = re.match(r"^<style>.+</style>", unicode(ds), re.M | re.I)

    if r is not None:
        return True
    else:
        return False

def download_page(url):
    global stop_words

    html = requests.get(url[1], timeout=10).text
    text = dict()

    hf = [ x[x.find(">")+1:] for x in html.split("<") ]
    df = [unicode(x.strip()) for x in hf if x != os.linesep]

    try:
        for ds in df:
            logger.debug(u"{}".format(ds))
            for w in ds.split(u" "):
                if w == u" ":
                    continue
                vv = clean_word(w)
                if vv not in stop_words and 20 > len(vv) > 0 :
                    dict_count(text, vv)

    except Exception, msg:
        logger.warn(u"%s" % msg)

    f = log_messsage(url, text)
    persist_url_words(f)

@stopwatch
def main():
    processed = 0
    error_count = 0
    delay = 5.0

    bookmarks = loadList(u"run/bookmarks.pl")

    try:
        for url in bookmarks:
            try:
                logger.info(u"Downloading URL : {}".format(url[1]))
                download_page(url)

                r = (int(random.random() * delay) + 1)
                logger.info(u"Sleep : {}".format(r))
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
    main()