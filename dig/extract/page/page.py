#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: page.py

'''
dig.extract.page.page
@author: Andrew Philpot
@version 4.0
'''

from dig.pymod.util import echo

# schema is
# post(url, market[faa_code], sitekey[e.g., "sanfernandovalley"], age, sitekey, created)
#   text(role, content)
#     phoneNumbers <later>
#   images: image(url)
#   crosslinks: (url1, url2)

class Page(object):
    def __init__(self, url=None, content=None, crawlAgent=None, datestamp=None):
        self.url = url
        self.content = content
        self.crawlAgent = crawlAgent
        self.datestamp = datestamp
        self.source = None
        self.cache = {}

    def postJson(self):
        """self here is page"""
        return {# "_className": "wat.escort.models.Post",
                "objectType": "Post",
                "market": self.cache['market'],
                "source": self.source,
                "sid": self.cache['sid'],
                "sitekey": self.cache['sitekey'],
                "statedAge": self.cache['statedAge'],
                "url": self.url,
                "cacheUrl": self.deriveCacheUrl(self.url),

                "bodyText": self.bodyTextJson(),
                "locationText": self.locationTextJson(),
                "titleText": self.titleTextJson(),
                "created": self.cache['created'].isoformat(),
                "images": [self.imageJson(im) for im in self.cache['imageRefs']],
                "crosslinks": self.cache['crosslinks']
                }

    # method bodyTextJson()
    def bodyTextJson(self):
        """self here is page"""
        return {# "_className": fullyQualifiedName(self),
                "objectType": "Text",
                "content": self.cache['bodyText'],
                "role": "body"}

    # method locationTextJson()
    def locationTextJson(self):
        """self here is page"""
        return {# "_className": fullyQualifiedName(self),
                "objectType": "Text",
                "content": self.cache['locationText'],
                "role": "location"}

    # method titleTextJson()
    def titleTextJson(self):
        """self here is page"""
        return {# "_className": fullyQualifiedName(self),
                "objectType": "Text",
                "content": self.cache['titleText'],
                "role": "title"}

    def imageUrl(self, urlFragment):
        return urlFragment

    def deriveCacheUrl(self, wildUrl):
        """stub/protocol: need not exist, dependent on WAT processing history"""
        if wildUrl.startswith('http'):
            return wildUrl
        else:
            return "http://studio.isi.edu/arch/data/escort/%s/" % str(self.datestamp) + wildUrl

    # method imageJson(imagePathname)
    def imageJson(self, imagePathname):
        """self here is page"""
        return {# "_className": fullyQualifiedName(self),
                "objectType": "Image",
                # "hashSignature": imageFileToHashSignature(imagePathname),
                "url": self.imageUrl(imagePathname),
                "cacheUrl": self.deriveCacheUrl(self.imageUrl(imagePathname))}

    def crosslinksJson(self, pairs):
        postUrl = self.cache['url']
        links = []
        for (xlFrom, xlTo) in pairs:
            if xlFrom == postUrl:
                links.append(self.crosslinkJson((xlFrom, xlTo)))
        return links

    # method crosslinkJson(pair)
    # input: pair of uris
    def crosslinkJson(self, pair):
        """self here is page"""
        return {# "_className": fullyQualifiedName(self),
                "objectType": "Crosslink",

                # "pathname1": pair[0],
                # artifact of db mat
                # "post1_id": self.post1_id,
                "url1": pair[0],
                # "pathname2": pair[1],
                # artifact of db mat
                # "post2_id": self.post2_id,
                "url2": pair[1]}

    # method phoneNumberJson(content)
    def phoneNumberJson(self, content):
        """self here is page"""
        (root, app, stamp, path) = deconstructPathname(content, self.root)
        return {# "_className": fullyQualifiedName(self),
                "objectType": "PhoneNumber",
                "content": str(content)}
