#!/usr/bin/env ./dig/bin/python
# -*- coding: utf-8 -*-
# Filename: patscan.py

# also consider
#!/usr/bin/env python

'''
dig.extract.entity.classifier.patscan
@author: Andrew Philpot
@version 0.0.1
'''

import sys
import os
import site
import argparse
import re
import simplejson as json
from collections import defaultdict
from itertools import izip, chain, izip_longest

# these two come fom $PYTHONPATH containing directory pymod
from cstokensearcher import CaseSensitiveTokenSearcher as TokenSearcher
from util import interpretCmdLine
# for debug only
from util import echo, info

VERSION = '0.0.1'
__version__ = VERSION

# FROM KELLY CORBALLY
# Young
# New
# Tight
# In town for a limited time/just visiting
# No black males
# Older men only (gives an age range, etc)
# User has multiple associated ads, especially linked to other girls
# Associated with other ads that have a different age posted (by user or phone number)
# Two or three girl special
# Ask about my friend
# Posted in multiple cities
# Differing area codes in an ad
# Age listed on post
# Looks young (body or face)
# No face shot, not looking at camera, face blurred
# Looks like stock photos pulled from the internet or other ads
# More clothed
# Multiple victims (faces) in the photos
# Incalls only (helpful for juveniles, also helpful for conducting operations as teams may only be set up for one or the other)

byIndic = dict()
byCategory = defaultdict(lambda: list())
byFamily = dict()

def isSequence(obj):
    '''Ignores the fact that str/unicode/buffer are sequences.  That's not the kind of sequence I care about in this context'''
    return isInstance(obj, list) or isInstance(obj, tuple) or isInstance(obj, xrange)

class PatternScanner(object):
    def __init__(self, tokens, category):
        self.tokens = tokens
        self.category = category

    def scan(self):
        """adapted from a scanner that allowed selection category or family or indicator.  For DIG, we will not
need fine-grained application of scans; but family and indicator left in and stubbed for now"""
        tokenList = self.tokens
        category = self.category
        family = None
        indicator = None
        def generateCandidates():
            if family:
                phrase = byFamily[(category, family)]
                if phrase:
                    yield phrase
            elif category:
                for phrase in byCategory[category]:
                    yield phrase
            elif indicator:
                # coerce indicator to list
                key = None
                if isSequence(indicator):
                    key = tuple(indicator)
                elif isInstance(indicator, basestring):
                    key = tuple([int(x) for x in indicator.split('.')])
                else:
                    raise ValueError(indicator)
                phrase = byIndic[key]
                if phrase:
                    yield phrase
            else:
                # all
                for cat in byCategory:
                    for phrase in byCategory[cat]:
                        # print phrase
                        yield phrase

        ts = TokenSearcher(tokenList)
        result = list()
        for phrase in generateCandidates():
            # print phrase.pattern
            match = ts.findall(phrase.pattern)
            if match:
                result.append((phrase, match))
        return result

class Phrase(object):

    def __init__(self, indic, category, family, pattern, weight):
        """Would like this to be interned"""
        self.indic = indic
        self.category = category
        self.family = family
        self.pattern = pattern
        self.weight = weight
        self.index()

    def __str__(self):
        return "<Phrase %s: %s.%s>" % (self.indic, self.category, self.family)
    
    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()

    def index(self):
        byIndic[self.indic] = self
        byCategory[self.category].append(self)
        byFamily[(self.category, self.family)] = self

Phrase.byIndic = byIndic
Phrase.byCategory = byCategory
Phrase.byFamily = byFamily

