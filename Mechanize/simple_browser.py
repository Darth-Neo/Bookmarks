#!/usr/bin/env python
import urllib
import urllib2

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


if __name__ == u"__main__":

    # Simple open?
    print urllib2.urlopen(u"http://stockrt.github.com").read()

    # With password?
    opener = urllib.FancyURLopener()
    print opener.open(u"http://user:password@stockrt.github.com").read()
