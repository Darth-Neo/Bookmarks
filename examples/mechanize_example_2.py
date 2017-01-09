#!/usr/bin/env python
import sys
import mechanize
import logging

# To make sure you're seeing all debug output:
logger = logging.getLogger("mechanize")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

br = mechanize.Browser()

import mechanize# Explicitly configure proxies (Browser will attempt to set good defaults).
# Note the userinfo ("joe:password@") and port number (":3128") are optional.
br.set_proxies({"http": "joe:password@myproxy.example.com:3128",
"ftp": "proxy.example.com",
                })
# Add HTTP Basic/Digest auth username and password for HTTP proxy access.
# (equivalent to using "joe:password@..." form above)
br.add_proxy_password("joe", "password")

# Add HTTP Basic/Digest auth username and password for website access.
br.add_password("http://example.com/protected/", "joe", "password")

# Don't handle HTTP-EQUIV headers (HTTP headers embedded in HTML).
br.set_handle_equiv(False)

# Ignore robots.txt.  Do not do this without thought and consideration.
br.set_handle_robots(False)

# Don't add Referer (sic) header
br.set_handle_referer(False)

# Don't handle Refresh redirections
br.set_handle_refresh(False)

# Don't handle cookies
cj = br.set_cookiejar()

# Supply your own mechanize.CookieJar (NOTE: cookie handling is ON by
# default: no need to do this unless you have some reason to use a
# particular cookiejar)
br.set_cookiejar(cj)

# Log information about HTTP redirects and Refreshes.
br.set_debug_redirects(True)

# Log HTTP response bodies (ie. the HTML, most of the time).
br.set_debug_responses(True)

# Print HTTP headers.
br.set_debug_http(True)

# Sometimes it's useful to process bad headers or bad HTML:
response = br.response()  # this is a copy of response
headers = response.info()  # currently, this is a mimetools.Message
headers["Content-type"] = "text/html; charset=utf-8"
response.set_data(response.get_data().replace("<!---", "<!--"))
br.set_response(response)