vocab = {
    "friend": "|".join(["FRIEND", "FREIND", "GIRLFRIEND", "GIRLFREIND", "GF", "FREND", "PLAYMATE"]),
    "friends": "|".join(["FRIENDS", "FREINDS", "GIRLFRIENDS", "GIRLFREINDS", "GFS", "FRENDS", "PLAYMATES"]),
    "two": "|".join(["2", "TWO"]),
    "both": "|".join(["BOTH", "ALL", "TWO", "THREE"]),
    "have": "|".join(["HAVE", "CHOOSE", "EXPERIENCE", "ENJOY"]),
    "girls": "|".join(["GIRLS", "WOMEN", "LADIES", "GIRLZ", "GIRLZZ", "LADIEZ", "CHICKS", "GURLS", "GURLZ", "GURLZZ"]),
    "girl": "|".join(["GIRL", "WOMAN", "LADY", "CHICK", "GURL"]),
    "special": "|".join(["SHOW", "SPECIAL"]),
    "specials": "|".join(["SHOWS", "SPECIALS"]),
    "double": "|".join(["DOUBLE", "TWICE", "DBL", "DBBL", "DBLS", "DBBLS"]),
    "your": "|".join(["YOUR", "YER", "YOURE", "YOU 'RE"]),

    "pleasure": "|".join(["PLEASURE", "FUN", "EXCITING", "EXCITEMENT", "SEXY", "TREAT"]),
    
    "man": "|".join(["MAN", "MALE", "GENTLEMAN", "GENTELMAN", "GENTLMAN", "DUDE", "DATE", "GENT", "GUY", "BOY", "B0Y", "FELLOW", "FELLA", "PERSON"]),
    "men": "|".join(["MEN", "MALES", "GENTLEMEN", "GENTELMEN", "GENTLMEN", "DUDES", "DATES", "GENTS", "GUYS", "BOYS", "B0YS", "FELLOWS", "FELLAS", "PERSONS", "PEOPLE"]),
    "black": "|".join(["BLACK", "AFRICAN-AMERICAN", "AA", "AFRO-AMERICAN", "AFRICANAMERICA", "AFROAMERICAN", "BLK"]),
    "blacks": "|".join(["BLACKS", "BLACKMEN", "AFRICAN-AMERICANS", "AAS"]),
    "african": "|".join(["AFRICAN", "AFRO"]),
    "white": "|".join(["WHITE", "CAUCASIAN", "CAUCASION"]),
    "whites": "|".join(["WHITES", "CAUCASIANS", "CAUCASIONS", "WHITEMEN"]),
    
    "town": "|".join(["TOWN", "AREA", "CITY", "NEIGHBORHOOD"]),
    "new": "|".join(["NEW", "NU"]),
    "limited": "|".join(["LIMITED", "SHORT"]),
    "time": "|".join(["TIME", "VISIT", "WHILE"]),
    "few": "|".join(["FEW", "COUPLE"]),
    "num": "|".join(["2", "TWO", "TOW", "3", "THREE", "4", "FOUR", "5", "FIVE"]),
    "days": "|".join(["DAYS", "NIGHTS", "HOURS"]),
    
    "older": "|".join(["OLDER", "MATURE"]),
    "prefer": "|".join(["PREFER", "LOVE", "&#10084;"]),
    "preferred": "|".join(["PREFERRED", "ESPECIALLY", "PLEASE"]),
    
    ## 22 May 2013
    ## NOTE: Tokenization yields many tokens which include 'incall'
    ## etc. but also include other characters, such as general
    ## location, price, hours.  This is a good candidate for a rework
    ## where offsets and examineWindow would accept a regex rather
    ## than only a literal

    "incall": "|".join(["INCALL", "IN-CALL", "INCALLS", "IN-CALLS", "INCALLZ", "IN-CALLZ", "INS", 
                        "INCAL", "INCALS",
                        "I/C", "IC"]),
    "outcall": "|".join(["OUTCALL", "OUT-CALL", "OUTCALLS", "OUT-CALLS", "OUTCALLZ", "OUT-CALLZ", "OUTCAL",
                         "0UTCALL", "0UT-CALL", "0UTCALLS", "0UT-CALLS", "0UTCALLZ", "0UT-CALLZ", "OUTCALS",
                         # OC can also mean Orange County so we don't want to use it in isolation
                         "O/C"]),
    "call": "|".join(["CALL", "CALLS", "CALLZ", "CALSS", "C@LL", "CAL", "CALS", "CALZ"]),
    "place": "|".join(["PLACE", "HOTEL", "HOME", "APARTMENT", "APT"]),
    "in": "|".join(["IN", "INS", "INZ"]),
    "out": "|".join(["OUT", "0UT", "OUTS", "0UTS", "OUTZ", "0UTZ"]),
    # desciptors for "location"
    "safe": "|".join(["SAFE", "CLEAN", "NICE", "UPSCALE", "COMFORTABLE", "PRIVATE"]),
    "discreet": "|".join(["DISCREET", "DISCRETE", "DESCREET", "DISCRET", "DESCRETE", "DISCREETE", "DISCRETO", "DESCRET", "DISCREAT", "DISCRETA", "DECREET", "DICREET", "DECRETE"]),
    "location": "|".join(["LOCATION", "RESIDENTIAL", "RESIDENCE"]),

    "honey": "|".join(["HONEY", "HON", "HUN"]),
    "punctuation": "|".join([",", "\\*", "!", ":"]),
    # punctuation/etc intended to indicate and/or
    "andor": "|".join([",", "/", "&", "AND", "OR", "~", "-", "--"]),

    ## 12 August 2013
    "asian": "|".join(["ASIAN", "ASAIN",
                       "CHINESE", "JAPANESE", "KOREAN", "THAI", "VIETNAMESE", "ORIENTAL", 
                       "FILIPINO", "FILIPINA", "PHILIPINO", "PHILIPINA",
                       "MALAYSIAN"]),
    "latina": "|".join(["LATINA", "LATINO", "LATIN"]),
    "asia": "|".join(["ASIA", "CHINA", "HONG" "KONG" "BEIJING" "TAIWAN" "TAIPEI" 
                      "JAPAN", "TOKYO", "OSAKA",
                      "KOREA", "SEOUL", 
                      "THAILAND", "BANGKOK",
                      "VIETNAM", 
                      "ORIENT", 
                      "PHILIPPINES", "MANILA",
                      "MALAYSIA"]),
    # "spa": "|".join(["SPA", "MASSAGE"]),
    "spa": "|".join(["SPA"]),
    "therapy": "|".join(["MASSEUSE", "MASSEUSES", "THERAPY", "THERAPIST", "THERAPISTS", "THERAPEUTIC", "RUB", "SHOWER", "STAFF", "STAFFS"]),
    "shiatsu": "|".join(["SHIATSU", "SWEDISH", "TISSUE", "NURU", "REFLEXOLOGY"]),
    "massage": "|".join(["MASSAGE", "MASSEUSE", "MASSEUSES"]),

    # not agency
    # no agency
    # not an agency
    # no * agency
    #
    # not with an agency
    # not affiliated|associated with any|an agency
    # [do not work] for an agency
    # law enforcement[s] enforcment inforcement agency

    # by an agency

    "agency": "|".join(["AGENCY", "CLUB", "ESTABLISHMENT", "AGENCIA"]),
    "affiliated": "|".join(["AFFILIATED", "ASSOCIATED", "WORK", "EMPLOYED"]),
    "with": "|".join(["WITH", "BY"]),
    "law": "|".join(["LAW"]),
    # '%nf%c%nt%' is productive and reasonably targeted
    "enforcement": "|".join(["ENFORCEMENT", "ENFORCEMENTS", "ENFORCMENT", "INFORCEMENT", 
                             "ENTRAP", "ENTRAPMENT", "ENRAPEMENT"]),
    # not with an agency
    # not affiliated|associated with any|an agency
    # [do not work] for an agency
    # law enforcement[s] enforcment inforcement agency
    "superbowl": "|".join(["superbowl", "meadowlands"]),
    }

