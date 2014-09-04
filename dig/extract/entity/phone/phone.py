#!/usr/bin/env ./dig/bin/python
# -*- coding: utf-8 -*-
# Filename: phone.py

# also consider
#!/usr/bin/env python

'''
dig.extract.entity.phone
@author: Andrew Philpot
@version 1.2
'''

import sys, os, re
import simplejson as json
import argparse
from dig.pymod.util import interpretCmdLine
from pkg_resources import resource_string
# for debug only
from dig.pymod.util import echo

VERSION = "1.2"
__version__ = VERSION

def uniqueStable(iterator):
    """Unique: rmdup
Stable: objects appear in output in order of first appearance in input"""
    seen = set()
    unique = []
    for item in iterator:
        if not item in seen:
            seen.add(item)
            unique.append(item)
    return unique
    
AREACODES = None

def loadAreacodes():
  global AREACODES
  from dig.extract.entity.phone.areacode import AREACODES
  return AREACODES

def ensureAreaCodes():
    global AREACODES
    if not AREACODES:
        loadAreaCodes()
    return AREACODES

class PhoneExtractor(object):

    phoneRegexp = re.compile(r"""([[{(<]{0,3}[2-9][\W_]{0,3}\d[\W_]{0,3}\d[\W_]{0,6}[2-9][\W_]{0,3}\d[\W_]{0,3}\d[\W_]{0,6}\d[\W_]{0,3}\d[\W_]{0,3}\d[\W_]{0,3}\d)""")

    areaCodes = ensureAreaCodes()

    def __init__(self, text):
        self.text = text
        
    @classmethod
    def validAreaCode(cls, ac):
        return cls.areaCodes.get(ac)

    @classmethod
    def validPhoneNumber(cls, ph, testAreaCode=True):
        ph = str(ph)
        m = re.search(r"""^[2-9]\d{2}[2-9]\d{6}$""", ph)
        if m:
            if testAreaCode:
                return cls.validAreaCode(ph[0:3])
            else:
                return True
        else:
            return False

    def cleanPhoneText(self, text):
        text = text.lower()

        # reminder: general re syntax
        # re.sub(pattern,replacement,string, flags=re.I | re.G)

        # first simply remove numeric entities
        # probably irrelevant for dig
        text = re.sub(r"""&#\d{1,3};""", "", text, flags=re.I)
        # misspelled numeral words 
        text = re.sub(r"""th0usand""", "thousand", text, flags=re.I)
        text = re.sub(r"""th1rteen""", "thirteen", text, flags=re.I)
        text = re.sub(r"""f0urteen""", "fourteen", text, flags=re.I)
        text = re.sub(r"""e1ghteen""", "eighteen", text, flags=re.I)
        text = re.sub(r"""n1neteen""", "nineteen", text, flags=re.I)
        text = re.sub(r"""f1fteen""", "fifteen", text, flags=re.I)
        text = re.sub(r"""s1xteen""", "sixteen", text, flags=re.I)
        text = re.sub(r"""th1rty""", "thirty", text, flags=re.I)
        text = re.sub(r"""e1ghty""", "eighty", text, flags=re.I)
        text = re.sub(r"""n1nety""", "ninety", text, flags=re.I)
        text = re.sub(r"""fourty""", "forty", text, flags=re.I)
        text = re.sub(r"""f0urty""", "forty", text, flags=re.I)
        text = re.sub(r"""e1ght""", "eight", text, flags=re.I)
        text = re.sub(r"""f0rty""", "forty", text, flags=re.I)
        text = re.sub(r"""f1fty""", "fifty", text, flags=re.I)
        text = re.sub(r"""s1xty""", "sixty", text, flags=re.I)
        text = re.sub(r"""zer0""", "zero", text, flags=re.I)
        text = re.sub(r"""f0ur""", "four", text, flags=re.I)
        text = re.sub(r"""f1ve""", "five", text, flags=re.I)
        text = re.sub(r"""n1ne""", "nine", text, flags=re.I)
        text = re.sub(r"""0ne""", "one", text, flags=re.I)
        text = re.sub(r"""tw0""", "two", text, flags=re.I)
        text = re.sub(r"""s1x""", "six", text, flags=re.I)
        # mixed compound numeral words
        # consider 7teen, etc.
        text = re.sub(r"""twenty[\\W_]{0,3}1""", "twenty-one", text, flags=re.I)
        text = re.sub(r"""twenty[\\W_]{0,3}2""", "twenty-two", text, flags=re.I)
        text = re.sub(r"""twenty[\\W_]{0,3}3""", "twenty-three", text, flags=re.I)
        text = re.sub(r"""twenty[\\W_]{0,3}4""", "twenty-four", text, flags=re.I)
        text = re.sub(r"""twenty[\\W_]{0,3}5""", "twenty-five", text, flags=re.I)
        text = re.sub(r"""twenty[\\W_]{0,3}6""", "twenty-six", text, flags=re.I)
        text = re.sub(r"""twenty[\\W_]{0,3}7""", "twenty-seven", text, flags=re.I)
        text = re.sub(r"""twenty[\\W_]{0,3}8""", "twenty-eight", text, flags=re.I)
        text = re.sub(r"""twenty[\\W_]{0,3}9""", "twenty-nine", text, flags=re.I)
        text = re.sub(r"""thirty[\\W_]{0,3}1""", "thirty-one", text, flags=re.I)
        text = re.sub(r"""thirty[\\W_]{0,3}2""", "thirty-two", text, flags=re.I)
        text = re.sub(r"""thirty[\\W_]{0,3}3""", "thirty-three", text, flags=re.I)
        text = re.sub(r"""thirty[\\W_]{0,3}4""", "thirty-four", text, flags=re.I)
        text = re.sub(r"""thirty[\\W_]{0,3}5""", "thirty-five", text, flags=re.I)
        text = re.sub(r"""thirty[\\W_]{0,3}6""", "thirty-six", text, flags=re.I)
        text = re.sub(r"""thirty[\\W_]{0,3}7""", "thirty-seven", text, flags=re.I)
        text = re.sub(r"""thirty[\\W_]{0,3}8""", "thirty-eight", text, flags=re.I)
        text = re.sub(r"""thirty[\\W_]{0,3}9""", "thirty-nine", text, flags=re.I)
        text = re.sub(r"""forty[\\W_]{0,3}1""", "forty-one", text, flags=re.I)
        text = re.sub(r"""forty[\\W_]{0,3}2""", "forty-two", text, flags=re.I)
        text = re.sub(r"""forty[\\W_]{0,3}3""", "forty-three", text, flags=re.I)
        text = re.sub(r"""forty[\\W_]{0,3}4""", "forty-four", text, flags=re.I)
        text = re.sub(r"""forty[\\W_]{0,3}5""", "forty-five", text, flags=re.I)
        text = re.sub(r"""forty[\\W_]{0,3}6""", "forty-six", text, flags=re.I)
        text = re.sub(r"""forty[\\W_]{0,3}7""", "forty-seven", text, flags=re.I)
        text = re.sub(r"""forty[\\W_]{0,3}8""", "forty-eight", text, flags=re.I)
        text = re.sub(r"""forty[\\W_]{0,3}9""", "forty-nine", text, flags=re.I)
        text = re.sub(r"""fifty[\\W_]{0,3}1""", "fifty-one", text, flags=re.I)
        text = re.sub(r"""fifty[\\W_]{0,3}2""", "fifty-two", text, flags=re.I)
        text = re.sub(r"""fifty[\\W_]{0,3}3""", "fifty-three", text, flags=re.I)
        text = re.sub(r"""fifty[\\W_]{0,3}4""", "fifty-four", text, flags=re.I)
        text = re.sub(r"""fifty[\\W_]{0,3}5""", "fifty-five", text, flags=re.I)
        text = re.sub(r"""fifty[\\W_]{0,3}6""", "fifty-six", text, flags=re.I)
        text = re.sub(r"""fifty[\\W_]{0,3}7""", "fifty-seven", text, flags=re.I)
        text = re.sub(r"""fifty[\\W_]{0,3}8""", "fifty-eight", text, flags=re.I)
        text = re.sub(r"""fifty[\\W_]{0,3}9""", "fifty-nine", text, flags=re.I)
        text = re.sub(r"""sixty[\\W_]{0,3}1""", "sixty-one", text, flags=re.I)
        text = re.sub(r"""sixty[\\W_]{0,3}2""", "sixty-two", text, flags=re.I)
        text = re.sub(r"""sixty[\\W_]{0,3}3""", "sixty-three", text, flags=re.I)
        text = re.sub(r"""sixty[\\W_]{0,3}4""", "sixty-four", text, flags=re.I)
        text = re.sub(r"""sixty[\\W_]{0,3}5""", "sixty-five", text, flags=re.I)
        text = re.sub(r"""sixty[\\W_]{0,3}6""", "sixty-six", text, flags=re.I)
        text = re.sub(r"""sixty[\\W_]{0,3}7""", "sixty-seven", text, flags=re.I)
        text = re.sub(r"""sixty[\\W_]{0,3}8""", "sixty-eight", text, flags=re.I)
        text = re.sub(r"""sixty[\\W_]{0,3}9""", "sixty-nine", text, flags=re.I)
        text = re.sub(r"""seventy[\\W_]{0,3}1""", "seventy-one", text, flags=re.I)
        text = re.sub(r"""seventy[\\W_]{0,3}2""", "seventy-two", text, flags=re.I)
        text = re.sub(r"""seventy[\\W_]{0,3}3""", "seventy-three", text, flags=re.I)
        text = re.sub(r"""seventy[\\W_]{0,3}4""", "seventy-four", text, flags=re.I)
        text = re.sub(r"""seventy[\\W_]{0,3}5""", "seventy-five", text, flags=re.I)
        text = re.sub(r"""seventy[\\W_]{0,3}6""", "seventy-six", text, flags=re.I)
        text = re.sub(r"""seventy[\\W_]{0,3}7""", "seventy-seven", text, flags=re.I)
        text = re.sub(r"""seventy[\\W_]{0,3}8""", "seventy-eight", text, flags=re.I)
        text = re.sub(r"""seventy[\\W_]{0,3}9""", "seventy-nine", text, flags=re.I)
        text = re.sub(r"""eighty[\\W_]{0,3}1""", "eighty-one", text, flags=re.I)
        text = re.sub(r"""eighty[\\W_]{0,3}2""", "eighty-two", text, flags=re.I)
        text = re.sub(r"""eighty[\\W_]{0,3}3""", "eighty-three", text, flags=re.I)
        text = re.sub(r"""eighty[\\W_]{0,3}4""", "eighty-four", text, flags=re.I)
        text = re.sub(r"""eighty[\\W_]{0,3}5""", "eighty-five", text, flags=re.I)
        text = re.sub(r"""eighty[\\W_]{0,3}6""", "eighty-six", text, flags=re.I)
        text = re.sub(r"""eighty[\\W_]{0,3}7""", "eighty-seven", text, flags=re.I)
        text = re.sub(r"""eighty[\\W_]{0,3}8""", "eighty-eight", text, flags=re.I)
        text = re.sub(r"""eighty[\\W_]{0,3}9""", "eighty-nine", text, flags=re.I)
        text = re.sub(r"""ninety[\\W_]{0,3}1""", "ninety-one", text, flags=re.I)
        text = re.sub(r"""ninety[\\W_]{0,3}2""", "ninety-two", text, flags=re.I)
        text = re.sub(r"""ninety[\\W_]{0,3}3""", "ninety-three", text, flags=re.I)
        text = re.sub(r"""ninety[\\W_]{0,3}4""", "ninety-four", text, flags=re.I)
        text = re.sub(r"""ninety[\\W_]{0,3}5""", "ninety-five", text, flags=re.I)
        text = re.sub(r"""ninety[\\W_]{0,3}6""", "ninety-six", text, flags=re.I)
        text = re.sub(r"""ninety[\\W_]{0,3}7""", "ninety-seven", text, flags=re.I)
        text = re.sub(r"""ninety[\\W_]{0,3}8""", "ninety-eight", text, flags=re.I)
        text = re.sub(r"""ninety[\\W_]{0,3}9""", "ninety-nine", text, flags=re.I)
        # now resolve compound numeral words
        # allow twenty-one, twentyone, twenty_one, twenty one
        text = re.sub(r"""twenty[ _-]?one""", "21", text, flags=re.I)
        text = re.sub(r"""twenty[ _-]?two""", "22", text, flags=re.I)
        text = re.sub(r"""twenty[ _-]?three""", "23", text, flags=re.I)
        text = re.sub(r"""twenty[ _-]?four""", "24", text, flags=re.I)
        text = re.sub(r"""twenty[ _-]?five""", "25", text, flags=re.I)
        text = re.sub(r"""twenty[ _-]?six""", "26", text, flags=re.I)
        text = re.sub(r"""twenty[ _-]?seven""", "27", text, flags=re.I)
        text = re.sub(r"""twenty[ _-]?eight""", "28", text, flags=re.I)
        text = re.sub(r"""twenty[ _-]?nine""", "29", text, flags=re.I)
        text = re.sub(r"""thirty[ _-]?one""", "31", text, flags=re.I)
        text = re.sub(r"""thirty[ _-]?two""", "32", text, flags=re.I)
        text = re.sub(r"""thirty[ _-]?three""", "33", text, flags=re.I)
        text = re.sub(r"""thirty[ _-]?four""", "34", text, flags=re.I)
        text = re.sub(r"""thirty[ _-]?five""", "35", text, flags=re.I)
        text = re.sub(r"""thirty[ _-]?six""", "36", text, flags=re.I)
        text = re.sub(r"""thirty[ _-]?seven""", "37", text, flags=re.I)
        text = re.sub(r"""thirty[ _-]?eight""", "38", text, flags=re.I)
        text = re.sub(r"""thirty[ _-]?nine""", "39", text, flags=re.I)
        text = re.sub(r"""forty[ _-]?one""", "41", text, flags=re.I)
        text = re.sub(r"""forty[ _-]?two""", "42", text, flags=re.I)
        text = re.sub(r"""forty[ _-]?three""", "43", text, flags=re.I)
        text = re.sub(r"""forty[ _-]?four""", "44", text, flags=re.I)
        text = re.sub(r"""forty[ _-]?five""", "45", text, flags=re.I)
        text = re.sub(r"""forty[ _-]?six""", "46", text, flags=re.I)
        text = re.sub(r"""forty[ _-]?seven""", "47", text, flags=re.I)
        text = re.sub(r"""forty[ _-]?eight""", "48", text, flags=re.I)
        text = re.sub(r"""forty[ _-]?nine""", "49", text, flags=re.I)
        text = re.sub(r"""fifty[ _-]?one""", "51", text, flags=re.I)
        text = re.sub(r"""fifty[ _-]?two""", "52", text, flags=re.I)
        text = re.sub(r"""fifty[ _-]?three""", "53", text, flags=re.I)
        text = re.sub(r"""fifty[ _-]?four""", "54", text, flags=re.I)
        text = re.sub(r"""fifty[ _-]?five""", "55", text, flags=re.I)
        text = re.sub(r"""fifty[ _-]?six""", "56", text, flags=re.I)
        text = re.sub(r"""fifty[ _-]?seven""", "57", text, flags=re.I)
        text = re.sub(r"""fifty[ _-]?eight""", "58", text, flags=re.I)
        text = re.sub(r"""fifty[ _-]?nine""", "59", text, flags=re.I)
        text = re.sub(r"""sixty[ _-]?one""", "61", text, flags=re.I)
        text = re.sub(r"""sixty[ _-]?two""", "62", text, flags=re.I)
        text = re.sub(r"""sixty[ _-]?three""", "63", text, flags=re.I)
        text = re.sub(r"""sixty[ _-]?four""", "64", text, flags=re.I)
        text = re.sub(r"""sixty[ _-]?five""", "65", text, flags=re.I)
        text = re.sub(r"""sixty[ _-]?six""", "66", text, flags=re.I)
        text = re.sub(r"""sixty[ _-]?seven""", "67", text, flags=re.I)
        text = re.sub(r"""sixty[ _-]?eight""", "68", text, flags=re.I)
        text = re.sub(r"""sixty[ _-]?nine""", "69", text, flags=re.I)
        text = re.sub(r"""seventy[ _-]?one""", "71", text, flags=re.I)
        text = re.sub(r"""seventy[ _-]?two""", "72", text, flags=re.I)
        text = re.sub(r"""seventy[ _-]?three""", "73", text, flags=re.I)
        text = re.sub(r"""seventy[ _-]?four""", "74", text, flags=re.I)
        text = re.sub(r"""seventy[ _-]?five""", "75", text, flags=re.I)
        text = re.sub(r"""seventy[ _-]?six""", "76", text, flags=re.I)
        text = re.sub(r"""seventy[ _-]?seven""", "77", text, flags=re.I)
        text = re.sub(r"""seventy[ _-]?eight""", "78", text, flags=re.I)
        text = re.sub(r"""seventy[ _-]?nine""", "79", text, flags=re.I)
        text = re.sub(r"""eighty[ _-]?one""", "81", text, flags=re.I)
        text = re.sub(r"""eighty[ _-]?two""", "82", text, flags=re.I)
        text = re.sub(r"""eighty[ _-]?three""", "83", text, flags=re.I)
        text = re.sub(r"""eighty[ _-]?four""", "84", text, flags=re.I)
        text = re.sub(r"""eighty[ _-]?five""", "85", text, flags=re.I)
        text = re.sub(r"""eighty[ _-]?six""", "86", text, flags=re.I)
        text = re.sub(r"""eighty[ _-]?seven""", "87", text, flags=re.I)
        text = re.sub(r"""eighty[ _-]?eight""", "88", text, flags=re.I)
        text = re.sub(r"""eighty[ _-]?nine""", "89", text, flags=re.I)
        text = re.sub(r"""ninety[ _-]?one""", "91", text, flags=re.I)
        text = re.sub(r"""ninety[ _-]?two""", "92", text, flags=re.I)
        text = re.sub(r"""ninety[ _-]?three""", "93", text, flags=re.I)
        text = re.sub(r"""ninety[ _-]?four""", "94", text, flags=re.I)
        text = re.sub(r"""ninety[ _-]?five""", "95", text, flags=re.I)
        text = re.sub(r"""ninety[ _-]?six""", "96", text, flags=re.I)
        text = re.sub(r"""ninety[ _-]?seven""", "97", text, flags=re.I)
        text = re.sub(r"""ninety[ _-]?eight""", "98", text, flags=re.I)
        text = re.sub(r"""ninety[ _-]?nine""", "99", text, flags=re.I)
        # larger units function as suffixes now
        # assume never have three hundred four, three hundred and four
        text = re.sub(r"""hundred""", "00", text, flags=re.I)
        text = re.sub(r"""thousand""", "000", text, flags=re.I)
        # single numeral words now
        # some would have been ambiguous
        text = re.sub(r"""seventeen""", "17", text, flags=re.I)
        text = re.sub(r"""thirteen""", "13", text, flags=re.I)
        text = re.sub(r"""fourteen""", "14", text, flags=re.I)
        text = re.sub(r"""eighteen""", "18", text, flags=re.I)
        text = re.sub(r"""nineteen""", "19", text, flags=re.I)
        text = re.sub(r"""fifteen""", "15", text, flags=re.I)
        text = re.sub(r"""sixteen""", "16", text, flags=re.I)
        text = re.sub(r"""seventy""", "70", text, flags=re.I)
        text = re.sub(r"""eleven""", "11", text, flags=re.I)
        text = re.sub(r"""twelve""", "12", text, flags=re.I)
        text = re.sub(r"""twenty""", "20", text, flags=re.I)
        text = re.sub(r"""thirty""", "30", text, flags=re.I)
        text = re.sub(r"""eighty""", "80", text, flags=re.I)
        text = re.sub(r"""ninety""", "90", text, flags=re.I)
        text = re.sub(r"""three""", "3", text, flags=re.I)
        text = re.sub(r"""seven""", "7", text, flags=re.I)
        text = re.sub(r"""eight""", "8", text, flags=re.I)
        text = re.sub(r"""forty""", "40", text, flags=re.I)
        text = re.sub(r"""fifty""", "50", text, flags=re.I)
        text = re.sub(r"""sixty""", "60", text, flags=re.I)
        text = re.sub(r"""zero""", "0", text, flags=re.I)
        text = re.sub(r"""four""", "4", text, flags=re.I)
        text = re.sub(r"""five""", "5", text, flags=re.I)
        text = re.sub(r"""nine""", "9", text, flags=re.I)
        text = re.sub(r"""one""", "1", text, flags=re.I)
        text = re.sub(r"""two""", "2", text, flags=re.I)
        text = re.sub(r"""six""", "6", text, flags=re.I)
        text = re.sub(r"""ten""", "10", text, flags=re.I)
        # now do letter for digit substitutions
        text = re.sub(r"""oh""", "0", text, flags=re.I)
        text = re.sub(r"""o""", "0", text, flags=re.I)
        text = re.sub(r"""i""", "1", text, flags=re.I)
        text = re.sub(r"""l""", "1", text, flags=re.I)
        return text

    # 3 May 2012
    # new strategy: skip finditer, do the indexing ourselves

    def genPhoneNumbers(self):
        text = self.cleanPhoneText(self.text)
        idx = 0
        m = self.phoneRegexp.search(text, idx)
        while m:
            g = m.group(1)
            start = m.start(1)
            end = m.end(1)
            digits = re.sub(r"""\D+""", "", g)
            prefix = text[start-1:start] if start>0 else None
            if digits[0:2] == '82' and prefix == '*':
                # this number overlaps with a *82 sequence
                idx += 2
            elif not self.validAreaCode(digits[0:3]):
                # probably a price, height, etc.
                idx += 1
            else:
                # seems good
                yield digits
                idx = end
            m = self.phoneRegexp.search(text, idx)
    
    def extractPhoneNumbers(self):
        return uniqueStable(self.genPhoneNumbers())

