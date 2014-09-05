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
from bs4 import BeautifulSoup as bs
import simplejson as json
import argparse
from dig.extract.page.page import Page
from dig.pymod.util import interpretCmdLine, ensureDirectoriesExist
from pkg_resources import resource_string, resource_exists
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
    
    pageCls = BackpagePage
    lineregex = re.compile(r"""(^.+)\t(.*)""")
    # specific to first url scheme
    urlregex = re.compile(r"""https://karmadigstorage.blob.core.windows.net/arch/([a-zA-Z0-9]+)/(\d{8})/.*\.backpage\.com/(.*)""")
    payload = ""
    count = 0
    total = 0
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
            

            urlMatch = urlregex.match(url)
            if urlMatch:
                crawlAgent = urlMatch.group(1)
                datestamp = urlMatch.group(2)
                tail = urlMatch.group(3)
                if "index.html" in tail:
                    pass
                else:
                    pageStr = json.loads(payload)
                    page = pageCls(url=url,
                                   content=pageStr,
                                   crawlAgent=crawlAgent,
                                   datestamp=int(datestamp))
                    page.process()
                    processed += 1
                    # print "%s\t%s" % (url, len(pageStr))
    print >> sys.stderr, "dig.extract.page.backpage processed %d records" % processed

# call main() if this is run as standalone
if __name__ == "__main__":
    sys.exit(main())