def v(*args):
    return "|".join([vocab[arg] for arg in args])

## (r"(?V1)<(?-i)ABC> <(?-i)def>")

## SECTION 1: multi-provider
# ask about my friend
Phrase((1,1,1), "multiProvider", "ask", r"""(?V1)<(?i)ASK> <(?i)ABOUT> <(?i)MY> <(?i).*>? <(?i)%s>""" % v('friend','friends'), 1)
# I have a friend
Phrase((1,1,2), "multiProvider", "i have", r"""(?V1)<(?i)I> <(?i)ALSO>? <(?i)HAVE> <(?i)A>? (<(?i).*>)? <(?i)%s>""" % v('friend','friends'), 1)
# me and my friend
Phrase((1,1,3), "multiProvider", "me and my", r"""(?V1)<(?i)ME> <(?i)AND> <(?i)MY> <(?i).*>? <(?i)%s>""" % v('friend','friends'), 1)
# with my friend
Phrase((1,1,4), "multiProvider", "with my", r"""(?V1)<(?i)WITH> <(?i)MY> <(?i).*>? <(?i)%s>""" % v('friend','friends'), 1)
# possessive: my friend ' s name is
Phrase((1,1,5), "multiProvider", "my friends name", r"""(?V1)<(?i)MY> <(?i)%s> <(?i)'S> <(?i)NAME>""" % v('friend'), 1)
# my friend(s), my cool friend, my really cool friend
Phrase((1,2,1), "multiProvider", "my friend", r"""(?V1)<(?i)MY> <(?i).*>{0,2} <(?i)%s>""" % v('friend', 'friends'), 0.5)
# my nice, cool friend(s)
Phrase((1,2,2), "multiProvider", "my x,y friend", r"""(?V1)<(?i)MY> <(?i).*> <(?i),>, <(?i).*> <(?i)%s>""" % v('friend', 'friends'), 0.5)
# two/2 girl shows/specials
Phrase((1,3,1), "multiProvider", "two girl show", r"""(?V1)<(?i)%s> <(?i)%s> <(?i)%s>""" % (v('num'), v('girl'), v('special', 'specials')), 1)
# have both of us
Phrase((1,4,1), "multiProvider", "have both of us", r"""(?V1)<(?i)%s> <(?i)%s> <(?i)OF> <(?i)US>""" % (v('have'), v('both')), 1)
# both girls for [$]
Phrase((1,5,1), "multiProvider", "both girls for", r"""(?V1)<(?i)%s> <(?i)%s> <(?i)FOR>""" % (v('both'), v('girls','friends')), 1)
# [$] for both girls
Phrase((1,5,2), "multiProvider", "for both girls", r"""(?V1)<(?i)FOR> <(?i)%s> <(?i)%s>""" % (v('both'), v('girls','friends')), 1)
# double {the} pleasure
Phrase((1,6,1), "multiProvider", "double pleasure", r"""(?V1)<(?i)%s> <(?i)THE>? <(?i)%s>""" % (v('double'), v('pleasure')), 1)
# double your pleasure
Phrase((1,6,2), "multiProvider", "double your pleasure", r"""(?V1)<(?i)%s> <(?i)%s> <(?i)%s>""" % (v('double'), v('your'), v('pleasure')), 1)
# double you're (sic) pleasure 
Phrase((1,6,3), "multiProvider", "double you're pleasure", r"""(?V1)<(?i)%s> <(?i)YOU> <(?i)'RE> <(?i)%s>""" % (v('double'), v('pleasure')), 1)
# twice as exciting 
Phrase((1,7,1), "multiProvider", "twice as exciting", r"""(?V1)<(?i)%s> <(?i)AS> <(?i)%s>""" % (v('double'), v('pleasure')), 1)
# two times as exciting, 2 times the pleasure
Phrase((1,7,2), "multiProvider", "two times as exciting", r"""(?V1)<(?i)%s> <(?i)TIMES> <(?i)AS|THE> <(?i)%s>""" % (v('num'), v('pleasure')), 1)
# duo (any context)
Phrase((1,8,1), "multiProvider", "duo", r"""(?V1)<(?i)DUO>""", 1)