# jo={"bodyText": {"content": "\n 100% Full Asian \n Petite at 4'11'' and 110lbs \n Sexy eyes with long black hair \n Soft silky skin \n 100% natural and clean \n Independent and discreet \n Pictures are real \n Location: Olympia , Tumwater , Lacey and surrounding areas. \n", "objectType": "Text", "role": "body"}, "cacheUrl": "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/100-asian-hi-im-honey-n-im-super-sweet-25/13538952", "created": "2013-11-28T19:43:00", "crosslinks": [], "images": [], "locationText": {"content": "Olympia, olympia , tumwater , lacey and surroundi", "objectType": "Text", "role": "location"}, "market": "TCM", "objectType": "Post", "sid": "13538952", "sitekey": "olympia", "source": "backpage", "statedAge": 25, "titleText": {"content": "100% Asian. Hi I'm Honey n I'm super sweet. - 25", "objectType": "Text", "role": "title"}, "url": "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/100-asian-hi-im-honey-n-im-super-sweet-25/13538952"}

# testLine = '''https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/bellingham.backpage.com/FemaleEscorts/120-morning-special-dont-miss-this-25/14910841\t"\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n  \r\n  \r\n  \r\n  <!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.01//EN\" \"http://www.w3.org/TR/html4/strict.dtd\">\r\n    <!--[if lte IE 7]> <html class=\"ie7\" lang-\"en-us\"> <![endif]-->  \r\n    <!--[if IE 8]>     <html class=\"ie8\" lang=\"en-us\"> <![endif]-->  \r\n    <!--[if IE 9]>     <html class=\"ie9\" lang=\"en-us\"> <![endif]-->  \r\n    <!--[if !IE]><!--> <html lang=\"en-us\">             <!--<![endif]-->\r\n\r\n    <head>\r\n      <title>$120 Morning Special!! Dont miss this! - bellingham escorts - backpage.com</title>\r\n      <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\r\n      <meta name=\"keywords\" content=\"Bellingham, bell/blaine/outcall, $120 Morning Special!! Dont miss this!\">\r\n      <meta name=\"description\" content=\"Bellingham. bell/blaine/outcall. $120 Morning Special!! Dont miss this! - 25\">\r\n\r\n      \r\n      \r\n        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\r\n      \r\n      \r\n      \r\n      \r\n      <link rel=\"stylesheet\" type=\"text/css\" href=\"http://bellingham.backpage.com/styles/Responsive.css?cb=22\">\r\n\r\n      \r\n      \r\n        <link rel=\"canonical\" href=\"14910841\" />\r\n      \r\n      \r\n            \r\n      <script type=\"text/javascript\" src=\"http://bellingham.backpage.com/scripts/jquery-1.7.2.min.js\"></script>\r\n  \r\n  <script type=\"text/javascript\" src=\"http://bellingham.backpage.com/scripts/global-compiled.js?3\"></script>\r\n    </head>\r\n\r\n    <body id=\"ViewAd\">\r\n  \r\n  \r\n  \r\n  \r\n\r\n\r\n  <!-- Google Tag Manager -->\r\n  <script>bpDataLayer=[];</script>\r\n  <noscript><iframe src=\"http://www.googletagmanager.com/ns.html?id=GTM-5KCSP8\"\r\n  height=\"0\" width=\"0\" style=\"display:none;visibility:hidden\"></iframe></noscript>\r\n  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\r\n  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],\r\n  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\r\n  '//www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\r\n  })(window,document,'script','bpDataLayer','GTM-5KCSP8');</script>\r\n  <!-- End Google Tag Manager -->\r\n\r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n    <div id=\"tlHeader\">\r\n    \r\n      \r\n      \r\n\r\n      <div id=\"logo\"><a href=\"http://bellingham.backpage.com/\" style=\"background-image:url(http://www.backpage.com/images/bp_logo_mobile.png);\">bellingham.backpage.com</a></div>\r\n      \r\n      \r\n      \r\n        <div id=\"postAdButton\">\r\n          <form name=\"formPost\" action=\"http://posting.bellingham.backpage.com/online/classifieds/PostAdPPI.html/bli/bellingham.backpage.com/\" method=\"get\">\r\n      <input type=\"submit\" value=\"Post an Ad\" class=\"button\" id=\"postAdButton\">\r\n      <input type=\"hidden\" name=\"section\" value=\"4381\">\r\n      <input type=\"hidden\" name=\"category\" value=\"4443\">\r\n      <input type=\"hidden\" name=\"u\" value=\"bli\">\r\n      <input type=\"hidden\" name=\"serverName\" value=\"bellingham.backpage.com\">\r\n    </form>\r\n        </div><!-- #postAdButton -->\r\n\r\n        \r\n      \r\n\r\n      <div id=\"community\">\r\n        \r\n          <span class=\"city\">bellingham,\u00a0wa</span>&nbsp;<span class=\"comm\">free&nbsp;classifieds</span>\r\n        \r\n      </div><!-- #community -->\r\n\r\n      \r\n      \r\n    </div><!-- #tlHeader -->\r\n  \r\n\r\n  <div id=\"pageBackground\" style=\"clear:both;\">\r\n\r\n  \r\n    <div id=\"cookieCrumb\">\r\n      <a href=\"http://bellingham.backpage.com/\">backpage.com</a> &gt; <a href=\"http://bellingham.backpage.com/adult/\">bellingham adult entertainment</a> &gt; <a href=\"../index.html\">bellingham escorts</a>\r\n    </div>\r\n    \r\n    \r\n    <div class=\"mainBody\">\r\n\r\n  \r\n\r\n  \r\n \r\n  \r\n        \r\n    \r\n\r\n    \r\n    <br>\r\n    <div id=\"postingTitle\">\r\n    \r\n      <a style=\"float:right;clear:right;\" href=\"http://posting.bellingham.backpage.com/online/classifieds/ReportAd?oid=14910841\">Report Ad</a>\r\n    \r\n    \r\n      <a class=\"h1link\" href=\"javascript:void;\"><h1>$120 Morning Special!! Dont miss this! - 25</h1></a>\r\n    \r\n  </div>\r\n\r\n  <div class=\"adInfo\">\r\n    Posted: \r\n    Wednesday, December 18, 2013 10:17 AM\r\n  </div>\r\n  \r\n    <hr noshade>\r\n  \r\n  \r\n  \r\n    \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n\r\n  \r\n  \r\n  \r\n\r\n\r\n  \r\n\r\n  \r\n    \r\n      <p class=\"replyDisplay\">\r\n        <b>Reply</b>:&nbsp;<a href=\"http://posting.bellingham.backpage.com/FemaleEscorts/classifieds/Reply?oid=14910841\">click here</a>\r\n      </p>\r\n    \r\n  \r\n\r\n\r\n  \r\n\r\n  \r\n\r\n\r\n  \r\n\r\n  \r\n\r\n  \r\n    <style>\r\n    <!-- \r\n      #viewAdPhotoLayout {\r\n        float:right;\r\n        margin:0 0 1em 1em;\r\n        padding:0;\r\n      }\r\n        #viewAdPhotoLayout li {\r\n          //display:inline-block;\r\n          list-style-type:none;\r\n          margin:0;\r\n          padding:0.75em;\r\n          background:#eee;\r\n          text-align:center;\r\n          overflow:hidden;\r\n          -webkit-column-break-inside: avoid;\r\n          -moz-column-break-inside: avoid; \r\n          -ms-column-break-inside: avoid; \r\n          break-inside: avoid; \r\n          \r\n        }\r\n          #viewAdPhotoLayout img {\r\n            margin-bottom:0.25em;\r\n          }\r\n          #viewAdPhotoLayout li a {\r\n            color:#000;\r\n          }\r\n    // -->\r\n    </style>\r\n    <!--[if gt IE 9]> -->\r\n    <style>\r\n    <!-- \r\n      #viewAdPhotoLayout.fivePlus {\r\n        width:465px;\r\n        -moz-column-count:2;\r\n        -webkit-column-count:2;\r\n        column-count:2;\r\n        -moz-column-gap:1.5em;\r\n        -webkit-column-gap:1.5em;\r\n        column-gap:1.5em;\r\n        column-fill: auto;\r\n      }\r\n      #viewAdPhotoLayout.ninePlus {\r\n        width:708px;\r\n        -moz-column-count:3;\r\n        -webkit-column-count:3;\r\n        column-count:3;\r\n        -moz-column-gap:1.5em;\r\n        -webkit-column-gap:1.5em;\r\n        column-gap:1.5em;\r\n        column-fill: auto;\r\n      }\r\n    // -->\r\n    </style>\r\n    <!-- <![endif]-->\r\n\r\n    \r\n    \r\n    <ul id=\"viewAdPhotoLayout\" class=\"fivePlus\">\r\n      \r\n        \r\n          \r\n            <li><img src=\"../../../images1.backpage.com/imager/u/medium/106356692/GetAttachment-14.jpg\" width=\"96\" height=\"158\" alt=\"$120 Morning Special!! Dont miss this! - 25\" title=\"$120 Morning Special!! Dont miss this! - 25\" border=\"0\"></li>\r\n          \r\n        \r\n          \r\n            <li><img src=\"../../../images3.backpage.com/imager/u/medium/106356694/GetAttachment-9.jpg\" width=\"107\" height=\"158\" alt=\"$120 Morning Special!! Dont miss this! - 25\" title=\"$120 Morning Special!! Dont miss this! - 25\" border=\"0\"></li>\r\n          \r\n        \r\n          \r\n            <li><img src=\"../../../images1.backpage.com/imager/u/medium/106356695/GetAttachment-11.jpg\" width=\"128\" height=\"159\" alt=\"$120 Morning Special!! Dont miss this! - 25\" title=\"$120 Morning Special!! Dont miss this! - 25\" border=\"0\"></li>\r\n          \r\n        \r\n          \r\n            <li><img src=\"../../../images2.backpage.com/imager/u/medium/106356697/GetAttachment-3.jpg\" width=\"127\" height=\"159\" alt=\"$120 Morning Special!! Dont miss this! - 25\" title=\"$120 Morning Special!! Dont miss this! - 25\" border=\"0\"></li>\r\n          \r\n        \r\n          \r\n            <li><img src=\"../../../images2.backpage.com/imager/u/medium/106356699/GetAttachment-4.jpg\" width=\"127\" height=\"159\" alt=\"$120 Morning Special!! Dont miss this! - 25\" title=\"$120 Morning Special!! Dont miss this! - 25\" border=\"0\"></li>\r\n          \r\n        \r\n          \r\n            <li><img src=\"../../../images3.backpage.com/imager/u/medium/106356700/GetAttachment-1.jpg\" width=\"127\" height=\"159\" alt=\"$120 Morning Special!! Dont miss this! - 25\" title=\"$120 Morning Special!! Dont miss this! - 25\" border=\"0\"></li>\r\n          \r\n        \r\n          \r\n            <li><img src=\"../../../images1.backpage.com/imager/u/medium/106356701/GetAttachment-7.jpg\" width=\"119\" height=\"159\" alt=\"$120 Morning Special!! Dont miss this! - 25\" title=\"$120 Morning Special!! Dont miss this! - 25\" border=\"0\"></li>\r\n          \r\n        \r\n          \r\n            <li><img src=\"../../../images2.backpage.com/imager/u/medium/106356702/GetAttachment-20.jpg\" width=\"119\" height=\"159\" alt=\"$120 Morning Special!! Dont miss this! - 25\" title=\"$120 Morning Special!! Dont miss this! - 25\" border=\"0\"></li>\r\n          \r\n        \r\n      \r\n    </ul><!-- #viewAdPhotoLayout -->\r\n  \r\n\r\n  <div class=\"posting\">\r\n    <div class=\"postingBody\">\r\n      \r\n        \r\n        \r\n          Hello gentlemen I'm back in town and for those of you who know me know I'm great at what I do!!.. for those of you who don't know me then ley me tell I'm a sexxy petite Burnett with a cuddly personality that you can't resist! !.. my pics are 100% real so if u like what you see call me now and set up sum time with the best!: 702-539-3220. From 8am-noon I'm having a $120 morningbspecial!!\r\n        \r\n      \r\n    </div>\r\n\r\n      \r\n      <p class=\"metaInfoDisplay\">Poster's age: 25<br></p>\r\n    \r\n\r\n    \r\n\r\n    \r\n      <div style=\"padding-left:2em;\">\r\n        &bull; Location: \r\n        \r\n          Bellingham, bell/blaine/outcall\r\n        \r\n      </div>\r\n    \r\n\r\n\r\n    \r\n      \r\n\r\n      \r\n      \r\n      <div style=\"padding-left:2em;\"><br />&bull; Post ID: 14910841 bellingham</div>\r\n\r\n      \r\n        <div id=\"OtherAdsByThisUser\" data-oid=\"14910841\">\r\n          <noscript>\r\n            \r\n          </noscript>\r\n        </div>\r\n        <script type=\"text/javascript\">\r\n          <!--\r\n          jQuery(\"#OtherAdsByThisUser\").loadOtherAdsByThisUser();\r\n          // -->\r\n        </script>\r\n      \r\n    \r\n\r\n\r\n    \r\n      <div class=\"helperLinks\" style=\"margin:2em 0;\">\r\n        <span style=\"font-weight:bold;\"><a href=\"http://posting.bellingham.backpage.com/FemaleEscorts/classifieds/EmailAd?oid=14910841\">Email this ad</a></span><br>\r\n      </div>\r\n    \r\n\r\n    \r\n\r\n  </div> <!-- .posting -->\r\n  \r\n\r\n  \r\n\r\n  \r\n  \r\n  \r\n  \r\n\r\n  \r\n  \r\n  <div style=\"clear:both;\"></div>\r\n    </div>\r\n    <!-- .mainBody -->\r\n  \r\n  \r\n  \r\n  \r\n    <script type=\"text/javascript\">\r\n    <!--\r\n      setCookie(\"site\",\"bellingham.backpage.com\",30,\"backpage.com\");\r\n    // -->\r\n    </script>\r\n  \r\n\r\n  <div id=\"tlFooter\">\r\n    <div class=\"footerText\">\r\n      \r\n        <a href=\"https://my.backpage.com/\">Account Login</a> |\r\n      \r\n\r\n      \r\n        <a href=\"http://www.backpage.com/classifieds/affiliates/index\">Affiliate Program</a> |\r\n        <a href=\"http://www.backpage.com/classifieds/affiliates/PromoteUs\">Promote Us</a>  |\r\n      \r\n  \r\n      \r\n\r\n      <a href=\"http://bellingham.backpage.com/online/Help\">Help</a> |\r\n      <a href=\"http://bellingham.backpage.com/online/PrivacyPolicy\">Privacy Policy</a> |\r\n      <a href=\"http://bellingham.backpage.com/online/TermsOfUse\">Terms of Use</a> |\r\n      <a href=\"http://bellingham.backpage.com/online/UserSafety\">User Safety</a> |\r\n\r\n      \r\n      \r\n      \r\n        <a href=\"http://bellingham.backpage.com/classifieds/AllCities\">backpage.com</a> \r\n      \r\n\r\n      &nbsp;&copy;&nbsp;Copyright&nbsp;2014\r\n    </div><!-- .footerText -->\r\n\r\n    <div class=\"footerDisclaimer\">\r\n      bellingham.backpage.com is an interactive computer service that enables access by multiple users and should not be treated as the publisher or speaker of any information provided by another information content provider.\r\n    </div><!-- .footerDisclaimer -->\r\n  </div><!-- #tlFooter -->\r\n\r\n  </div><!-- #pageBackground -->\r\n  \r\n  \r\n\r\n  \r\n    </body>\r\n    </html>\r\n  \r\n\r\n'''

