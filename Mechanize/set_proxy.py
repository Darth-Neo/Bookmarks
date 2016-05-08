import mechanize

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


if __name__ == u"__main__":
    # Browser
    br = mechanize.Browser()

    # Proxy and user/password
    br.set_proxies({u"http": u"joe:password@myproxy.example.com:3128"})

    # Proxy
    br.set_proxies({u"http": u"myproxy.example.com:3128"})
    # Proxy password
    br.add_proxy_password(u"joe", u"password")
