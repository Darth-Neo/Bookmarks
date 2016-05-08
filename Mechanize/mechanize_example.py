#!/usr/bin/env python
from mechanize import Browser
import mechanize

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

if __name__ == u"__main__":
    br = mechanize.Browser()
    br.open(u"http://www.example.com/")

    response1 = br.follow_link(text_regex=r"cheeses*shop", nr=1)
    assert br.viewing_html()

    print br.title()
    print response1.geturl()
    print response1.info()  # headers
    print response1.read()  # body

    browser = Browser()
    response = browser.open(u'http://www.google.com')
    print response.code

    import mechanize

    br = mechanize.Browser()
    br.open(u"http://www.google.com/")
    for f in br.forms():
        print f
