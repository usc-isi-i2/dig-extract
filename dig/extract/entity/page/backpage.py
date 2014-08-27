#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: extract.py

'''
wat.escort.extract.backpage
@author: Andrew Philpot
@version 4.2
'''

import sys, os, re, time, datetime
from time import localtime, mktime, gmtime
from bs4 import BeautifulSoup as bs
from wat.escort.markets import MARKETS
import simplejson as json
import argparse
from wat.tool.shedhtml import shedHTML
from wat.escort.extract.page import Page
from util import echo, interpretCmdLine, ensureDirectoriesExist
from util import abbrevString, emittable, utf8print
import pprint

VERSION = "4.2"
__version__ = VERSION
REVISION = "$Revision: 25782 $".replace("$","")

# extraction schema is extremely simple
# post(url, market[faa_code], sitekey[e.g., "sanfernandovalley"], statedAge, sitekey, created)
#   text(role, content)
#     phoneNumbers <later>
#   images: image(url)
#   crosslinks: (url1, url2)

class BackpagePage(Page):
    def __init__(self, **kwargs):
        Page.__init__(self, **kwargs)
        self.source = 'backpage'

    def prep(self):
        self.soup = bs(self.content)

    def extractSid(self):
        link = self.soup.find('link', {"rel": "canonical"})
        if link:
            return link.get('href')
        return None

    def extractSitekey(self):
        div = self.soup.find('div', {"id": "logo"})
        if div:
            for a in div.find_all('a'):
                content = a['href']
                m = re.search(r"""http://(.*).backpage.com""", content, re.I | re.S)
                if m:
                    return m.group(1)
        return None

    def deduceMarket(self, sitekey):
        for (faa_code, market) in MARKETS.iteritems():
            websites = market.get('websites') or []
            for website in websites:
                if (website.get('application') == 'escort' 
                    and website.get('source') == 'backpage'
                    and website.get('sitekey') == sitekey):
                    return faa_code
        return None

    def extractStatedAge(self, default=0):
        p = self.soup.find('p', {'class': "metaInfoDisplay"})
        if p:
            content = p.contents[0]
            if content:
                m = re.search(r"""Poster's age: (\d+)""", content, re.I | re.S)
                return (m and int(m.group(1)))
        return default

    def extractCreated(self):
        """Unfortunately, this is BP-specific"""
        div = self.soup.find('div', {"class": "adInfo"})
        if div:
            content = div.contents[0]
            if content:
                m = re.search(r"""Posted:(.+)\s*$""", content, re.I | re.S)
                raw = m.group(1).strip() if m else None
                parsed = raw and time.strptime(raw, "%A, %B %d, %Y %I:%M %p")
                fmt = parsed and time.strftime("%Y-%m-%d %H:%M:%S", parsed)
                return datetime.datetime.fromtimestamp(mktime(time.strptime(fmt,"%Y-%m-%d %H:%M:%S")))
        return datetime.datetime.fromtimestamp(mktime(gmtime(0)))

    def extractTitleText(self):
        h1 = self.soup.find('h1')
        if h1:
            content = h1.contents[0]
            if content:
                return content.strip()
        return None
       
    def extractLocationText(self):
        for div in self.soup.find_all('div', {"style": "padding-left:2em;"}):
            content = div.contents[0]
            try:
                m = re.search(r"""Location:\s*(.*?)\s*$""", content, re.I | re.S)
                if m:
                    return m.group(1).strip()
            except:
                pass
        return None

    def extractBodyHtml(self):
        div = self.soup.find('div', {"class": "postingBody"})
        if div:
            return div
        return None

    def extractBodyText(self):
        html = self.cache.get('bodyHtml') or self.extractBodyHtml()
        if html:
            return html.get_text()
        return None

    def extractImageRefs(self):
        imageRefs = list()
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
        return imageRefs

    def extractCrosslinks(self):
        # untested
        crosslinks = []
        div = self.soup.find('div', {"id": "OtherAdsByThisUser"})
        if div:
            for a in div.find_all('a'):
                sibling = a.href
                # reject ../index.html and 
                # anything outside the FemaleEscorts category ??
                # if ("FemaleEscorts" in sibling or (sibling[0:2] == ".." and sibling != "../index.html")):
                if (sibling and sibling[0:2] == ".." and sibling != "../index.html"):
                    crosslinks.append((self.url, sibling))
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
    for line in sys.stdin:
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
                    # print "%s\t%s" % (url, len(pageStr))

# call main() if this is run as standalone
if __name__ == "__main__":
    sys.exit(main())
