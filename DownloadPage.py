#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import *

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

def load_stop_words():

    with open("stop-word-list.csv", "rb") as f:
        sw = f.readlines()

    nsw = [unicode(x.split(",")) for x in sw]

    return nsw[0]

def clean_word(v):
    nw = u""
    vv = v.lower()
    for n in range(0, len(vv)):
        if vv[n].isalnum():
            nw += vv[n]
    return nw

def test_clean_word():
    v = u"The big pid jumped the moon"
    c = clean_word(v)

if __name__ == u"__main__":

    stop_words = load_stop_words()

    url = u"http://www.foxnews.com"
    html = requests.get(url).text
    soup = BeautifulSoup(html)

    text = dict()
    data = soup.findAll(text=True)

    df = [x for x in data if x != "\n"]

    for d in df:
        ds = str(d)
        if re.match(r"^<!--.*-->", ds, re.M | re.I) is True:
            logger.debug(u"{}".format(ds))
            continue

        elif not re.match(r"^<![-]*[A-Za-z 0-9/\n]+[-]*>", ds, re.M | re.I | re.S):
            logger.debug(u"{}".format(ds))
            for w in ds.split(" "):
                if w == " ":
                    continue
                vv = clean_word(w)
                if vv not in stop_words:
                    dict_count(text, vv)

    s = sorted(text.items(), key=lambda n: n[1] * 100.0, reverse=True)
    len_s = len(s)
    logger.info("Words : %d" % len_s)

    logger.info("row \t tfidf \t count \t text")

    for n, v in enumerate(s):
        if not(v[0] in stop_words):
                if len(v[0]) > 0 and v[1] > 1:
                    tfidf = float(float(v[1] / float(len_s)) * 100.0)
                    logger.info("%3d\t %3.2f \t %4d \t .%s." % (n, tfidf, v[1], v[0]))

    filename = "fn.pl"
    saveList(s, filename)

