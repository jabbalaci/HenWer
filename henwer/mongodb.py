#!/usr/bin/env python

"""
Database handler for MongoDB.
"""

import sys
import config as cfg

mdb = None      # mongodb


def process(img):
    """Where img is a myimage instance."""
    if img.asterisk:
        mdb.marked.insert({'md5_hash': img.md5_hash}, safe=True)
    else:
        mdb.marked.remove({'md5_hash': img.md5_hash}, safe=True)
        
def is_md5_registered(md5_hash):
    row = mdb.marked.find_one({'md5_hash': md5_hash})
    return True if row else False

def init():
    """Initialize the DB."""
    global mdb
    
    try:
        conn = Connection(host=cfg.MONGODB_URL, port=cfg.MONGODB_PORT)
    except ConnectionFailure, e:
        print >>sys.stderr, "Could not connect to MongoDB: %s" % e
        sys.exit(1)
        
    mdb = conn[cfg.MONGODB_DB]
    
    mdb.marked.create_index("md5_hash", unique=True)
    
######

if cfg.USE_MONGO:
    from pymongo import Connection
    from pymongo.errors import ConnectionFailure
    init()
