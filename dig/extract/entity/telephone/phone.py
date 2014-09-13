#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: phone.py

# also consider
#!/usr/bin/env python

'''
dig.extract.entity.telephone.phone
@author: Andrew Philpot
@version 1.4
'''

import sys, os, re
import simplejson as json
import argparse
from dig.pymod.util import interpretCmdLine
from pkg_resources import resource_string
# for debug only
from dig.pymod.util import echo

VERSION = "1.4"
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

AREACODES = {
             "201": {
                     "areaCode": "201",
                     "cities": "Jersey City",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NJ",
                     "stateProvinceDistrictName": "New Jersey"
                     },
             "202": {
                     "areaCode": "202",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "DC",
                     "stateProvinceDistrictName": "Washington, D.C."
                     },
             "203": {
                     "areaCode": "203",
                     "cities": "New Haven",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CT",
                     "stateProvinceDistrictName": "Connecticut"
                     },
             "204": {
                     "areaCode": "204",
                     "cities": "",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "MB",
                     "stateProvinceDistrictName": "Manitoba"
                     },
             "205": {
                     "areaCode": "205",
                     "cities": "Birmingham",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "AL",
                     "stateProvinceDistrictName": "Alabama"
                     },
             "206": {
                     "areaCode": "206",
                     "cities": "Seattle",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "WA",
                     "stateProvinceDistrictName": "Washington"
                     },
             "207": {
                     "areaCode": "207",
                     "cities": "Estcourt Station",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "ME",
                     "stateProvinceDistrictName": "Maine"
                     },
             "208": {
                     "areaCode": "208",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "ID",
                     "stateProvinceDistrictName": "Idaho"
                     },
             "209": {
                     "areaCode": "209",
                     "cities": "Stockton",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "210": {
                     "areaCode": "210",
                     "cities": "San Antonio",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "212": {
                     "areaCode": "212",
                     "cities": "Manhattan",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NY",
                     "stateProvinceDistrictName": "New York"
                     },
             "213": {
                     "areaCode": "213",
                     "cities": "Downtown Los Angeles",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "214": {
                     "areaCode": "214",
                     "cities": "Dallas/Fort Worth metroplex",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "215": {
                     "areaCode": "215",
                     "cities": "Philadelphia",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "PA",
                     "stateProvinceDistrictName": "Pennsylvania"
                     },
             "216": {
                     "areaCode": "216",
                     "cities": "Cleveland",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "OH",
                     "stateProvinceDistrictName": "Ohio"
                     },
             "217": {
                     "areaCode": "217",
                     "cities": "Springfield",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IL",
                     "stateProvinceDistrictName": "Illinois"
                     },
             "218": {
                     "areaCode": "218",
                     "cities": "Duluth",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MN",
                     "stateProvinceDistrictName": "Minnesota"
                     },
             "219": {
                     "areaCode": "219",
                     "cities": "Gary",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IN",
                     "stateProvinceDistrictName": "Indiana"
                     },
             "224": {
                     "areaCode": "224",
                     "cities": "Arlington Heights",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IL",
                     "stateProvinceDistrictName": "Illinois"
                     },
             "225": {
                     "areaCode": "225",
                     "cities": "Baton Rouge",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "LA",
                     "stateProvinceDistrictName": "Louisiana"
                     },
             "226": {
                     "areaCode": "226",
                     "cities": "",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "ON",
                     "stateProvinceDistrictName": "Ontario"
                     },
             "228": {
                     "areaCode": "228",
                     "cities": "Pascagoula",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MS",
                     "stateProvinceDistrictName": "Mississippi"
                     },
             "229": {
                     "areaCode": "229",
                     "cities": "Albany",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "GA",
                     "stateProvinceDistrictName": "Georgia"
                     },
             "231": {
                     "areaCode": "231",
                     "cities": "Traverse City",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MI",
                     "stateProvinceDistrictName": "Michigan"
                     },
             "234": {
                     "areaCode": "234",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "OH",
                     "stateProvinceDistrictName": "Ohio"
                     },
             "239": {
                     "areaCode": "239",
                     "cities": "Lee County",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "FL",
                     "stateProvinceDistrictName": "Florida"
                     },
             "240": {
                     "areaCode": "240",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MD",
                     "stateProvinceDistrictName": "Maryland"
                     },
             "242": {
                     "areaCode": "242",
                     "cities": "",
                     "countryAbbrev": "BS",
                     "countryCode": "44",
                     "stateProvinceDistrictAbbrev": "00",
                     "stateProvinceDistrictName": "Bahamas"
                     },
             "246": {
                     "areaCode": "246",
                     "cities": "",
                     "countryAbbrev": "BB",
                     "countryCode": "52",
                     "stateProvinceDistrictAbbrev": "00",
                     "stateProvinceDistrictName": "Barbados"
                     },
             "248": {
                     "areaCode": "248",
                     "cities": "Oakland County",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MI",
                     "stateProvinceDistrictName": "Michigan"
                     },
             "249": {
                     "areaCode": "249",
                     "cities": "Northeastern Ontario",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "ON",
                     "stateProvinceDistrictName": "Ontario"
                     },
             "250": {
                     "areaCode": "250",
                     "cities": "Victoria",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "BC",
                     "stateProvinceDistrictName": "British Columbia"
                     },
             "251": {
                     "areaCode": "251",
                     "cities": "Mobile County",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "AL",
                     "stateProvinceDistrictName": "Alabama"
                     },
             "252": {
                     "areaCode": "252",
                     "cities": "Rocky Mount",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NC",
                     "stateProvinceDistrictName": "North Carolina"
                     },
             "253": {
                     "areaCode": "253",
                     "cities": "Tacoma",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "WA",
                     "stateProvinceDistrictName": "Washington"
                     },
             "254": {
                     "areaCode": "254",
                     "cities": "Waco",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "256": {
                     "areaCode": "256",
                     "cities": "Huntsville",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "AL",
                     "stateProvinceDistrictName": "Alabama"
                     },
             "260": {
                     "areaCode": "260",
                     "cities": "Fort Wayne",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IN",
                     "stateProvinceDistrictName": "Indiana"
                     },
             "262": {
                     "areaCode": "262",
                     "cities": "Kenosha",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "WI",
                     "stateProvinceDistrictName": "Wisconsin"
                     },
             "264": {
                     "areaCode": "264",
                     "cities": "",
                     "countryAbbrev": "AI",
                     "countryCode": "660",
                     "stateProvinceDistrictAbbrev": "00",
                     "stateProvinceDistrictName": "Anguilla"
                     },
             "267": {
                     "areaCode": "267",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "PA",
                     "stateProvinceDistrictName": "Pennsylvania"
                     },
             "268": {
                     "areaCode": "268",
                     "cities": "",
                     "countryAbbrev": "AG",
                     "countryCode": "28",
                     "stateProvinceDistrictAbbrev": "00",
                     "stateProvinceDistrictName": "Antigua and Barbuda"
                     },
             "269": {
                     "areaCode": "269",
                     "cities": "Kalamazoo",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MI",
                     "stateProvinceDistrictName": "Michigan"
                     },
             "270": {
                     "areaCode": "270",
                     "cities": "Paducah",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "KY",
                     "stateProvinceDistrictName": "Kentucky"
                     },
             "272": {
                     "areaCode": "272",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "PA",
                     "stateProvinceDistrictName": "Pennsylvania"
                     },
             "274": {
                     "areaCode": "274",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "WI",
                     "stateProvinceDistrictName": "Wisconsin"
                     },
             "276": {
                     "areaCode": "276",
                     "cities": "Bristol",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "VA",
                     "stateProvinceDistrictName": "Virginia"
                     },
             "281": {
                     "areaCode": "281",
                     "cities": "Houston",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "283": {
                     "areaCode": "283",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "OH",
                     "stateProvinceDistrictName": "Ohio"
                     },
             "284": {
                     "areaCode": "284",
                     "cities": "",
                     "countryAbbrev": "VG",
                     "countryCode": "92",
                     "stateProvinceDistrictAbbrev": "00",
                     "stateProvinceDistrictName": "British Virgin Islands"
                     },
             "289": {
                     "areaCode": "289",
                     "cities": "",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "ON",
                     "stateProvinceDistrictName": "Ontario"
                     },
             "301": {
                     "areaCode": "301",
                     "cities": "Washington, D.C., suburbs",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MD",
                     "stateProvinceDistrictName": "Maryland"
                     },
             "302": {
                     "areaCode": "302",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "DE",
                     "stateProvinceDistrictName": "Delaware"
                     },
             "303": {
                     "areaCode": "303",
                     "cities": "Denver",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CO",
                     "stateProvinceDistrictName": "Colorado"
                     },
             "304": {
                     "areaCode": "304",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "WV",
                     "stateProvinceDistrictName": "West Virginia"
                     },
             "305": {
                     "areaCode": "305",
                     "cities": "Miami-Dade County",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "FL",
                     "stateProvinceDistrictName": "Florida"
                     },
             "306": {
                     "areaCode": "306",
                     "cities": "",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "SK",
                     "stateProvinceDistrictName": "Saskatchewan"
                     },
             "307": {
                     "areaCode": "307",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "WY",
                     "stateProvinceDistrictName": "Wyoming"
                     },
             "308": {
                     "areaCode": "308",
                     "cities": "Grand Island",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NE",
                     "stateProvinceDistrictName": "Nebraska"
                     },
             "309": {
                     "areaCode": "309",
                     "cities": "Peoria",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IL",
                     "stateProvinceDistrictName": "Illinois"
                     },
             "310": {
                     "areaCode": "310",
                     "cities": "Beverly Hills",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "312": {
                     "areaCode": "312",
                     "cities": "Chicago",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IL",
                     "stateProvinceDistrictName": "Illinois"
                     },
             "313": {
                     "areaCode": "313",
                     "cities": "Detroit",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MI",
                     "stateProvinceDistrictName": "Michigan"
                     },
             "314": {
                     "areaCode": "314",
                     "cities": "St. Louis",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MO",
                     "stateProvinceDistrictName": "Missouri"
                     },
             "315": {
                     "areaCode": "315",
                     "cities": "Syracuse",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NY",
                     "stateProvinceDistrictName": "New York"
                     },
             "316": {
                     "areaCode": "316",
                     "cities": "Wichita metropolitan area",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "KS",
                     "stateProvinceDistrictName": "Kansas"
                     },
             "317": {
                     "areaCode": "317",
                     "cities": "Indianapolis",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IN",
                     "stateProvinceDistrictName": "Indiana"
                     },
             "318": {
                     "areaCode": "318",
                     "cities": "Shreveport",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "LA",
                     "stateProvinceDistrictName": "Louisiana"
                     },
             "319": {
                     "areaCode": "319",
                     "cities": "Cedar Rapids",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IA",
                     "stateProvinceDistrictName": "Iowa"
                     },
             "320": {
                     "areaCode": "320",
                     "cities": "St. Cloud",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MN",
                     "stateProvinceDistrictName": "Minnesota"
                     },
             "321": {
                     "areaCode": "321",
                     "cities": "Orlando",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "FL",
                     "stateProvinceDistrictName": "Florida"
                     },
             "323": {
                     "areaCode": "323",
                     "cities": "City of Los Angeles",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "325": {
                     "areaCode": "325",
                     "cities": "Abilene",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "327": {
                     "areaCode": "327",
                     "cities": "Pine Bluff",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "AR",
                     "stateProvinceDistrictName": "Arkansas"
                     },
             "330": {
                     "areaCode": "330",
                     "cities": "Akron",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "OH",
                     "stateProvinceDistrictName": "Ohio"
                     },
             "331": {
                     "areaCode": "331",
                     "cities": "Aurora",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IL",
                     "stateProvinceDistrictName": "Illinois"
                     },
             "334": {
                     "areaCode": "334",
                     "cities": "Montgomery",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "AL",
                     "stateProvinceDistrictName": "Alabama"
                     },
             "336": {
                     "areaCode": "336",
                     "cities": "Greensboro",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NC",
                     "stateProvinceDistrictName": "North Carolina"
                     },
             "337": {
                     "areaCode": "337",
                     "cities": "Lake Charles",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "LA",
                     "stateProvinceDistrictName": "Louisiana"
                     },
             "339": {
                     "areaCode": "339",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MA",
                     "stateProvinceDistrictName": "Massachusetts"
                     },
             "340": {
                     "areaCode": "340",
                     "cities": "",
                     "countryAbbrev": "VI",
                     "countryCode": "850",
                     "stateProvinceDistrictAbbrev": "VI",
                     "stateProvinceDistrictName": "US Virgin Islands"
                     },
             "343": {
                     "areaCode": "343",
                     "cities": "Ottawa metropolitan area",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "ON",
                     "stateProvinceDistrictName": "Ontario"
                     },
             "345": {
                     "areaCode": "345",
                     "cities": "",
                     "countryAbbrev": "KY",
                     "countryCode": "136",
                     "stateProvinceDistrictAbbrev": "00",
                     "stateProvinceDistrictName": "Cayman Islands"
                     },
             "347": {
                     "areaCode": "347",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NY",
                     "stateProvinceDistrictName": "New York"
                     },
             "351": {
                     "areaCode": "351",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MA",
                     "stateProvinceDistrictName": "Massachusetts"
                     },
             "352": {
                     "areaCode": "352",
                     "cities": "Gainesville",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "FL",
                     "stateProvinceDistrictName": "Florida"
                     },
             "360": {
                     "areaCode": "360",
                     "cities": "Olympia",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "WA",
                     "stateProvinceDistrictName": "Washington"
                     },
             "361": {
                     "areaCode": "361",
                     "cities": "Corpus Christi",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "364": {
                     "areaCode": "364",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "KY",
                     "stateProvinceDistrictName": "Kentucky"
                     },
             "365": {
                     "areaCode": "365",
                     "cities": "",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "ON",
                     "stateProvinceDistrictName": "Ontario"
                     },
             "385": {
                     "areaCode": "385",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "UT",
                     "stateProvinceDistrictName": "Utah"
                     },
             "386": {
                     "areaCode": "386",
                     "cities": "Daytona Beach",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "FL",
                     "stateProvinceDistrictName": "Florida"
                     },
             "401": {
                     "areaCode": "401",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "RI",
                     "stateProvinceDistrictName": "Rhode Island"
                     },
             "402": {
                     "areaCode": "402",
                     "cities": "Omaha",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NE",
                     "stateProvinceDistrictName": "Nebraska"
                     },
             "403": {
                     "areaCode": "403",
                     "cities": "Calgary",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "AB",
                     "stateProvinceDistrictName": "Alberta"
                     },
             "404": {
                     "areaCode": "404",
                     "cities": "Atlanta",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "GA",
                     "stateProvinceDistrictName": "Georgia"
                     },
             "405": {
                     "areaCode": "405",
                     "cities": "Oklahoma City",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "OK",
                     "stateProvinceDistrictName": "Oklahoma"
                     },
             "406": {
                     "areaCode": "406",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MT",
                     "stateProvinceDistrictName": "Montana"
                     },
             "407": {
                     "areaCode": "407",
                     "cities": "Orlando",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "FL",
                     "stateProvinceDistrictName": "Florida"
                     },
             "408": {
                     "areaCode": "408",
                     "cities": "San Jose",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "409": {
                     "areaCode": "409",
                     "cities": "Beaumont",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "410": {
                     "areaCode": "410",
                     "cities": "Chesapeake Bay",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MD",
                     "stateProvinceDistrictName": "Maryland"
                     },
             "412": {
                     "areaCode": "412",
                     "cities": "Pittsburgh",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "PA",
                     "stateProvinceDistrictName": "Pennsylvania"
                     },
             "413": {
                     "areaCode": "413",
                     "cities": "Springfield",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MA",
                     "stateProvinceDistrictName": "Massachusetts"
                     },
             "414": {
                     "areaCode": "414",
                     "cities": "Milwaukee County",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "WI",
                     "stateProvinceDistrictName": "Wisconsin"
                     },
             "415": {
                     "areaCode": "415",
                     "cities": "San Francisco",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "416": {
                     "areaCode": "416",
                     "cities": "Toronto",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "ON",
                     "stateProvinceDistrictName": "Ontario"
                     },
             "417": {
                     "areaCode": "417",
                     "cities": "Branson",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MO",
                     "stateProvinceDistrictName": "Missouri"
                     },
             "418": {
                     "areaCode": "418",
                     "cities": "Quebec City",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "QC",
                     "stateProvinceDistrictName": "Quebec"
                     },
             "419": {
                     "areaCode": "419",
                     "cities": "Toledo",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "OH",
                     "stateProvinceDistrictName": "Ohio"
                     },
             "423": {
                     "areaCode": "423",
                     "cities": "Chattanooga",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TN",
                     "stateProvinceDistrictName": "Tennessee"
                     },
             "424": {
                     "areaCode": "424",
                     "cities": "Beverly Hills",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "425": {
                     "areaCode": "425",
                     "cities": "Bellevue",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "WA",
                     "stateProvinceDistrictName": "Washington"
                     },
             "430": {
                     "areaCode": "430",
                     "cities": "Texarkana",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "432": {
                     "areaCode": "432",
                     "cities": "Midland",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "434": {
                     "areaCode": "434",
                     "cities": "Charlottesville",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "VA",
                     "stateProvinceDistrictName": "Virginia"
                     },
             "435": {
                     "areaCode": "435",
                     "cities": "Park City",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "UT",
                     "stateProvinceDistrictName": "Utah"
                     },
             "437": {
                     "areaCode": "437",
                     "cities": "Toronto metropolitan area",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "ON",
                     "stateProvinceDistrictName": "Ontario"
                     },
             "438": {
                     "areaCode": "438",
                     "cities": "Montreal metropolitan area",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "QC",
                     "stateProvinceDistrictName": "Quebec"
                     },
             "440": {
                     "areaCode": "440",
                     "cities": "Cleveland",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "OH",
                     "stateProvinceDistrictName": "Ohio"
                     },
             "441": {
                     "areaCode": "441",
                     "cities": "",
                     "countryAbbrev": "BM",
                     "countryCode": "60",
                     "stateProvinceDistrictAbbrev": "00",
                     "stateProvinceDistrictName": "Bermuda"
                     },
             "442": {
                     "areaCode": "442",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "443": {
                     "areaCode": "443",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MD",
                     "stateProvinceDistrictName": "Maryland"
                     },
             "450": {
                     "areaCode": "450",
                     "cities": "City of Montreal",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "QC",
                     "stateProvinceDistrictName": "Quebec"
                     },
             "458": {
                     "areaCode": "458",
                     "cities": "Eugene",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "OR",
                     "stateProvinceDistrictName": "Oregon"
                     },
             "469": {
                     "areaCode": "469",
                     "cities": "Dallas",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "470": {
                     "areaCode": "470",
                     "cities": "Atlanta",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "GA",
                     "stateProvinceDistrictName": "Georgia"
                     },
             "473": {
                     "areaCode": "473",
                     "cities": "",
                     "countryAbbrev": "GD",
                     "countryCode": "308",
                     "stateProvinceDistrictAbbrev": "00",
                     "stateProvinceDistrictName": "Grenada"
                     },
             "475": {
                     "areaCode": "475",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CT",
                     "stateProvinceDistrictName": "Connecticut"
                     },
             "478": {
                     "areaCode": "478",
                     "cities": "Macon",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "GA",
                     "stateProvinceDistrictName": "Georgia"
                     },
             "479": {
                     "areaCode": "479",
                     "cities": "Fort Smith",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "AR",
                     "stateProvinceDistrictName": "Arkansas"
                     },
             "480": {
                     "areaCode": "480",
                     "cities": "Scottsdale",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "AZ",
                     "stateProvinceDistrictName": "Arizona"
                     },
             "484": {
                     "areaCode": "484",
                     "cities": "Allentown",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "PA",
                     "stateProvinceDistrictName": "Pennsylvania"
                     },
             "501": {
                     "areaCode": "501",
                     "cities": "Little Rock",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "AR",
                     "stateProvinceDistrictName": "Arkansas"
                     },
             "502": {
                     "areaCode": "502",
                     "cities": "Louisiville",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "KY",
                     "stateProvinceDistrictName": "Kentucky"
                     },
             "503": {
                     "areaCode": "503",
                     "cities": "Portland",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "OR",
                     "stateProvinceDistrictName": "Oregon"
                     },
             "504": {
                     "areaCode": "504",
                     "cities": "New Orleans metropolitan area",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "LA",
                     "stateProvinceDistrictName": "Louisiana"
                     },
             "505": {
                     "areaCode": "505",
                     "cities": "Albuquerque",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NM",
                     "stateProvinceDistrictName": "New Mexico"
                     },
             "506": {
                     "areaCode": "506",
                     "cities": "",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "NB",
                     "stateProvinceDistrictName": "New Brunswick"
                     },
             "507": {
                     "areaCode": "507",
                     "cities": "Rochester",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MN",
                     "stateProvinceDistrictName": "Minnesota"
                     },
             "508": {
                     "areaCode": "508",
                     "cities": "Worcester",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MA",
                     "stateProvinceDistrictName": "Massachusetts"
                     },
             "509": {
                     "areaCode": "509",
                     "cities": "Spokane",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "WA",
                     "stateProvinceDistrictName": "Washington"
                     },
             "510": {
                     "areaCode": "510",
                     "cities": "Oakland",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "512": {
                     "areaCode": "512",
                     "cities": "Austin",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "513": {
                     "areaCode": "513",
                     "cities": "Cincinnati",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "OH",
                     "stateProvinceDistrictName": "Ohio"
                     },
             "514": {
                     "areaCode": "514",
                     "cities": "Island of Montreal",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "QC",
                     "stateProvinceDistrictName": "Quebec"
                     },
             "515": {
                     "areaCode": "515",
                     "cities": "Des Moines",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IA",
                     "stateProvinceDistrictName": "Iowa"
                     },
             "516": {
                     "areaCode": "516",
                     "cities": "Nassau County",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NY",
                     "stateProvinceDistrictName": "New York"
                     },
             "517": {
                     "areaCode": "517",
                     "cities": "Lansing",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MI",
                     "stateProvinceDistrictName": "Michigan"
                     },
             "518": {
                     "areaCode": "518",
                     "cities": "Albany",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NY",
                     "stateProvinceDistrictName": "New York"
                     },
             "519": {
                     "areaCode": "519",
                     "cities": "London",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "ON",
                     "stateProvinceDistrictName": "Ontario"
                     },
             "520": {
                     "areaCode": "520",
                     "cities": "Tucson",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "AZ",
                     "stateProvinceDistrictName": "Arizona"
                     },
             "530": {
                     "areaCode": "530",
                     "cities": "Redding",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "531": {
                     "areaCode": "531",
                     "cities": "Omaha",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NE",
                     "stateProvinceDistrictName": "Nebraska"
                     },
             "534": {
                     "areaCode": "534",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "WI",
                     "stateProvinceDistrictName": "Wisconsin"
                     },
             "539": {
                     "areaCode": "539",
                     "cities": "Tulsa",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "OK",
                     "stateProvinceDistrictName": "Oklahoma"
                     },
             "540": {
                     "areaCode": "540",
                     "cities": "Fredericksburg",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "VA",
                     "stateProvinceDistrictName": "Virginia"
                     },
             "541": {
                     "areaCode": "541",
                     "cities": "Eugene",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "OR",
                     "stateProvinceDistrictName": "Oregon"
                     },
             "551": {
                     "areaCode": "551",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NJ",
                     "stateProvinceDistrictName": "New Jersey"
                     },
             "559": {
                     "areaCode": "559",
                     "cities": "Fresno",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "561": {
                     "areaCode": "561",
                     "cities": "Palm Beach County",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "FL",
                     "stateProvinceDistrictName": "Florida"
                     },
             "562": {
                     "areaCode": "562",
                     "cities": "Long Beach",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "563": {
                     "areaCode": "563",
                     "cities": "Davenport",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IA",
                     "stateProvinceDistrictName": "Iowa"
                     },
             "564": {
                     "areaCode": "564",
                     "cities": "Western Washington",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "WA",
                     "stateProvinceDistrictName": "Washington"
                     },
             "567": {
                     "areaCode": "567",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "OH",
                     "stateProvinceDistrictName": "Ohio"
                     },
             "570": {
                     "areaCode": "570",
                     "cities": "Scranton",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "PA",
                     "stateProvinceDistrictName": "Pennsylvania"
                     },
             "571": {
                     "areaCode": "571",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "VA",
                     "stateProvinceDistrictName": "Virginia"
                     },
             "573": {
                     "areaCode": "573",
                     "cities": "Columbia",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MO",
                     "stateProvinceDistrictName": "Missouri"
                     },
             "574": {
                     "areaCode": "574",
                     "cities": "South Bend",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IN",
                     "stateProvinceDistrictName": "Indiana"
                     },
             "575": {
                     "areaCode": "575",
                     "cities": "Las Cruces",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NM",
                     "stateProvinceDistrictName": "New Mexico"
                     },
             "579": {
                     "areaCode": "579",
                     "cities": "Laval",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "QC",
                     "stateProvinceDistrictName": "Quebec"
                     },
             "580": {
                     "areaCode": "580",
                     "cities": "Ponca City",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "OK",
                     "stateProvinceDistrictName": "Oklahoma"
                     },
             "581": {
                     "areaCode": "581",
                     "cities": "",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "QC",
                     "stateProvinceDistrictName": "Quebec"
                     },
             "582": {
                     "areaCode": "582",
                     "cities": "Erie",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "PA",
                     "stateProvinceDistrictName": "Pennsylvania"
                     },
             "585": {
                     "areaCode": "585",
                     "cities": "Rochester",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NY",
                     "stateProvinceDistrictName": "New York"
                     },
             "586": {
                     "areaCode": "586",
                     "cities": "Warren",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MI",
                     "stateProvinceDistrictName": "Michigan"
                     },
             "587": {
                     "areaCode": "587",
                     "cities": "",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "AB",
                     "stateProvinceDistrictName": "Alberta"
                     },
             "601": {
                     "areaCode": "601",
                     "cities": "Jackson",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MS",
                     "stateProvinceDistrictName": "Mississippi"
                     },
             "602": {
                     "areaCode": "602",
                     "cities": "Downtown Phoenix",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "AZ",
                     "stateProvinceDistrictName": "Arizona"
                     },
             "603": {
                     "areaCode": "603",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NH",
                     "stateProvinceDistrictName": "New Hampshire"
                     },
             "604": {
                     "areaCode": "604",
                     "cities": "Greater Vancouver Regional District",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "BC",
                     "stateProvinceDistrictName": "British Columbia"
                     },
             "605": {
                     "areaCode": "605",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "SD",
                     "stateProvinceDistrictName": "South Dakota"
                     },
             "606": {
                     "areaCode": "606",
                     "cities": "London",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "KY",
                     "stateProvinceDistrictName": "Kentucky"
                     },
             "607": {
                     "areaCode": "607",
                     "cities": "Binghamton",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NY",
                     "stateProvinceDistrictName": "New York"
                     },
             "608": {
                     "areaCode": "608",
                     "cities": "Madison",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "WI",
                     "stateProvinceDistrictName": "Wisconsin"
                     },
             "609": {
                     "areaCode": "609",
                     "cities": "Trenton",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NJ",
                     "stateProvinceDistrictName": "New Jersey"
                     },
             "610": {
                     "areaCode": "610",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "PA",
                     "stateProvinceDistrictName": "Pennsylvania"
                     },
             "612": {
                     "areaCode": "612",
                     "cities": "Minneapolis",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MN",
                     "stateProvinceDistrictName": "Minnesota"
                     },
             "613": {
                     "areaCode": "613",
                     "cities": "Ottawa",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "ON",
                     "stateProvinceDistrictName": "Ontario"
                     },
             "614": {
                     "areaCode": "614",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "OH",
                     "stateProvinceDistrictName": "Ohio"
                     },
             "615": {
                     "areaCode": "615",
                     "cities": "Nashville",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TN",
                     "stateProvinceDistrictName": "Tennessee"
                     },
             "616": {
                     "areaCode": "616",
                     "cities": "Grand Rapids",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MI",
                     "stateProvinceDistrictName": "Michigan"
                     },
             "617": {
                     "areaCode": "617",
                     "cities": "Boston",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MA",
                     "stateProvinceDistrictName": "Massachusetts"
                     },
             "618": {
                     "areaCode": "618",
                     "cities": "Carbondale",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IL",
                     "stateProvinceDistrictName": "Illinois"
                     },
             "619": {
                     "areaCode": "619",
                     "cities": "San Diego, California",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "620": {
                     "areaCode": "620",
                     "cities": "Wichita Metropolitan Area",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "KS",
                     "stateProvinceDistrictName": "Kansas"
                     },
             "623": {
                     "areaCode": "623",
                     "cities": "Maricopa County",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "AZ",
                     "stateProvinceDistrictName": "Arizona"
                     },
             "626": {
                     "areaCode": "626",
                     "cities": "Pasadena",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "630": {
                     "areaCode": "630",
                     "cities": "Aurora",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IL",
                     "stateProvinceDistrictName": "Illinois"
                     },
             "631": {
                     "areaCode": "631",
                     "cities": "Suffolk County",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NY",
                     "stateProvinceDistrictName": "New York"
                     },
             "636": {
                     "areaCode": "636",
                     "cities": "St. Charles",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MO",
                     "stateProvinceDistrictName": "Missouri"
                     },
             "641": {
                     "areaCode": "641",
                     "cities": "Mason City",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IA",
                     "stateProvinceDistrictName": "Iowa"
                     },
             "646": {
                     "areaCode": "646",
                     "cities": "Borough of Manhattan",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NY",
                     "stateProvinceDistrictName": "New York"
                     },
             "647": {
                     "areaCode": "647",
                     "cities": "",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "ON",
                     "stateProvinceDistrictName": "Ontario"
                     },
             "649": {
                     "areaCode": "649",
                     "cities": "",
                     "countryAbbrev": "TC",
                     "countryCode": "796",
                     "stateProvinceDistrictAbbrev": "00",
                     "stateProvinceDistrictName": "Turks and Caicos"
                     },
             "650": {
                     "areaCode": "650",
                     "cities": "Palo Alto",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "651": {
                     "areaCode": "651",
                     "cities": "St. Paul",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MN",
                     "stateProvinceDistrictName": "Minnesota"
                     },
             "657": {
                     "areaCode": "657",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "660": {
                     "areaCode": "660",
                     "cities": "Sedalia",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MO",
                     "stateProvinceDistrictName": "Missouri"
                     },
             "661": {
                     "areaCode": "661",
                     "cities": "Bakersfield",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "662": {
                     "areaCode": "662",
                     "cities": "Tupelo",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MS",
                     "stateProvinceDistrictName": "Mississippi"
                     },
             "664": {
                     "areaCode": "664",
                     "cities": "",
                     "countryAbbrev": "MS",
                     "countryCode": "500",
                     "stateProvinceDistrictAbbrev": "00",
                     "stateProvinceDistrictName": "Montserrat"
                     },
             "670": {
                     "areaCode": "670",
                     "cities": "Commonwealth of the United States",
                     "countryAbbrev": "MP",
                     "countryCode": "580",
                     "stateProvinceDistrictAbbrev": "00",
                     "stateProvinceDistrictName": "Northern Mariana Islands"
                     },
             "671": {
                     "areaCode": "671",
                     "cities": "Andersen Air Force Base",
                     "countryAbbrev": "GU",
                     "countryCode": "316",
                     "stateProvinceDistrictAbbrev": "00",
                     "stateProvinceDistrictName": "Guam"
                     },
             "672": {
                     "areaCode": "672",
                     "cities": "",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "BC",
                     "stateProvinceDistrictName": "British Columbia"
                     },
             "678": {
                     "areaCode": "678",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "GA",
                     "stateProvinceDistrictName": "Georgia"
                     },
             "681": {
                     "areaCode": "681",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "WV",
                     "stateProvinceDistrictName": "West Virginia"
                     },
             "682": {
                     "areaCode": "682",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "684": {
                     "areaCode": "684",
                     "cities": "",
                     "countryAbbrev": "AS",
                     "countryCode": "16",
                     "stateProvinceDistrictAbbrev": "AS",
                     "stateProvinceDistrictName": "American Samoa"
                     },
             "701": {
                     "areaCode": "701",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "ND",
                     "stateProvinceDistrictName": "North Dakota"
                     },
             "702": {
                     "areaCode": "702",
                     "cities": "Clark County",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NV",
                     "stateProvinceDistrictName": "Nevada"
                     },
             "703": {
                     "areaCode": "703",
                     "cities": "Northern Virginia",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "VA",
                     "stateProvinceDistrictName": "Virginia"
                     },
             "704": {
                     "areaCode": "704",
                     "cities": "Charlotte",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NC",
                     "stateProvinceDistrictName": "North Carolina"
                     },
             "705": {
                     "areaCode": "705",
                     "cities": "Northeastern Ontario",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "ON",
                     "stateProvinceDistrictName": "Ontario"
                     },
             "706": {
                     "areaCode": "706",
                     "cities": "Augusta",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "GA",
                     "stateProvinceDistrictName": "Georgia"
                     },
             "707": {
                     "areaCode": "707",
                     "cities": "Vallejo",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "708": {
                     "areaCode": "708",
                     "cities": "Oak Park",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IL",
                     "stateProvinceDistrictName": "Illinois"
                     },
             "709": {
                     "areaCode": "709",
                     "cities": "",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "NL",
                     "stateProvinceDistrictName": "Newfoundland and Labrador"
                     },
             "712": {
                     "areaCode": "712",
                     "cities": "Sioux City",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IA",
                     "stateProvinceDistrictName": "Iowa"
                     },
             "713": {
                     "areaCode": "713",
                     "cities": "Houston",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "714": {
                     "areaCode": "714",
                     "cities": "Orange County",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "715": {
                     "areaCode": "715",
                     "cities": "Wausau",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "WI",
                     "stateProvinceDistrictName": "Wisconsin"
                     },
             "716": {
                     "areaCode": "716",
                     "cities": "Buffalo",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NY",
                     "stateProvinceDistrictName": "New York"
                     },
             "717": {
                     "areaCode": "717",
                     "cities": "Harrisburg",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "PA",
                     "stateProvinceDistrictName": "Pennsylvania"
                     },
             "718": {
                     "areaCode": "718",
                     "cities": "New York City",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NY",
                     "stateProvinceDistrictName": "New York"
                     },
             "719": {
                     "areaCode": "719",
                     "cities": "Colorado Springs",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CO",
                     "stateProvinceDistrictName": "Colorado"
                     },
             "720": {
                     "areaCode": "720",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CO",
                     "stateProvinceDistrictName": "Colorado"
                     },
             "721": {
                     "areaCode": "721",
                     "cities": "",
                     "countryAbbrev": "SX",
                     "countryCode": "920",
                     "stateProvinceDistrictAbbrev": "00",
                     "stateProvinceDistrictName": "Sint Maarten"
                     },
             "724": {
                     "areaCode": "724",
                     "cities": "Washington, Pa.",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "PA",
                     "stateProvinceDistrictName": "Pennsylvania"
                     },
             "727": {
                     "areaCode": "727",
                     "cities": "Pinellas County",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "FL",
                     "stateProvinceDistrictName": "Florida"
                     },
             "730": {
                     "areaCode": "730",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IL",
                     "stateProvinceDistrictName": "Illinois"
                     },
             "731": {
                     "areaCode": "731",
                     "cities": "West Tennessee",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TN",
                     "stateProvinceDistrictName": "Tennessee"
                     },
             "732": {
                     "areaCode": "732",
                     "cities": "New Brunswick",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NJ",
                     "stateProvinceDistrictName": "New Jersey"
                     },
             "734": {
                     "areaCode": "734",
                     "cities": "Ann Arbor",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MI",
                     "stateProvinceDistrictName": "Michigan"
                     },
             "740": {
                     "areaCode": "740",
                     "cities": "Columbus",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "OH",
                     "stateProvinceDistrictName": "Ohio"
                     },
             "747": {
                     "areaCode": "747",
                     "cities": "Los Angeles County",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "754": {
                     "areaCode": "754",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "FL",
                     "stateProvinceDistrictName": "Florida"
                     },
             "757": {
                     "areaCode": "757",
                     "cities": "Hampton Roads",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "VA",
                     "stateProvinceDistrictName": "Virginia"
                     },
             "758": {
                     "areaCode": "758",
                     "cities": "",
                     "countryAbbrev": "LC",
                     "countryCode": "662",
                     "stateProvinceDistrictAbbrev": "00",
                     "stateProvinceDistrictName": "Saint Lucia"
                     },
             "760": {
                     "areaCode": "760",
                     "cities": "San Bernardino County",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "762": {
                     "areaCode": "762",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "GA",
                     "stateProvinceDistrictName": "Georgia"
                     },
             "763": {
                     "areaCode": "763",
                     "cities": "Minneapolis",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MN",
                     "stateProvinceDistrictName": "Minnesota"
                     },
             "765": {
                     "areaCode": "765",
                     "cities": "Lafayette",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IN",
                     "stateProvinceDistrictName": "Indiana"
                     },
             "767": {
                     "areaCode": "767",
                     "cities": "",
                     "countryAbbrev": "DM",
                     "countryCode": "212",
                     "stateProvinceDistrictAbbrev": "00",
                     "stateProvinceDistrictName": "Dominica"
                     },
             "769": {
                     "areaCode": "769",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MS",
                     "stateProvinceDistrictName": "Mississippi"
                     },
             "770": {
                     "areaCode": "770",
                     "cities": "Marietta",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "GA",
                     "stateProvinceDistrictName": "Georgia"
                     },
             "772": {
                     "areaCode": "772",
                     "cities": "Fort Pierce",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "FL",
                     "stateProvinceDistrictName": "Florida"
                     },
             "773": {
                     "areaCode": "773",
                     "cities": "Chicago",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IL",
                     "stateProvinceDistrictName": "Illinois"
                     },
             "774": {
                     "areaCode": "774",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MA",
                     "stateProvinceDistrictName": "Massachusetts"
                     },
             "775": {
                     "areaCode": "775",
                     "cities": "Carson City",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NV",
                     "stateProvinceDistrictName": "Nevada"
                     },
             "778": {
                     "areaCode": "778",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "BC",
                     "stateProvinceDistrictName": "British Columbia"
                     },
             "779": {
                     "areaCode": "779",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IL",
                     "stateProvinceDistrictName": "Illinois"
                     },
             "780": {
                     "areaCode": "780",
                     "cities": "Edmonton",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "AB",
                     "stateProvinceDistrictName": "Alberta"
                     },
             "781": {
                     "areaCode": "781",
                     "cities": "Waltham",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MA",
                     "stateProvinceDistrictName": "Massachusetts"
                     },
             "784": {
                     "areaCode": "784",
                     "cities": "",
                     "countryAbbrev": "VC",
                     "countryCode": "670",
                     "stateProvinceDistrictAbbrev": "00",
                     "stateProvinceDistrictName": "Saint Vincent and the Grenadines"
                     },
             "785": {
                     "areaCode": "785",
                     "cities": "Topeka",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "KS",
                     "stateProvinceDistrictName": "Kansas"
                     },
             "786": {
                     "areaCode": "786",
                     "cities": "Miami-Dade County",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "FL",
                     "stateProvinceDistrictName": "Florida"
                     },
             "787": {
                     "areaCode": "787",
                     "cities": "",
                     "countryAbbrev": "PR",
                     "countryCode": "630",
                     "stateProvinceDistrictAbbrev": "PR",
                     "stateProvinceDistrictName": "Puerto Rico"
                     },
             "801": {
                     "areaCode": "801",
                     "cities": "Wasatch Front",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "UT",
                     "stateProvinceDistrictName": "Utah"
                     },
             "802": {
                     "areaCode": "802",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "VT",
                     "stateProvinceDistrictName": "Vermont"
                     },
             "803": {
                     "areaCode": "803",
                     "cities": "Columbia",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "SC",
                     "stateProvinceDistrictName": "South Carolina"
                     },
             "804": {
                     "areaCode": "804",
                     "cities": "Richmond Metropolitan Area",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "VA",
                     "stateProvinceDistrictName": "Virginia"
                     },
             "805": {
                     "areaCode": "805",
                     "cities": "Ventura County",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "806": {
                     "areaCode": "806",
                     "cities": "Lubbock",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "807": {
                     "areaCode": "807",
                     "cities": "Northwestern Ontario",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "ON",
                     "stateProvinceDistrictName": "Ontario"
                     },
             "808": {
                     "areaCode": "808",
                     "cities": "Midway Atoll",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "HI",
                     "stateProvinceDistrictName": "Hawaii"
                     },
             "809": {
                     "areaCode": "809",
                     "cities": "",
                     "countryAbbrev": "DO",
                     "countryCode": "214",
                     "stateProvinceDistrictAbbrev": "00",
                     "stateProvinceDistrictName": "Dominican Republic"
                     },
             "810": {
                     "areaCode": "810",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MI",
                     "stateProvinceDistrictName": "Michigan"
                     },
             "812": {
                     "areaCode": "812",
                     "cities": "Bloomington",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IN",
                     "stateProvinceDistrictName": "Indiana"
                     },
             "813": {
                     "areaCode": "813",
                     "cities": "Hillsborough County",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "FL",
                     "stateProvinceDistrictName": "Florida"
                     },
             "814": {
                     "areaCode": "814",
                     "cities": "Erie",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "PA",
                     "stateProvinceDistrictName": "Pennsylvania"
                     },
             "815": {
                     "areaCode": "815",
                     "cities": "Rockford",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IL",
                     "stateProvinceDistrictName": "Illinois"
                     },
             "816": {
                     "areaCode": "816",
                     "cities": "Kansas City",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MO",
                     "stateProvinceDistrictName": "Missouri"
                     },
             "817": {
                     "areaCode": "817",
                     "cities": "Fort Worth",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "818": {
                     "areaCode": "818",
                     "cities": "San Fernando Valley",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "819": {
                     "areaCode": "819",
                     "cities": "",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "QC",
                     "stateProvinceDistrictName": "Quebec"
                     },
             "828": {
                     "areaCode": "828",
                     "cities": "Asheville",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NC",
                     "stateProvinceDistrictName": "North Carolina"
                     },
             "829": {
                     "areaCode": "829",
                     "cities": "",
                     "countryAbbrev": "DO",
                     "countryCode": "214",
                     "stateProvinceDistrictAbbrev": "00",
                     "stateProvinceDistrictName": "Dominican Republic"
                     },
             "830": {
                     "areaCode": "830",
                     "cities": "Del Rio",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "831": {
                     "areaCode": "831",
                     "cities": "Monterey",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "832": {
                     "areaCode": "832",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "843": {
                     "areaCode": "843",
                     "cities": "Charleston",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "SC",
                     "stateProvinceDistrictName": "South Carolina"
                     },
             "845": {
                     "areaCode": "845",
                     "cities": "Poughkeepsie",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NY",
                     "stateProvinceDistrictName": "New York"
                     },
             "847": {
                     "areaCode": "847",
                     "cities": "Arlington Heights",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IL",
                     "stateProvinceDistrictName": "Illinois"
                     },
             "848": {
                     "areaCode": "848",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NJ",
                     "stateProvinceDistrictName": "New Jersey"
                     },
             "849": {
                     "areaCode": "849",
                     "cities": "",
                     "countryAbbrev": "DO",
                     "countryCode": "214",
                     "stateProvinceDistrictAbbrev": "00",
                     "stateProvinceDistrictName": "Dominican Republic"
                     },
             "850": {
                     "areaCode": "850",
                     "cities": "Pensacola",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "FL",
                     "stateProvinceDistrictName": "Florida"
                     },
             "856": {
                     "areaCode": "856",
                     "cities": "Cherry Hill",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NJ",
                     "stateProvinceDistrictName": "New Jersey"
                     },
             "857": {
                     "areaCode": "857",
                     "cities": "Boston",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MA",
                     "stateProvinceDistrictName": "Massachusetts"
                     },
             "858": {
                     "areaCode": "858",
                     "cities": "San Diego",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "859": {
                     "areaCode": "859",
                     "cities": "Lexington",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "KY",
                     "stateProvinceDistrictName": "Kentucky"
                     },
             "860": {
                     "areaCode": "860",
                     "cities": "Hartford",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CT",
                     "stateProvinceDistrictName": "Connecticut"
                     },
             "862": {
                     "areaCode": "862",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NJ",
                     "stateProvinceDistrictName": "New Jersey"
                     },
             "863": {
                     "areaCode": "863",
                     "cities": "Lakeland",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "FL",
                     "stateProvinceDistrictName": "Florida"
                     },
             "864": {
                     "areaCode": "864",
                     "cities": "Greenville",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "SC",
                     "stateProvinceDistrictName": "South Carolina"
                     },
             "865": {
                     "areaCode": "865",
                     "cities": "Knoxville",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TN",
                     "stateProvinceDistrictName": "Tennessee"
                     },
             "867": {
                     "areaCode": "867",
                     "cities": "Northwest Territories",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "YT",
                     "stateProvinceDistrictName": "Yukon"
                     },
             "868": {
                     "areaCode": "868",
                     "cities": "",
                     "countryAbbrev": "TT",
                     "countryCode": "780",
                     "stateProvinceDistrictAbbrev": "00",
                     "stateProvinceDistrictName": "Trinidad and Tobago"
                     },
             "869": {
                     "areaCode": "869",
                     "cities": "",
                     "countryAbbrev": "KN",
                     "countryCode": "659",
                     "stateProvinceDistrictAbbrev": "00",
                     "stateProvinceDistrictName": "Saint Kitts and Nevis"
                     },
             "870": {
                     "areaCode": "870",
                     "cities": "Texarkana",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "AR",
                     "stateProvinceDistrictName": "Arkansas"
                     },
             "872": {
                     "areaCode": "872",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "IL",
                     "stateProvinceDistrictName": "Illinois"
                     },
             "876": {
                     "areaCode": "876",
                     "cities": "",
                     "countryAbbrev": "JM",
                     "countryCode": "388",
                     "stateProvinceDistrictAbbrev": "00",
                     "stateProvinceDistrictName": "Jamaica"
                     },
             "878": {
                     "areaCode": "878",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "PA",
                     "stateProvinceDistrictName": "Pennsylvania"
                     },
             "901": {
                     "areaCode": "901",
                     "cities": "Memphis",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TN",
                     "stateProvinceDistrictName": "Tennessee"
                     },
             "902": {
                     "areaCode": "902",
                     "cities": "Prince Edward Island",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "NS",
                     "stateProvinceDistrictName": "Nova Scotia"
                     },
             "903": {
                     "areaCode": "903",
                     "cities": "Tyler",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "904": {
                     "areaCode": "904",
                     "cities": "Jacksonville",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "FL",
                     "stateProvinceDistrictName": "Florida"
                     },
             "905": {
                     "areaCode": "905",
                     "cities": "Niagara Falls Region",
                     "countryAbbrev": "CA",
                     "countryCode": "124",
                     "stateProvinceDistrictAbbrev": "ON",
                     "stateProvinceDistrictName": "Ontario"
                     },
             "906": {
                     "areaCode": "906",
                     "cities": "Upper Peninsula of Michigan",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MI",
                     "stateProvinceDistrictName": "Michigan"
                     },
             "907": {
                     "areaCode": "907",
                     "cities": "Anchorage",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "AK",
                     "stateProvinceDistrictName": "Alaska"
                     },
             "908": {
                     "areaCode": "908",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NJ",
                     "stateProvinceDistrictName": "New Jersey"
                     },
             "909": {
                     "areaCode": "909",
                     "cities": "San Bernardino County",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "910": {
                     "areaCode": "910",
                     "cities": "Fayetteville",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NC",
                     "stateProvinceDistrictName": "North Carolina"
                     },
             "912": {
                     "areaCode": "912",
                     "cities": "Savannah",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "GA",
                     "stateProvinceDistrictName": "Georgia"
                     },
             "913": {
                     "areaCode": "913",
                     "cities": "Kansas City, Kansas",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "KS",
                     "stateProvinceDistrictName": "Kansas"
                     },
             "914": {
                     "areaCode": "914",
                     "cities": "Westchester County",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NY",
                     "stateProvinceDistrictName": "New York"
                     },
             "915": {
                     "areaCode": "915",
                     "cities": "El Paso County",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "916": {
                     "areaCode": "916",
                     "cities": "Sacramento Metropolitan Area",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "917": {
                     "areaCode": "917",
                     "cities": "New York City",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NY",
                     "stateProvinceDistrictName": "New York"
                     },
             "918": {
                     "areaCode": "918",
                     "cities": "Tulsa",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "OK",
                     "stateProvinceDistrictName": "Oklahoma"
                     },
             "919": {
                     "areaCode": "919",
                     "cities": "Raleigh",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NC",
                     "stateProvinceDistrictName": "North Carolina"
                     },
             "920": {
                     "areaCode": "920",
                     "cities": "Green Bay",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "WI",
                     "stateProvinceDistrictName": "Wisconsin"
                     },
             "925": {
                     "areaCode": "925",
                     "cities": "Livermore",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "928": {
                     "areaCode": "928",
                     "cities": "Flagstaff",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "AZ",
                     "stateProvinceDistrictName": "Arizona"
                     },
             "929": {
                     "areaCode": "929",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NY",
                     "stateProvinceDistrictName": "New York"
                     },
             "931": {
                     "areaCode": "931",
                     "cities": "Middle Tennessee",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TN",
                     "stateProvinceDistrictName": "Tennessee"
                     },
             "936": {
                     "areaCode": "936",
                     "cities": "Nacogdoches",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "937": {
                     "areaCode": "937",
                     "cities": "Dayton",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "OH",
                     "stateProvinceDistrictName": "Ohio"
                     },
             "938": {
                     "areaCode": "938",
                     "cities": "Huntsville",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "AL",
                     "stateProvinceDistrictName": "Alabama"
                     },
             "939": {
                     "areaCode": "939",
                     "cities": "",
                     "countryAbbrev": "PR",
                     "countryCode": "630",
                     "stateProvinceDistrictAbbrev": "PR",
                     "stateProvinceDistrictName": "Puerto Rico"
                     },
             "940": {
                     "areaCode": "940",
                     "cities": "Denton",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "941": {
                     "areaCode": "941",
                     "cities": "Tampa Bay",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "FL",
                     "stateProvinceDistrictName": "Florida"
                     },
             "947": {
                     "areaCode": "947",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MI",
                     "stateProvinceDistrictName": "Michigan"
                     },
             "949": {
                     "areaCode": "949",
                     "cities": "Irvine",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "951": {
                     "areaCode": "951",
                     "cities": "Riverside County",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CA",
                     "stateProvinceDistrictName": "California"
                     },
             "952": {
                     "areaCode": "952",
                     "cities": "Bloomington",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MN",
                     "stateProvinceDistrictName": "Minnesota"
                     },
             "954": {
                     "areaCode": "954",
                     "cities": "Broward County",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "FL",
                     "stateProvinceDistrictName": "Florida"
                     },
             "956": {
                     "areaCode": "956",
                     "cities": "Laredo",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "959": {
                     "areaCode": "959",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CT",
                     "stateProvinceDistrictName": "Connecticut"
                     },
             "970": {
                     "areaCode": "970",
                     "cities": "Grand Junction",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "CO",
                     "stateProvinceDistrictName": "Colorado"
                     },
             "971": {
                     "areaCode": "971",
                     "cities": "Portland",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "OR",
                     "stateProvinceDistrictName": "Oregon"
                     },
             "972": {
                     "areaCode": "972",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "973": {
                     "areaCode": "973",
                     "cities": "Newark",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NJ",
                     "stateProvinceDistrictName": "New Jersey"
                     },
             "978": {
                     "areaCode": "978",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MA",
                     "stateProvinceDistrictName": "Massachusetts"
                     },
             "979": {
                     "areaCode": "979",
                     "cities": "College Station",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "TX",
                     "stateProvinceDistrictName": "Texas"
                     },
             "980": {
                     "areaCode": "980",
                     "cities": "",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "NC",
                     "stateProvinceDistrictName": "North Carolina"
                     },
             "985": {
                     "areaCode": "985",
                     "cities": "Houma",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "LA",
                     "stateProvinceDistrictName": "Louisiana"
                     },
             "989": {
                     "areaCode": "989",
                     "cities": "Bay City",
                     "countryAbbrev": "US",
                     "countryCode": "840",
                     "stateProvinceDistrictAbbrev": "MI",
                     "stateProvinceDistrictName": "Michigan"
                     }
             }


def loadAreaCodes():
  global AREACODES
  # from dig.extract.entity.telephone.areacode import AREACODES
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
    url = None
    processed = 0
    for line in sys.stdin:
        try:
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
                processed += 1
                print >> sys.stdout, "%s\t%s" % (url, js)
        except Exception as e:
            print >> sys.stderr, "dig.extract.entity.telephone.phone Exception [%s].  Last url was [%s]" % (str(e), url)
    print >> sys.stderr, "dig.extract.entity.telephone.phone processed %d records" % processed

# call main() if this is run as standalone
if __name__ == "__main__":
    sys.exit(main())