## SECTION 2: RACE/ETHNIC SELECTION
# no black men
Phrase((2,1,1), "raceEthnicSelect", "no black men", r"""(?V1)<(?i)NO> <(?i)%s> <(?i)%s>""" % (v('black'), v('man', 'men')), 1)
# no african american men
Phrase((2,1,2), "raceEthnicSelect", "no african american men", r"""(?V1)<(?i)NO> <(?i)%s> <(?i)AMERICAN> <(?i)%s>""" % (v('african'), v('man', 'men')), 1)
# no african-american men
Phrase((2,1,3), "raceEthnicSelect", "no african-american men", r"""(?V1)<(?i)NO> <(?i)%s> <(?i)-> <(?i)AMERICAN> <(?i)%s>""" % (v('african'), v('man', 'men')), 1)
# no blacks
Phrase((2,1,4), "raceEthnicSelect", "no blacks", r"""(?V1)<(?i)NO> <(?i)%s>""" % (v('blacks')), 1)
# white men only
Phrase((2,2,1), "raceEthnicSelect", "white men only", r"""(?V1)<(?i)%s> <(?i)%s> <(?i)ONLY>""" % (v('white'), v('man', 'men')), 1)
# only white men, only date/see white men
Phrase((2,2,2), "raceEthnicSelect", "only white men", r"""(?V1)<(?i)ONLY> <(?i)DATE|SEE>? <(?i)%s> <(?i)%s>""" % (v('white'), v('man', 'men')), 1)
# whites only
Phrase((2,2,3), "raceEthnicSelect", "whites only", r"""(?V1)<(?i)%s> <(?i)ONLY>""" % (v('whites')), 1)
# only whites, only date/see whites
Phrase((2,2,4), "raceEthnicSelect", "only whites", r"""(?V1)<(?i)ONLY> <(?i)DATE|SEE>? <(?i)%s>""" % (v('whites')), 1)
# white men preferred
Phrase((2,3,1), "raceEthnicSelect", "white men preferred", r"""(?V1)<(?i)%s> <(?i)%s> <(?i)%s>""" % (v('white'), v('man', 'men'), v('preferred')), 1)
# prefer white men, prefer to date/see white men
Phrase((2,3,2), "raceEthnicSelect", "prefer white men", r"""(?V1)<(?i)%s> <(?i)TO>? <(?i)DATE|SEE>? <(?i)%s> <(?i)%s>""" % (v('prefer'), v('white'), v('man', 'men')), 1)
# whites preferred
Phrase((2,3,3), "raceEthnicSelect", "whites preferred", r"""(?V1)<(?i)%s> <(?i)%s>""" % (v('whites'), v('preferred')), 1)
# prefer whites, prefer to date/see whites
Phrase((2,3,4), "raceEthnicSelect", "prefer whites", r"""(?V1)<(?i)%s> <(?i)TO>? <(?i)DATE|SEE>? <(?i)%s>""" % (v('prefer'), v('whites')), 1)
### TBD
### I don't service blacks

