#!/usr/bin/env python
import os
import requests
import random
import time
from urlparse import urlparse
import tika
from tika import parser

from Logger import *
# logger = setupLogging(__name__)
logger.setLevel(INFO)

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

    logger.debug("Words : %d" % len_s)
    logger.debug("tfidf \t count \t text")

    for n, v in enumerate(s):
        # logger.debug("%s : %d" % v)
        word = v[0]
        count = v[1]
        if not (word in sw) and (len(word) > 0) and (count > 1):
            tfidf = float(float(count / float(len_s)) * 100.0)
            # logger.debug("%3.2f \t %4d \t .%s." % (tfidf, count, word))
            p = list([tfidf, count, word])
            output.append(p)

    doc["url"] = url[1]
    doc["words"] = output
    doc["name"] = url[0]
    return doc

def tika_parse(html, show_content=False):
    parsed = None
    try:
        ServerEndpoint = "http://localhost:9998"
        parsed = parser.from_buffer(html, serverEndpoint=ServerEndpoint)

        n = 0
        if show_content is True:
            for k, v in parsed["metadata"].items():
                logger.debug("    {} {} = {}".format(n, k, v))
                n += 1

            logger.debug("  {} Content = {} ...".format(n, parsed["content"].strip()))

    except Exception, msg:
        logger.error("{}".format(msg))
        # sys.exit(1)

    return parsed

def download_page(url):
    global stop_words
    text = dict()

    html = requests.get(url, timeout=10).text
    logger.info("html : %s" % html[:25])

    tp = tika_parse(html)
    df = [x.lower() for x in tp["content"].split(os.linesep) if x != os.linesep]

    try:
        for words in df:
            logger.info(".{}.".format(words))
            for word in words.split(" "):
                if len(word) > 1:
                    w = word.strip().strip("\t").lower()
                    logger.info("    .{}.".format(w))
                    dict_count(text, w)

    except Exception, msg:
        pass
        # logger.debug("%s" % msg)

    print("u%s" % url)
    for k, v in text.items():
        print("    %s[%s]" % (k, v))

    f = compute_tf_idf(url, text)

def read_input():
    n = 0

    # lines = sys.stdin.readlines()
    with open("test_bookmarks.txt", "r") as f:
        lines = f.readlines()

    for line in lines: # sys.stdin.readlines():
        n += 1
        nl = line.split("\t")
        name = nl[0]
        url = nl[1][:-1]
        logger.info("{} Yield => {} : {}".format(n, name, url))

        download_page(url)

def main(test=False):
    processed = 0
    error_count = 0
    delay = 5.0
    rows = 5
    n = 0
    logger.debug("In main:")

    read_input()

if __name__ == "__main__":
    os.environ["DEBUG_PYSOLR"] = "0"
    main(test=False)