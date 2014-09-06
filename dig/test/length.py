#!/usr/bin/env ./dig/bin/python
# -*- coding: utf-8 -*-
# Filename: length.py

# also consider
#!/usr/bin/env python

'''
dig.test.length
@author: Andrew Philpot
@version 1.0
'''

import sys, os, re, time, datetime
from time import localtime, mktime, gmtime
import simplejson as json
import argparse
from dig.pymod.util import interpretCmdLine, ensureDirectoriesExist
# for debug only
# for some reason the utf8print is not found here
# from dig.pymod.util import echo, abbrevString, emittable, utf8print
from dig.pymod.util import echo, abbrevString, emittable

VERSION = "1.0"
__version__ = VERSION
REVISION = "$Revision: 25782 $".replace("$","")

def main(argv=None):
    '''this is called if run from command line'''
    (prog, args) = interpretCmdLine()
    parser = argparse.ArgumentParser(prog, description='Test Length')
    # parser.add_argument()
    args = parser.parse_args(args)
    
    lineregex = re.compile(r"""(^.+)\t(.*)""")
    # specific to first url scheme
    urlregex = re.compile(r"""https://karmadigstorage.blob.core.windows.net/arch/([a-zA-Z0-9]+)/(\d{8})/.*\.backpage\.com/(.*)""")
    payload = ""
    count = 0
    total = 0
    url = ""
    for line in sys.stdin:
        # print line
        m = lineregex.match(line) 
        if m:
            url = m.group(1)
            payload = m.group(2)
            increment = len(str(payload))
            print >> sys.stdout, "%s\t%s" % (url, increment)
            count += 1
            total += increment
    print >> sys.stdout, "%s\ttotal=%s" % (url, total)
    print >> sys.stdout, "%s\tcount=%s" % (url, count)
    print >> sys.stderr, "dig.test.length processed %d records" % count

# call main() if this is run as standalone
if __name__ == "__main__":
    sys.exit(main())