## SECTION 3: Limited duration: New arrival, limited time, etc.
# new in town
Phrase((3,1,1), "briefDuration", "new in town", r"""(?V1)<(?i)%s> <(?i)IN|N|TO> <(?i)THE|THIS>? <(?i)%s>""" % (v('new'), v('town')), 1)
# [for a] limited time
Phrase((3,2,1), "briefDuration", "limited time", r"""(?V1)<(?i)%s> <(?i)%s>""" % (v('limited'), v('time')), 1)
# (for a) few days/nights, few more days, couple 
Phrase((3,3,1), "briefDuration", "few days", r"""(?V1)<(?i)%s> <(?i)MORE>? <(?i)%s>""" % (v('few'), v('days')), 1)
# (for a) few exciting days
Phrase((3,3,2), "briefDuration", "few * days", r"""(?V1)<(?i)%s> <(?i)%s>""" % (v('few'), v('days')), 0.5)
# (for) two days only
Phrase((3,4,1), "briefDuration", "two days only", r"""(?V1)<(?i)%s> <(?i)%s> <(?i)ONLY>""" % (v('num'), v('days')), 1)
# 2 more days
Phrase((3,4,2), "briefDuration", "two more days", r"""(?V1)<(?i)%s> <(?i)MORE> <(?i)%s>""" % (v('num'), v('days')), 1)
# visiting
Phrase((3,5,1), "briefDuration", "visiting", r"""(?V1)<(?i)VISITING>""", 1)

# SECTION 4: customer age selection
# older men
Phrase((4,1,1), "ageSelect", "older men only", r"""(?V1)<(?i)%s> <(?i)%s> <(?i)ONLY>""" % (v('older'), v('man', 'men')), 1.0)
Phrase((4,1,2), "ageSelect", "only older men", r"""(?V1)<(?i)ONLY> <(?i)%s> <(?i)%s>""" % (v('older'), v('man', 'men')), 1.0)
# older, generous men
Phrase((4,1,3), "ageSelect", "older x, y men", r"""(?V1)<(?i)%s> <(?i).*> <(?i),>? <(?i).*> <(?i)%s>""" % (v('older'), v('man', 'men')), 0.8)
# men 35 or older
Phrase((4,1,4), "ageSelect", "man x,y, older", r"""(?V1)<(?i)%s> <(?i).*> <(?i).*> <(?i)%s>""" % (v('man', 'men'), v('older')), 0.8)
# prefer/love older men
Phrase((4,2,1), "ageSelect", "prefer older men", r"""(?V1)<(?i)%s> <(?i)%s> <(?i)%s>""" % (v('prefer'), v('older'), v('man', 'men')), 1)
Phrase((4,2,2), "ageSelect", "prefer older x y men", r"""(?V1)<(?i)%s> <(?i)%s> <(?i).*>{0,2} <(?i)%s>""" % (v('prefer'), v('older'), v('man', 'men')), 1)
Phrase((4,2,3), "ageSelect", "prefer older x,y men", r"""(?V1)<(?i)%s> <(?i)%s> <(?i).*> <(?i),> <(?i).*> <(?i)%s>""" % (v('prefer'), v('older'), v('man', 'men')), 1)
Phrase((4,2,4), "ageSelect", "older men preferred", r"""(?V1)<(?i)%s> <(?i)%s> <(?i)%s>""" % (v('older'), v('man', 'men'), v('preferred')), 1)

