#!/usr/bin/env python
import re
import mechanize

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(DEBUG)

br = mechanize.Browser()
response = br.open("http://playground.arduino.cc/CommonTopics/PullUpDownResistor")

logger.debug("{}".format(response.read()))

pass
