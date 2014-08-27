#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: phone.py

'''
dig.extract.page.backpage
@author: Andrew Philpot
@version 1.0
'''

import sys, os, re, time, datetime
from time import localtime, mktime, gmtime
import simplejson as json
import argparse
from wat.tool.shedhtml import shedHTML
from wat.escort.extract.page import Page
from util import echo, interpretCmdLine, ensureDirectoriesExist
from util import abbrevString, emittable, utf8print
import pprint

VERSION = "1.0"
__version__ = VERSION

# extraction schema is extremely simple
# post(url, market[faa_code], sitekey[e.g., "sanfernandovalley"], statedAge, sitekey, created)
#   text(role, content)
#     phoneNumbers <later>
#   images: image(url)
#   crosslinks: (url1, url2)

AREACODES=[]

class BackpagePage(Page):
    def __init__(self, **kwargs):
        Page.__init__(self, **kwargs)
        self.source = 'backpage'

def valid_area_code(ac):
    # return ensure_area_codes().get(ac,False)
    return AreaCode.lookup(ac)

def valid_phone_number(ph, test_area_code=True):
    m = re.search(r"""^[2-9]\d{2}[2-9]\d{6}$""", ph)
    if m:
        if test_area_code:
            return valid_area_code(ph[0:3])
        else:
            return True
    else:
        return False

def clean_phone_text(text):
    text = text.lower()
    
    # simply remove numeric entities
    text = re.sub(r"""&#\d{1,3};""", "", text, flags=re.I)

    # re.sub(pattern,replacement,string, flags=re.I | re.G)

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

def make_phone_regexp():
    return re.compile(r"""([[{(<]{0,3}[2-9][\W_]{0,3}\d[\W_]{0,3}\d[\W_]{0,6}[2-9][\W_]{0,3}\d[\W_]{0,3}\d[\W_]{0,6}\d[\W_]{0,3}\d[\W_]{0,3}\d[\W_]{0,3}\d)""")

PHONE_REGEXP = make_phone_regexp()

# 3 May 2012
# new strategy: skip finditer, do the indexing ourselves

def genPhones(text):
    text = clean_phone_text(text)
    regex = PHONE_REGEXP
    idx = 0
    m = regex.search(text, idx)
    while m:
        g = m.group(1)
        start = m.start(1)
        end = m.end(1)
        digits = re.sub(r"""\D+""", "", g)
        prefix = text[start-1:start] if start>0 else None
        if digits[0:2] == '82' and prefix == '*':
            # this number overlaps with a *82 sequence
            idx += 2
        elif not valid_area_code(digits[0:3]):
            # probably a price, height, etc.
            idx += 1
        else:
            # seems good
            yield digits
            idx = end
        m = regex.search(text, idx)
            
    
def extractPhoneNumbers(text):
    return [ph for ph in genPhones(text)]

def main(argv=None):
    '''this is called if run from command line'''
    (prog, args) = interpretCmdLine()
    parser = argparse.ArgumentParser(prog, description='Backpage Extractor')
    # parser.add_argument()
    args = parser.parse_args(args)
    
    pageCls = BackpagePage
    lineregex = re.compile(r"""(^.+)\t(.*)""")
    rawText = ""
    for line in sys.stdin:
        # print line
        m = lineregex.match(line) 
        if m:
            url = m.group(1)
            rawText = m.group(2)
            # json object should be a dict
            d = json.loads(rawText)
            if isinstance(d, dict):
                bodyPhones = 
            bodyText = jsonObj
            page = pageCls(url=url,
                                   content=pageStr,
                                   crawlAgent=crawlAgent,
                                   datestamp=int(datestamp))
                    page.process()
                    # print "%s\t%s" % (url, len(pageStr))

# call main() if this is run as standalone
if __name__ == "__main__":
    sys.exit(main())
