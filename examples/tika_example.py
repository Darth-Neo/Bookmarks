# !/usr/bin/env python
#
import re
from tika import parser
import tika

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(DEBUG)


def tika_parse(filepath, show_content=False):
    try:
        ServerEndpoint = u"http://localhost:9998"
        parsed = parser.from_file(filepath, serverEndpoint=ServerEndpoint)

        n = 0
        for k, v in parsed[u"metadata"].items():
            logger.debug(u"    {} {} = {}".format(n, k, v))
            n += 1

        if show_content is True:
            logger.debug(u"  {} Content = {} ...".format(n, parsed[u"content"].strip()))

    except Exception, msg:
        logger.error(u"{}".format(msg))
        sys.exit(1)

    return parsed


def walk_subdir(sd):
    error_count = 0
    files_parsed = 0

    try:
        for root, dirs, files in os.walk(sd, topdown=True):
            for name in files:
                nameFile = os.path.join(root, name)
                logger.debug(u"{}".format(nameFile))

                matchObj = re.match(r'^[.].+', name, re.M|re.I)

                if matchObj is not None:
                    continue
                try:
                    parsed = tika_parse(nameFile)

                    if len(parsed) > 0:
                        files_parsed += 1

                except Exception, msg:
                    logger.error(u"{} : {}".format(name, msg))
                    error_count += 1

    except Exception, msg:
        logger.error(u"%s" % msg)

    return files_parsed, error_count

@stopwatch
def test_tika_example():
    np = 0
    errors = 0

    subdir = u"./testdata"
    np, errors = walk_subdir(subdir)

    logger.info(u"Number Parsed %d" % np)
    logger.info(u"Errors        %d" % errors)


if __name__ == u"__main__":
    test_tika_example()
