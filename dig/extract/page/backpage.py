#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: backpage.py

# also consider
#!/usr/bin/env python

'''
dig.extract.page.backpage
@author: Andrew Philpot
@version 4.7
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

VERSION = "4.7"
__version__ = VERSION
REVISION = "$Revision: 25782 $".replace("$","")

# extraction schema is extremely simple
# post(url, market[faa_code], sitekey[e.g., "sanfernandovalley"], statedAge, sitekey, created)
#   text(role, content)
#     phoneNumbers <later>
#   images: image(url)
#   crosslinks: (url1, url2)

MARKETS = None

def loadMarkets():
    global MARKETS
    from dig.extract.page.market import MARKETS
    return MARKETS

def ensureMarkets():
    global MARKETS
    if not MARKETS:
        loadMarkets()
    print >> sys.stderr, "There are %d markets" % len(MARKETS)
    return MARKETS

class BackpagePage(Page):

    markets = ensureMarkets()

    def __init__(self, **kwargs):
        Page.__init__(self, **kwargs)
        self.source = 'backpage'

    def prep(self):
        self.soup = bs(self.content)

    def extractSid(self):
        default = None
        try:
            link = self.soup.find('link', {"rel": "canonical"})
            return link.get('href')
        except:
            pass
        return default

    def extractSitekey(self):
        default = None
        try:
            div = self.soup.find('div', {"id": "logo"})
            for a in div.find_all('a'):
                content = a['href']
                m = re.search(r"""http://(.*).backpage.com""", content, re.I | re.S)
                if m:
                    return m.group(1)
        except:
            pass
        return default

    def deduceMarket(self, sitekey):
        default = None
        try:
            for (faa_code, market) in self.markets.iteritems():
                websites = market.get('websites') or []
                for website in websites:
                    if (website.get('application') == 'escort' 
                        and website.get('source') == 'backpage'
                        and website.get('sitekey') == sitekey):
                        return faa_code
        except:
            pass
        return default

    def extractStatedAge(self, default=0):
        try:
            p = self.soup.find('p', {'class': "metaInfoDisplay"})
            content = p.contents[0]
            m = re.search(r"""Poster's age: (\d+)""", content, re.I | re.S)
            return (m and int(m.group(1)))
        except:
            return default
        return default

    def extractCreated(self):
        """Unfortunately, this is BP-specific"""
        default = datetime.datetime.fromtimestamp(mktime(gmtime(0)))
        try:
            div = self.soup.find('div', {"class": "adInfo"})
            content = div.contents[0]
            m = re.search(r"""Posted:(.+)\s*$""", content, re.I | re.S)
            raw = m.group(1).strip() if m else None
            parsed = raw and time.strptime(raw, "%A, %B %d, %Y %I:%M %p")
            fmt = parsed and time.strftime("%Y-%m-%d %H:%M:%S", parsed)
            return datetime.datetime.fromtimestamp(mktime(time.strptime(fmt,"%Y-%m-%d %H:%M:%S")))
        except:
            pass
        return default

    def extractTitleText(self):
        default = None
        try:
            h1 = self.soup.find('h1')
            content = h1.contents[0]
            return content.strip()
        except:
            pass
        return default
       
    def extractLocationText(self):
        default = None
        try:
            for div in self.soup.find_all('div', {"style": "padding-left:2em;"}):
                content = div.contents[0]
                try:
                    m = re.search(r"""Location:\s*(.*?)\s*$""", content, re.I | re.S)
                    if m:
                        return m.group(1).strip()
                except:
                    pass
        except:
            pass
        return default

    def extractBodyHtml(self):
        default = None
        try:
            div = self.soup.find('div', {"class": "postingBody"})
            if div:
                return div
        except:
            pass
        return default

    def extractBodyText(self):
        default = None
        try:
            html = self.cache.get('bodyHtml') or self.extractBodyHtml()
            return html.get_text()
        except:
            pass
        return None

    def extractImageRefs(self):
        imageRefs = list()
        try:
            ul = self.soup.find('ul', {"id": "viewAdPhotoLayout"})
            if ul:
                for img in ul.find_all('img'):
                    src = img.get('src')
                    if src:
                        m = re.search(r"""(images\d+.backpage.com/imager/u/[^ "]+(?:.jpg|.gif|.png|.jpeg)+)""",
                                      src,
                                      re.I | re.S)
                        if m:
                            # not contextualized to either studio or the real world
                            imageRefs.append(m.group(1))
        except:
            pass
        return imageRefs

    def extractCrosslinks(self):
        # untested
        crosslinks = []
        try:
            div = self.soup.find('div', {"id": "OtherAdsByThisUser"})
            if div:
                for a in div.find_all('a'):
                    sibling = a.href
                    # reject ../index.html and 
                    # anything outside the FemaleEscorts category ??
                    # if ("FemaleEscorts" in sibling or (sibling[0:2] == ".." and sibling != "../index.html")):
                    if (sibling and sibling[0:2] == ".." and sibling != "../index.html"):
                        crosslinks.append((self.url, sibling))
        except:
            pass
        return crosslinks

    def extract(self):
        self.cache = {}
        self.cache['sid'] = self.extractSid()
        self.cache['sitekey'] = self.extractSitekey()
        self.cache['market'] = self.deduceMarket(self.cache['sitekey'])
        self.cache['statedAge'] = self.extractStatedAge()
        self.cache['created'] = self.extractCreated()
        self.cache['titleText'] = self.extractTitleText()
        self.cache['locationText'] = self.extractLocationText()
        self.cache['bodyHtml'] = self.extractBodyHtml()
        self.cache['bodyText'] = self.extractBodyText()
        self.cache['imageRefs'] = self.extractImageRefs()
        self.cache['crosslinks'] = self.extractCrosslinks()

    def process(self):
        self.prep()
        self.extract()
        self.emit()

    def serializationPath(self, pagePathnameOrUrl):
        """To which json path should this data be written?"""
        serPath = pagePathnameOrUrl + "__srlz.json"
        ensureDirectoriesExist(serPath)
        return serPath

    def emit(self):
        js = json.dumps(self.postJson(), sort_keys=True, indent=None)
        # serPath = self.serializationPath(self.url)
        serPath = self.url
        outputStream = sys.stdout
        print >> outputStream, "%s\t%s" % (serPath, js)

def main(argv=None):
    '''this is called if run from command line'''
    (prog, args) = interpretCmdLine()
    parser = argparse.ArgumentParser(prog, description='Backpage Extractor')
    # parser.add_argument()
    args = parser.parse_args(args)
    
    pageCls = BackpagePage
    lineregex = re.compile(r"""(^.+)\t(.*)""")
    # specific to first url scheme
    urlregex = re.compile(r"""https://karmadigstorage.blob.core.windows.net/arch/([a-zA-Z0-9]+)/(\d{8})/.*\.backpage\.com/(.*)""")
    rawText = ""
    processed = 0
    url = None
    for line in sys.stdin:
        try:
            # print line
            m = lineregex.match(line) 
            if m:
                url = m.group(1)
                rawText = m.group(2)
                urlMatch = urlregex.match(url)
                if urlMatch:
                    crawlAgent = urlMatch.group(1)
                    datestamp = urlMatch.group(2)
                    tail = urlMatch.group(3)
                    if "index.html" in tail:
                        pass
                    else:
                        pageStr = json.loads(rawText)
                        page = pageCls(url=url,
                                       content=pageStr,
                                       crawlAgent=crawlAgent,
                                       datestamp=int(datestamp))
                        page.process()
                        processed += 1
                        # print "%s\t%s" % (url, len(pageStr))
        except Exception as e:
            print >> sys.stderr, "dig.extract.page.backpage Exception [%s].  Last url was [%s]" % (str(e), url)
    print >> sys.stderr, "dig.extract.page.backpage processed %d records" % processed

# call main() if this is run as standalone
if __name__ == "__main__":
    sys.exit(main())