# SECTION 5: provider youthfulness
# young
Phrase((5,1,1), "providerYouth", "young", r"""(?V1)<(?i)YOUNG>""", 0.8)
# tight
Phrase((5,2,1), "providerYouth", "tight", r"""(?V1)<(?i)TIGHT|TITE>""", 0.8)
# new: ideally, this matches only if new does not match new in town etc above
Phrase((5,3,1), "providerYouth", "new", r"""(?V1)<(?i)%s>""" % v('new'), 0.5)

# SECTION 6: incall
Phrase((6,1,1), "incall", "incall", r"""(?V1)<(?i)%s>""" % v('incall'), 1)
# in call , in-call
Phrase((6,1,2), "incall", "in call", r"""(?V1)<(?i)IN> <(?i)->? <(?i)%s>""" % v('call'), 1)
Phrase((6,2,1), "incall", "my place", r"""(?V1)<(?i)MY> <(?i)%s>""" % v('place'), 1)
# hosting (should it be hosting in/at/out of?)
Phrase((6,3,1), "incall", "hosting", r"""(?V1)<(?i)HOSTING>""", 1)
Phrase((6,4,1), "incall", "safe location", r"""(?V1)<(?i)%s>""" % v('safe'), 1)
Phrase((6,4,2), "incall", "discreet location", r"""(?V1)<(?i)%s>""" % v('discreet'), 1)

# SECTION 7: NOTINCALL
Phrase((7,1,1), "notincall", "not", r"""(?V1)<(?i)NO|NOT|N0> <(?i)%s>""" % v('incall'), 1)

# SECTION 8: outcall
Phrase((8,1,1), "outcall", "outcall", r"""(?V1)<(?i)%s>""" % v('outcall'), 1)
# out call, out-call
Phrase((8,1,2), "outcall", "out-call", r"""(?V1)<(?i)OUT> <(?i)-> <(?i)%s>""" % v('call'), 1)
# your place
Phrase((8,2,1), "outcall", "your place", r"""(?V1)<(?i)%s> <(?i)%s>""" % (v('your'), v('place')), 1)
# you're place
Phrase((8,2,2), "outcall", "you're place", r"""(?V1)<(?i)YOU> <(?i)'RE> <(?i)%s>""" % v('place'), 1)
# hotel friendly? hotel/motel

# SECTION 9: NOTOUTCALL
Phrase((9,1,1), "notoutcall", "not", r"""(?V1)<(?i)NO|NOT|N0> <(?i)%s>""" % v('outcall'), 1)

# SECTION 10: incall + outcall both
# single token
Phrase((10,1,1), "incalloutcall", "incall/outcall", r"""(?V1)<(?i)(?:%s)[-/*_]+(?:%s)>""" % (v('incall', 'in'), v('outcall', 'out')), 1)

# two tokens
Phrase((10,2,1), "incalloutcall", "in call/outcall", r"""(?V1)<(?i)IN> <(?i)(?:%s)[-/*_]+(?:%s)>""" % (v('call'), v('outcall', 'out')), 1)

# three tokens
Phrase((10,3,1), "incalloutcall", "incall / outcall", r"""(?V1)<(?i)%s> <(?i)%s>? <(?i)%s>""" % (v('incall', 'in'), v('andor'), v('outcall', 'out')), 1)

# SECTION 13: names
# needs case sensitivity
Phrase((13,1,1), "names", "my name is", r"""(?V1)<(?i)THE|MY> <(?i)NAME> <(?i)IS|'S> <(?-i)[A-Z][a-zA-Z-]*>""", 1)
Phrase((13,1,2), "names", "my names", r"""(?V1)<(?i)THE|MY> <(?i)NAMES> <(?-i)[A-Z][a-zA-Z-]*>""", 1)

