#!/usr/bin/env python
import mechanize
import cookielib
from BeautifulSoup import *

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


if __name__ == u"__main__":
    # Browser
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    # br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # Want debugging messages?
    # br.set_debug_http(True)
    # br.set_debug_redirects(True)
    # br.set_debug_responses(True)

    # User-Agent (this is cheating, ok?)
    br.addheaders = [(u"User-agent", u"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) \
                                    Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1")]

    # Open some site, let"s pick a random one, the first that pops in mind:
    url = u"http://www.google.com"
    br.add_password(u"http://safe-site.domain", u"username", u"password")
    r = br.open(url)
    html = r.read()

    # Show the source
    soup = BeautifulSoup(html)
    output = soup.prettify().decode(u"utf-8", errors=u"replace")
    logger.debug(u"HTML: %s " % output)

    # Show the html title
    logger.info(u"%s----->Title: %s " % (br.title(), os.linesep))

    logger.info(u"%s----->Show the response headers" % os.linesep)
    logger.info(u"\t%s " % r.info())

    logger.info(u"%s----->Show the available forms" % os.linesep)
    for f in br.forms():
        logger.info(u"\t%s " % f)

    # Select the first (index zero) form
    br.select_form(nr=0)

    logger.info(u"%s----->Search" % os.linesep)
    br.form[u"q"] = u"weekend codes"
    br.submit()
    soup = BeautifulSoup(br.response().read())
    output = soup.prettify().decode(u"utf-8", errors=u"replace")
    logger.info(u"\t%s " % output)

    logger.info(u"%s----->Looking at some results in link format" % os.linesep)
    for l in br.links(url_regex=u"stockrt"):
        logger.info(u"\t%s " % l)
