#!/usr/bin/env python
from urllib2 import *
import pysolr
import requests

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(DEBUG)


def createSolrConnection(collection=u"Test"):
    s = pysolr.Solr(u'http://localhost:8983/solr/%s' % collection)
    return s


def querySolrCollection(collection=u"Test", query=u"title:*"):
    server = u"localhost"
    port = 8983
    wt = u"python"
    action = u"select"
    url = u"http://%s:%d/solr/%s/%s?q=%s&wt=%s" % (server, port, collection, action, query, wt)
    logger.debug(u"%s" % url)

    s = pysolr.Solr(u'http://localhost:8983/solr/%s' % collection)
    return s, url


def resetSolr(c):
    """
    curl "http://localhost:8984/solr/demo/update?commit=true" -H "Content-Type: text/xml" \
    --data-binary '<delete><query>*:*</query></delete>'
    """

    from subprocess import call
    command = u"curl"
    p0 = u"http://localhost:8984/solr/%s/update?commit=true " % c
    p1 = u"-H 'Content-Type: text/xml' "
    p2 = u"--data-binary '<delete><query>*:*</query></delete>'"
    cmd = [u"%s %s %s %s" % (command, p0, p1, p2,)]
    call(cmd, shell=True)


if __name__ == u"__main__":

    collection = u"demo"
    resetSolr(collection)

    if False:
        s, url = querySolrCollection(collection=collection)
        logger.debug(u"%s" % url)

        conn = urlopen(url)
        rsp = eval(conn.read())

        logger.debug(u"number of matches={}".format(rsp[u'response'][u'numFound']))

        # print out the name field for each returned document
        for doc in rsp[u'response'][u'docs']:
            for k, v in doc.items():
                logger.debug(u"{} : {}".format(k, v))