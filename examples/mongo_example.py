#!/usr/bin/env python
from pymongo import *


def insert_Message(message):
    client = MongoClient(u'mongodb://localhost:27017/')

    db = client[u"local"]
    collection = db[u'Bookmarks']

    collection.insert_one(message)

if __name__ == u"__main__":
    pass