Phrase((13,2,1), "names", "hi fellas i am", r"""(?V1)<(?i)HELLO|HI|HEY|HOWDY>? <(?i)%s>? <(?i)%s>? <(?i)I> <(?i)AM|'M> <(?-i)[A-Z][a-zA-Z-]*>""" % (v('honey', 'men'), v('punctuation')), 1)
Phrase((13,2,2), "names", "hi fellas im", r"""(?V1)<(?i)HELLO|HI|HEY|HOWDY>? <(?i)%s>? <(?i)%s>? <(?i)IM|IAM> <(?-i)[A-Z][a-zA-Z-]*>"""  % (v('honey', 'men'), v('punctuation')), 1)

Phrase((13,3,1), "names", "ask for", r"""(?V1)<(?i)ASK> <(?i)FOR> <(?-i)[A-Z][a-zA-Z-]*>""", 1)
Phrase((13,3,2), "names", "try me", r"""(?V1)<(?i)TRY> <(?i)ME> <(?-i)[A-Z][a-zA-Z-]*>""", 1)
Phrase((13,3,4), "names", "call now", r"""(?V1)<(?i)CALL> <(?i)NOW|ME> <(?i)%s>? <(?-i)[A-Z][a-zA-Z-]*>""" % v('punctuation'), 1)

Phrase((13,4,1), "names", "yours", r"""(?V1)<(?i)YOURS|YERS> <(?i)TRULY|TRUELY>? <(?i)%s>? <(?-i)[A-Z][a-zA-Z-]*>""" % v('punctuation'), 1)
Phrase((13,4,2), "names", "xoxo", r"""(?V1)<(?i)XOXO> <(?i)%s>? <(?-i)[A-Z][a-zA-Z-]*>""" % v('punctuation'), 1)
Phrase((13,4,3), "names", "kisses", r"""(?V1)<(?i)KISSES> <(?i)%s>? <(?-i)[A-Z][a-zA-Z-]*>""" % v('punctuation'), 1)
Phrase((13,4,4), "names", "mwah", r"""(?V1)<(?i)MWAH|MUAH> <(?i)%s>? <(?-i)[A-Z][a-zA-Z-]*>""" % v('punctuation'), 1)

# SECTION 15: race/ethnic
Phrase((15,1,1), "ethnicityNationality", "asian", r"""(?V1)<(?i)%s>""" % v('asian'), 1)
Phrase((15,1,2), "ethnicityNationality", "asia", r"""(?V1)<(?i)%s>""" % v('asia'), 1)
Phrase((15,1,3), "ethnicityNationality", "latina", r"""(?V1)<(?i)%s>""" % v('latina'), 1)

# SECTION 21: spa
Phrase((21,1,1), "spa", "spa", r"""(?V1)<(?i)%s>""" % v('spa'), 1)
Phrase((21,1,2), "spa", "therapy", r"""(?V1)<(?i)%s>""" % v('therapy'), 0.5)
Phrase((21,1,3), "spa", "massage", r"""(?V1)<(?i)%s> (?V1)<(?i)%s>""" % (v('shiatsu'), v('massage')), 1)
# SECTION 31: agency
Phrase((31,1,1), "agency", "agency", r"""(?V1)<(?i)%s>""" % v('agency'), 1)
# SECTION 32: not an agency
# no agency, not an agency
# not with an agency, not with any agency
Phrase((32,1,1), "notagency", "not", r"""(?V1)<(?i)NO|NOT|N0> <.*>{0,2} <(?i)%s>""" % v('agency'), 1)

# not affiliated|associated with any|an agency
# [do not work] for an agency
Phrase((32,1,2), "notagency", "affiliated", r"""(?V1)<(?i)%s> <(?i)%s> <.*>? <(?i)%s>""" % (v('affiliated'), v('with'), v('agency')), 1)

# law enforcement[s] enforcment inforcement agency
Phrase((32,1,3), "notagency", "enforcement", r"""(?V1)<(?i)%s> <(?i)%s>""" % (v('enforcement'), v('agency')), 1)

# SECTION 91: superbowl
Phrase((91,1,1), "superbowl", "superbowl", r"""(?V1)<(?i)SUPERBOWL>""", 1)
Phrase((91,1,2), "superbowl", "super bowl", r"""(?V1)<(?i)SUPER> (?V1)<(?i)BOWL>""", 1)
Phrase((91,2,1), "meadowlands", "meadowlands", r"""(?V1)<(?i)MEADOWLANDS>""", 1)
Phrase((91,2,2), "meadowlands", "meadow lands", r"""(?V1)<(?i)MEADOW> (?V1)<(?i)LANDS>""", 1)

