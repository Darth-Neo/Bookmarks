import pysolr
import tika
import datetime

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(DEBUG)

collection = u"gettingstarted"
s = pysolr.Solr(u'http://localhost:8983/solr/%s/' % collection)
assert s is not None


def import_doc(sd, c=None):
    collection = u"gettingstarted"
    if c is None:
        c = pysolr.Solr(u'http://localhost:8983/solr/%s/' % collection)
    try:
        return c.add(sd, commit=True)

    except Exception, msg:
        logger.error(u"%s" % msg)
        return None


def search_doc(sd, c):
    try:
        return c.query(sd)

    except Exception, msg:
        logger.error(u"%s" % msg)
        return None


def test_fields():
    dtn = datetime.datetime.now()
    doc1 = dict(id=1, title=u'Lucene in action', author=[u'james', u'kevin'], datetime=dtn,
              d=u"book1", title_t=u"The Way of Kings", author_s=u"Brandon Sanderson")

    doc2 = dict()
    doc2[u'id'] = u"1"
    doc2[u'title'] = u"Lucene in action"
    doc2[u'author'] = [u"james", u"kevin"]
    doc2[u'id'] = u"book1"
    doc2[u'title_t'] = u"The Way of Kings"
    doc2[u'author_s'] = u"Brandon Sanderson"

    r = import_doc([doc2], s)

    logger.info(u"%s" % r)


def test_search():
    # do a search
    qd = u'title:*'

    response = search_doc(qd, s)

    for hit in response.results:
        logger.info(u"---")
        for y in hit:
            logger.info(u"    %s = %s" % (y, hit[y]))


if __name__ == u"__main__":
    test_fields()
