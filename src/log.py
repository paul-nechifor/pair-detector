import sys
from datetime import datetime


def log(msg, *args):
    print >>sys.stderr, datetime.utcnow().isoformat(),
    print >>sys.stderr, msg % tuple(args)