# SECTION 92: superbowl
Phrase((92,1,1), "NBA", "NBA", r"""(?V1)<(?i)NBA>""", 1)
Phrase((92,2,1), "allstar", "allstar", r"""(?V1)<(?i)allstar>""", 1)
Phrase((92,2,2), "allstar", "all star", r"""(?V1)<(?i)ALL> <->? (?V1)<(?i)STAR>""", 1)

DEFAULTCATEGORY = "multiProvider"
def main(argv=None):
    '''this is called if run from command line'''
    (prog, args) = interpretCmdLine()
    parser = argparse.ArgumentParser(prog, description='PatterScanner')
    parser.add_argument('-c', '--category', help='category to match', 
                        required=True, 
                        default=DEFAULTCATEGORY)
    # parser.add_argument()
    args = parser.parse_args(args)
    category = args.category
    
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
                titleText = post.get('titleText')
                if titleText:
                    scanner = PatternScanner(titleText['tokens'], category)
                    # arguably we should only add novel matches
                    # implemention would be to represent/convert 
                    # patternScanMatch dicts to namedtuples
                    # use a set to uniquify
                    # then convert back to dict to write out as JSON
                    # for now, we will simply append to list
                    titlePatternScanMatches = titleText.get('patternScanMatches') or []
                    for (phrase, subseqs) in scanner.scan():
                        for subseq in subseqs:
                            resultJson = {"objectType": "patternScanMatch",
                                          "phrasePattern":
                                              {"indic": phrase.indic,
                                               "category": phrase.category,
                                               "family": phrase.family,
                                               "tokenRegexPattern": str(phrase.pattern),
                                               "weight": phrase.weight},
                                          "tokenSequence": subseq}
                            titlePatternScanMatches.append(resultJson)
                    # is it good practice to record empty results
                    # or should we just not have any such entry
                    titleText['patternScanMatches'] = titlePatternScanMatches
                locationText = post.get('locationText')
                if locationText:
                    scanner = PatternScanner(locationText['tokens'], category)
                    # arguably we should only add novel matches
                    # implemention would be to represent/convert 
                    # patternScanMatch dicts to namedtuples
                    # use a set to uniquify
                    # then convert back to dict to write out as JSON
                    # for now, we will simply append to list
                    locationPatternScanMatches = locationText.get('patternScanMatches') or []
                    for (phrase, subseqs) in scanner.scan():
                        for subseq in subseqs:
                            resultJson = {"objectType": "patternScanMatch",
                                          "phrasePattern":
                                              {"indic": phrase.indic,
                                               "category": phrase.category,
                                               "family": phrase.family,
                                               "tokenRegexPattern": str(phrase.pattern),
                                               "weight": phrase.weight},
                                          "tokenSequence": subseq}
                            locationPatternScanMatches.append(resultJson)
                    # is it good practice to record empty results
                    # or should we just not have any such entry
                    locationText['patternScanMatches'] = locationPatternScanMatches
                bodyText = post.get('bodyText')
                if bodyText:
                    scanner = PatternScanner(bodyText['tokens'], category)
                    # arguably we should only add novel matches
                    # implemention would be to represent/convert 
                    # patternScanMatch dicts to namedtuples
                    # use a set to uniquify
                    # then convert back to dict to write out as JSON
                    # for now, we will simply append to list
                    bodyPatternScanMatches = bodyText.get('patternScanMatches') or []
                    for (phrase, subseqs) in scanner.scan():
                        for subseq in subseqs:
                            resultJson = {"objectType": "patternScanMatch",
                                          "phrasePattern":
                                              {"indic": phrase.indic,
                                               "category": phrase.category,
                                               "family": phrase.family,
                                               "tokenRegexPattern": str(phrase.pattern),
                                               "weight": phrase.weight},
                                          "tokenSequence": subseq}
                            bodyPatternScanMatches.append(resultJson)
                    # is it good practice to record empty results
                    # or should we just not have any such entry
                    bodyText['patternScanMatches'] = bodyPatternScanMatches

            js = json.dumps(post, sort_keys=True, indent=None)
            print >> sys.stdout, "%s\t%s" % (url, js)

# call main() if this is run as standalone
if __name__ == "__main__":
    sys.exit(main())