def main(argv=None):
    '''this is called if run from command line'''
    (prog, args) = interpretCmdLine()
    parser = argparse.ArgumentParser(prog, description='Phone Number Extractor')
    # parser.add_argument()
    args = parser.parse_args(args)
    
    lineregex = re.compile(r"""(^.+)\t(.*)""")
    rawText = ""
    for line in sys.stdin:
        # print line
        m = lineregex.match(line) 
        if m:
            url = m.group(1)
            rawText = m.group(2)
            post = json.loads(rawText)
            if isinstance(post, dict):
                allPhoneNumbers = []

                titleText = post.get('titleText')
                if titleText and titleText.get('content'):
                    extr = PhoneExtractor(titleText['content'])
                    phoneNumbers = extr.extractPhoneNumbers()
                    # store locally with the specific text
                    titleText['phoneNumbers'] = phoneNumbers
                    allPhoneNumbers.extend(phoneNumbers)

                locationText = post.get('locationText')
                if locationText and locationText.get('content'):
                    extr = PhoneExtractor(locationText['content'])
                    phoneNumbers = extr.extractPhoneNumbers()
                    # store locally with the specific text
                    locationText['phoneNumbers'] = phoneNumbers
                    allPhoneNumbers.extend(phoneNumbers)

                bodyText = post.get('bodyText')
                if bodyText and bodyText.get('content'):
                    extr = PhoneExtractor(bodyText['content'])
                    phoneNumbers = extr.extractPhoneNumbers()
                    # store locally with the specific text
                    bodyText['phoneNumbers'] = phoneNumbers
                    allPhoneNumbers.extend(phoneNumbers)
            
                post['phoneNumbers'] = uniqueStable(allPhoneNumbers)

            js = json.dumps(post, sort_keys=True, indent=None)
            print >> sys.stdout, "%s\t%s" % (url, js)

# call main() if this is run as standalone
if __name__ == "__main__":
    sys.exit(main())
