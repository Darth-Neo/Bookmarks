#!/usr/bin/env python
import os
import requests
import random
import time
from urlparse import urlparse
from SolrImport import *
import tika
from tika import parser

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(DEBUG)


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


if __name__ == u"__main__":

    url = u"https://www.ops-class.org/"
    html = requests.get(url, timeout=10).text

    tp = tika_parse(html)
    df = [x.lower().strip() for x in tp[u"content"].split(os.linesep) if x != os.linesep and len(x) > 2]

    try:
        for words in df:
            logger.info(u".{}.".format(words))
            for word in words.split(u" "):
                w = word.strip().strip(u"\t").lower()
                logger.debug(u"    .{}.".format(w))

    except Exception, msg:
        logger.warn(u"%s" % msg)
