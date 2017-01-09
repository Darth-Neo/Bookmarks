# !/usr/bin/env python
#
# Uses SolrConnection Modiule
#
import re
import pysolr
import random
import tika
from tika import parser
import tika
from subprocess import call

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(DEBUG)

TikaServerEndpoint = u"http://localhost:9998"
collection = u"gettingstarted"
solr_url = u'http://localhost:8983/solr/%s/' % collection
s = pysolr.Solr(solr_url)


def resetSolr(c):
    from subprocess import call
    command = u"curl"
    p0 = u"http://localhost:8983/solr/%s/update?commit=true " % c
    p1 = u"-H 'Content-Type: text/xml' "
    p2 = u"--data-binary '<delete><query>*:*</query></delete>'"
    cmd = [u"%s %s %s %s" % (command, p0, p1, p2,)]

    call(cmd, shell=True)


def random_id():
    sid = int(random.random() * 100000000)
    return sid


def create_connection(c):
    solr_url = u'http://localhost:8983/solr/%s/' % c
    s = pysolr.Solr(solr_url)
    return s


def log_parsed(p):
    for k, v in p.items():
        if k != u"content":
            logger.info(u"{} = {}".format(k, v))


def collect_errors(msg, error_count, error_msg):
    if msg in error_msg:
        error_msg[msg] += 1
    else:
        error_msg[msg] = 1
    error_count += 1
    return error_count, error_msg


def post_subdirectory(subdir):
    error_count = 0
    error_msg = dict()
    files_parsed = 0
    pd = None
    global TikaServerEndpoint
    global s

    try:
        for root, dirs, files in os.walk(subdir, topdown=True):
            for name in files:
                nameFile = os.path.join(root, name)
                logger.debug(u"{}".format(nameFile))

                matchObj = re.match(r'^[.].+', name, re.M|re.I)

                if matchObj is not None:
                    continue
                try:
                    parsed = parser.from_file(nameFile, serverEndpoint=TikaServerEndpoint)
                    pd = parsed[u"metadata"]
                    pd[u"id"] = random_id()
                    pd[u"resourcename"] = nameFile
                    pd[u"resource"] = name
                    content = parsed[u"content"]
                    if len(content) != 0:
                        pd[u"content_txt_en"] = content.encode(u"utf-8", errors=u"replace")

                    # log_parsed(pd)
                    s.add([pd], commit=True)

                    if len(parsed) > 0:
                        files_parsed += 1

                except Exception, msg:
                    logger.error(u"{} : {}".format(name, msg))
                    error_count, error_msg = collect_errors(msg, error_count, error_msg)

    except Exception, msg:
        logger.error(u"{}".format(msg))
        error_count, error_msg = collect_errors(msg, error_count, error_msg)

    return files_parsed, error_count, error_msg


def test_tika_solr():
    s = create_connection(u"Test")

    file_path = u"testdata/example.pdf"

    parsed = parser.from_file(file_path)

    log_parsed(parsed)

    s.add([parsed], commit=True)

    return 1, 0


if __name__ == u"__main__":

    start_time = startTimer()
    np = 0
    errors = 0

    collection = u"gettingstarted"

    resetSolr(collection)

    if False:
        np, errors = test_tika_solr()

    else:
        subdir = u"/Users/morrj140/Documents/SolutionEngineering/Kronos/scope"
        # subdir = u"./testdata"
        np, errors, error_msg = post_subdirectory(subdir)

        for k, v in error_msg.items():
            logger.info(u"{}[{}]".format(k, v))

    stopTimer(start_time)
    logger.info(u"\n")
    logger.info(u"Number Parsed %d" % np)
    logger.info(u"Errors        %d" % errors)

