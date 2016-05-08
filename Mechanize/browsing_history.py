#!/usr/bin/env python
import mechanize

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

if __name__ == u"__main__":
    # Browser
    br = mechanize.Browser()
    r = br.open(u"http://google.com")
    html = r.read()

    # Testing presence of link (if the link is not found you would have to
    # handle a LinkNotFoundError exception)
    br.find_link(text=u"Weekend codes")

    # Actually clicking the link
    req = br.click_link(text=u"Weekend codes")
    br.open(req)
    print br.response().read()
    print br.geturl()

    # Back
    br.back()
    print br.response().read()
    print br.geturl()