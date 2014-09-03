#!/usr/bin/env ./dig/bin/python
# -*- coding: utf-8 -*-
# Filename: token.py

# also consider
#!/usr/bin/env python

'''
dig.extract.entity.digtoken
@author: Andrew Philpot
@version 0.0.1
'''

# adapted from wat.tool.wattok version 1.5
# NB apparently cannot call this token.py because it would shadow something already in $PYTHONPATH
# NB failure happens during import of util.py

VERSION = "0.0.1"
__version__ = VERSION

import sys, os, re
import simplejson as json
import argparse
import dig.pymod.util
from dig.pymod.util import interpretCmdLine
# for debug only
from dig.pymod.util import echo

# may be preferable to store this in /usr/share, etc.
# see nltk.download()
# may be preferable to use env var setting from shared .bashrc
os.environ['NLTK_DATA'] = '/opt/dig/env/nltk_data'
import nltk

class Tokenizer(object):
    def __init__(self, text):
        '''create DIG-customized tokenizer (adapted from wattok)'''        
        self.text = text

    # compiling here wrecks the re.sub in genTokens
    # entityRE = re.compile(r"(?:&#\d{2,5};|&gt;|&lt;|&quot;|&apos;)")
    entityRE = r"(?:&#\d{2,5};|&gt;|&lt;|&quot;|&apos;)"
    # so don't know if we can ever use this
    compiledEntityRe = re.compile(entityRE)

    # digitRE = re.compile(r"\d")

    # need maximal segments of &#\d{2,4};\s* 
    def genSegments(self, s):
        while len(s) > 0:
            m = re.search(r"\s*%s(?:\s*%s)*" % (Tokenizer.entityRE, Tokenizer.entityRE), s)
            if m:
                if m.start(0) == 0:
                    yield (True, m.group(0))
                    s = s[m.end(0):]
                else:
                    yield (False, s[0:m.start(0)])
                    yield (True, m.group(0))
                    s = s[m.end(0):]
            else:
                yield (False, s)
                s = ""
        
    # Some imperfect tokens created by above tokenizer joining at '.':
    # dirty.This
    # DAYS.......
    # But we would want to retain as single tokens:
    # 1.25
    # www.backpage.com
    # J.U.L.I.E (ideally)
    #
    # Propose:
    # If token contains period:
    #    If token contains two or more periods in a row:
    #       split at each group of 2+ periods, then call recursively on each segment
    #    Else if token contains digits:
    #       yield it
    #    Else if token contains ".com" (etc.) and/or "http" and/or "www"
    #       yield it
    #    Else split at each period    

    ellipsisRE = re.compile(r'''(.*?)(\.{2,})''')
    allperiodsRE = re.compile(r'''^\.+$''')
    digitsRE = re.compile('\d')
    urlRE = re.compile('.com|.net|.org|.xxx|.biz|.edu|.info|www|http')
    periodRE = re.compile('(.*?)(\.)')

    def genTokens(self):
        # use the new property
        string = self.text
        # set off w/space any entities that are butted up to preceding data
        string = re.sub(r'(?<!\s)(?P<entityref>%s)' % Tokenizer.entityRE, 
                      ' \g<entityref>',
                      string)
        # set off w/space any entities that are butted up to following data
        string = re.sub(r'(?P<entityref>%s)(?!\s)' % Tokenizer.entityRE,
                      '\g<entityref> ',
                      string)
        for (entities, segment) in self.genSegments(string):
            # print "SEGMENT: [%s %r]" % (entities,segment)
            segment = segment.strip()
            if entities:
                for entity in re.split(r'\s+',segment):
                    # print " ENTITY: [%s]" % entity;
                    yield entity
            else:
                sentences = nltk.sent_tokenize(segment)
                # correct for any embedded newlines (irrelevant?)
                sentences = [re.sub(r'[\n\t]+', ' ', sent).strip() for sent in sentences]
                # inexplicably, NLTK thinks big,red should be a single token
                sentences = [re.sub(r'\b,\b', ', ', sent) for sent in sentences]
                for runon in sentences:
                    for sentence in re.split(Tokenizer.ellipsisRE, runon):
                        # print "  SENTENCE: [%s]" % sentence
                        if sentence:
                            # may have some empty strings
                            if re.search(Tokenizer.allperiodsRE, sentence):
                                # may be all periods
                                yield sentence
                            else:
                                for tok in nltk.word_tokenize(sentence):
                                    # print "    TOK: [%s]" % tok
                                    if Tokenizer.digitsRE.search(tok) or Tokenizer.urlRE.search(tok):
                                        yield tok
                                    else:
                                        for subtok in re.split(Tokenizer.periodRE, tok):
                                            # may have some empty strings
                                            if subtok:
                                                yield subtok

# testLine = '''https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/bellingham.backpage.com/FemaleEscorts/120-morning-special-dont-miss-this-25/14910841\t"\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n  \r\n  \r\n  \r\n  <!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.01//EN\" \"http://www.w3.org/TR/html4/strict.dtd\">\r\n    <!--[if lte IE 7]> <html class=\"ie7\" lang-\"en-us\"> <![endif]-->  \r\n    <!--[if IE 8]>     <html class=\"ie8\" lang=\"en-us\"> <![endif]-->  \r\n    <!--[if IE 9]>     <html class=\"ie9\" lang=\"en-us\"> <![endif]-->  \r\n    <!--[if !IE]><!--> <html lang=\"en-us\">             <!--<![endif]-->\r\n\r\n    <head>\r\n      <title>$120 Morning Special!! Dont miss this! - bellingham escorts - backpage.com</title>\r\n      <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\r\n      <meta name=\"keywords\" content=\"Bellingham, bell/blaine/outcall, $120 Morning Special!! Dont miss this!\">\r\n      <meta name=\"description\" content=\"Bellingham. bell/blaine/outcall. $120 Morning Special!! Dont miss this! - 25\">\r\n\r\n      \r\n      \r\n        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\r\n      \r\n      \r\n      \r\n      \r\n      <link rel=\"stylesheet\" type=\"text/css\" href=\"http://bellingham.backpage.com/styles/Responsive.css?cb=22\">\r\n\r\n      \r\n      \r\n        <link rel=\"canonical\" href=\"14910841\" />\r\n      \r\n      \r\n            \r\n      <script type=\"text/javascript\" src=\"http://bellingham.backpage.com/scripts/jquery-1.7.2.min.js\"></script>\r\n  \r\n  <script type=\"text/javascript\" src=\"http://bellingham.backpage.com/scripts/global-compiled.js?3\"></script>\r\n    </head>\r\n\r\n    <body id=\"ViewAd\">\r\n  \r\n  \r\n  \r\n  \r\n\r\n\r\n  <!-- Google Tag Manager -->\r\n  <script>bpDataLayer=[];</script>\r\n  <noscript><iframe src=\"http://www.googletagmanager.com/ns.html?id=GTM-5KCSP8\"\r\n  height=\"0\" width=\"0\" style=\"display:none;visibility:hidden\"></iframe></noscript>\r\n  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\r\n  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],\r\n  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\r\n  '//www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\r\n  })(window,document,'script','bpDataLayer','GTM-5KCSP8');</script>\r\n  <!-- End Google Tag Manager -->\r\n\r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n    <div id=\"tlHeader\">\r\n    \r\n      \r\n      \r\n\r\n      <div id=\"logo\"><a href=\"http://bellingham.backpage.com/\" style=\"background-image:url(http://www.backpage.com/images/bp_logo_mobile.png);\">bellingham.backpage.com</a></div>\r\n      \r\n      \r\n      \r\n        <div id=\"postAdButton\">\r\n          <form name=\"formPost\" action=\"http://posting.bellingham.backpage.com/online/classifieds/PostAdPPI.html/bli/bellingham.backpage.com/\" method=\"get\">\r\n      <input type=\"submit\" value=\"Post an Ad\" class=\"button\" id=\"postAdButton\">\r\n      <input type=\"hidden\" name=\"section\" value=\"4381\">\r\n      <input type=\"hidden\" name=\"category\" value=\"4443\">\r\n      <input type=\"hidden\" name=\"u\" value=\"bli\">\r\n      <input type=\"hidden\" name=\"serverName\" value=\"bellingham.backpage.com\">\r\n    </form>\r\n        </div><!-- #postAdButton -->\r\n\r\n        \r\n      \r\n\r\n      <div id=\"community\">\r\n        \r\n          <span class=\"city\">bellingham,\u00a0wa</span>&nbsp;<span class=\"comm\">free&nbsp;classifieds</span>\r\n        \r\n      </div><!-- #community -->\r\n\r\n      \r\n      \r\n    </div><!-- #tlHeader -->\r\n  \r\n\r\n  <div id=\"pageBackground\" style=\"clear:both;\">\r\n\r\n  \r\n    <div id=\"cookieCrumb\">\r\n      <a href=\"http://bellingham.backpage.com/\">backpage.com</a> &gt; <a href=\"http://bellingham.backpage.com/adult/\">bellingham adult entertainment</a> &gt; <a href=\"../index.html\">bellingham escorts</a>\r\n    </div>\r\n    \r\n    \r\n    <div class=\"mainBody\">\r\n\r\n  \r\n\r\n  \r\n \r\n  \r\n        \r\n    \r\n\r\n    \r\n    <br>\r\n    <div id=\"postingTitle\">\r\n    \r\n      <a style=\"float:right;clear:right;\" href=\"http://posting.bellingham.backpage.com/online/classifieds/ReportAd?oid=14910841\">Report Ad</a>\r\n    \r\n    \r\n      <a class=\"h1link\" href=\"javascript:void;\"><h1>$120 Morning Special!! Dont miss this! - 25</h1></a>\r\n    \r\n  </div>\r\n\r\n  <div class=\"adInfo\">\r\n    Posted: \r\n    Wednesday, December 18, 2013 10:17 AM\r\n  </div>\r\n  \r\n    <hr noshade>\r\n  \r\n  \r\n  \r\n    \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n  \r\n\r\n  \r\n  \r\n  \r\n\r\n\r\n  \r\n\r\n  \r\n    \r\n      <p class=\"replyDisplay\">\r\n        <b>Reply</b>:&nbsp;<a href=\"http://posting.bellingham.backpage.com/FemaleEscorts/classifieds/Reply?oid=14910841\">click here</a>\r\n      </p>\r\n    \r\n  \r\n\r\n\r\n  \r\n\r\n  \r\n\r\n\r\n  \r\n\r\n  \r\n\r\n  \r\n    <style>\r\n    <!-- \r\n      #viewAdPhotoLayout {\r\n        float:right;\r\n        margin:0 0 1em 1em;\r\n        padding:0;\r\n      }\r\n        #viewAdPhotoLayout li {\r\n          //display:inline-block;\r\n          list-style-type:none;\r\n          margin:0;\r\n          padding:0.75em;\r\n          background:#eee;\r\n          text-align:center;\r\n          overflow:hidden;\r\n          -webkit-column-break-inside: avoid;\r\n          -moz-column-break-inside: avoid; \r\n          -ms-column-break-inside: avoid; \r\n          break-inside: avoid; \r\n          \r\n        }\r\n          #viewAdPhotoLayout img {\r\n            margin-bottom:0.25em;\r\n          }\r\n          #viewAdPhotoLayout li a {\r\n            color:#000;\r\n          }\r\n    // -->\r\n    </style>\r\n    <!--[if gt IE 9]> -->\r\n    <style>\r\n    <!-- \r\n      #viewAdPhotoLayout.fivePlus {\r\n        width:465px;\r\n        -moz-column-count:2;\r\n        -webkit-column-count:2;\r\n        column-count:2;\r\n        -moz-column-gap:1.5em;\r\n        -webkit-column-gap:1.5em;\r\n        column-gap:1.5em;\r\n        column-fill: auto;\r\n      }\r\n      #viewAdPhotoLayout.ninePlus {\r\n        width:708px;\r\n        -moz-column-count:3;\r\n        -webkit-column-count:3;\r\n        column-count:3;\r\n        -moz-column-gap:1.5em;\r\n        -webkit-column-gap:1.5em;\r\n        column-gap:1.5em;\r\n        column-fill: auto;\r\n      }\r\n    // -->\r\n    </style>\r\n    <!-- <![endif]-->\r\n\r\n    \r\n    \r\n    <ul id=\"viewAdPhotoLayout\" class=\"fivePlus\">\r\n      \r\n        \r\n          \r\n            <li><img src=\"../../../images1.backpage.com/imager/u/medium/106356692/GetAttachment-14.jpg\" width=\"96\" height=\"158\" alt=\"$120 Morning Special!! Dont miss this! - 25\" title=\"$120 Morning Special!! Dont miss this! - 25\" border=\"0\"></li>\r\n          \r\n        \r\n          \r\n            <li><img src=\"../../../images3.backpage.com/imager/u/medium/106356694/GetAttachment-9.jpg\" width=\"107\" height=\"158\" alt=\"$120 Morning Special!! Dont miss this! - 25\" title=\"$120 Morning Special!! Dont miss this! - 25\" border=\"0\"></li>\r\n          \r\n        \r\n          \r\n            <li><img src=\"../../../images1.backpage.com/imager/u/medium/106356695/GetAttachment-11.jpg\" width=\"128\" height=\"159\" alt=\"$120 Morning Special!! Dont miss this! - 25\" title=\"$120 Morning Special!! Dont miss this! - 25\" border=\"0\"></li>\r\n          \r\n        \r\n          \r\n            <li><img src=\"../../../images2.backpage.com/imager/u/medium/106356697/GetAttachment-3.jpg\" width=\"127\" height=\"159\" alt=\"$120 Morning Special!! Dont miss this! - 25\" title=\"$120 Morning Special!! Dont miss this! - 25\" border=\"0\"></li>\r\n          \r\n        \r\n          \r\n            <li><img src=\"../../../images2.backpage.com/imager/u/medium/106356699/GetAttachment-4.jpg\" width=\"127\" height=\"159\" alt=\"$120 Morning Special!! Dont miss this! - 25\" title=\"$120 Morning Special!! Dont miss this! - 25\" border=\"0\"></li>\r\n          \r\n        \r\n          \r\n            <li><img src=\"../../../images3.backpage.com/imager/u/medium/106356700/GetAttachment-1.jpg\" width=\"127\" height=\"159\" alt=\"$120 Morning Special!! Dont miss this! - 25\" title=\"$120 Morning Special!! Dont miss this! - 25\" border=\"0\"></li>\r\n          \r\n        \r\n          \r\n            <li><img src=\"../../../images1.backpage.com/imager/u/medium/106356701/GetAttachment-7.jpg\" width=\"119\" height=\"159\" alt=\"$120 Morning Special!! Dont miss this! - 25\" title=\"$120 Morning Special!! Dont miss this! - 25\" border=\"0\"></li>\r\n          \r\n        \r\n          \r\n            <li><img src=\"../../../images2.backpage.com/imager/u/medium/106356702/GetAttachment-20.jpg\" width=\"119\" height=\"159\" alt=\"$120 Morning Special!! Dont miss this! - 25\" title=\"$120 Morning Special!! Dont miss this! - 25\" border=\"0\"></li>\r\n          \r\n        \r\n      \r\n    </ul><!-- #viewAdPhotoLayout -->\r\n  \r\n\r\n  <div class=\"posting\">\r\n    <div class=\"postingBody\">\r\n      \r\n        \r\n        \r\n          Hello gentlemen I'm back in town and for those of you who know me know I'm great at what I do!!.. for those of you who don't know me then ley me tell I'm a sexxy petite Burnett with a cuddly personality that you can't resist! !.. my pics are 100% real so if u like what you see call me now and set up sum time with the best!: 702-539-3220. From 8am-noon I'm having a $120 morningbspecial!!\r\n        \r\n      \r\n    </div>\r\n\r\n      \r\n      <p class=\"metaInfoDisplay\">Poster's age: 25<br></p>\r\n    \r\n\r\n    \r\n\r\n    \r\n      <div style=\"padding-left:2em;\">\r\n        &bull; Location: \r\n        \r\n          Bellingham, bell/blaine/outcall\r\n        \r\n      </div>\r\n    \r\n\r\n\r\n    \r\n      \r\n\r\n      \r\n      \r\n      <div style=\"padding-left:2em;\"><br />&bull; Post ID: 14910841 bellingham</div>\r\n\r\n      \r\n        <div id=\"OtherAdsByThisUser\" data-oid=\"14910841\">\r\n          <noscript>\r\n            \r\n          </noscript>\r\n        </div>\r\n        <script type=\"text/javascript\">\r\n          <!--\r\n          jQuery(\"#OtherAdsByThisUser\").loadOtherAdsByThisUser();\r\n          // -->\r\n        </script>\r\n      \r\n    \r\n\r\n\r\n    \r\n      <div class=\"helperLinks\" style=\"margin:2em 0;\">\r\n        <span style=\"font-weight:bold;\"><a href=\"http://posting.bellingham.backpage.com/FemaleEscorts/classifieds/EmailAd?oid=14910841\">Email this ad</a></span><br>\r\n      </div>\r\n    \r\n\r\n    \r\n\r\n  </div> <!-- .posting -->\r\n  \r\n\r\n  \r\n\r\n  \r\n  \r\n  \r\n  \r\n\r\n  \r\n  \r\n  <div style=\"clear:both;\"></div>\r\n    </div>\r\n    <!-- .mainBody -->\r\n  \r\n  \r\n  \r\n  \r\n    <script type=\"text/javascript\">\r\n    <!--\r\n      setCookie(\"site\",\"bellingham.backpage.com\",30,\"backpage.com\");\r\n    // -->\r\n    </script>\r\n  \r\n\r\n  <div id=\"tlFooter\">\r\n    <div class=\"footerText\">\r\n      \r\n        <a href=\"https://my.backpage.com/\">Account Login</a> |\r\n      \r\n\r\n      \r\n        <a href=\"http://www.backpage.com/classifieds/affiliates/index\">Affiliate Program</a> |\r\n        <a href=\"http://www.backpage.com/classifieds/affiliates/PromoteUs\">Promote Us</a>  |\r\n      \r\n  \r\n      \r\n\r\n      <a href=\"http://bellingham.backpage.com/online/Help\">Help</a> |\r\n      <a href=\"http://bellingham.backpage.com/online/PrivacyPolicy\">Privacy Policy</a> |\r\n      <a href=\"http://bellingham.backpage.com/online/TermsOfUse\">Terms of Use</a> |\r\n      <a href=\"http://bellingham.backpage.com/online/UserSafety\">User Safety</a> |\r\n\r\n      \r\n      \r\n      \r\n        <a href=\"http://bellingham.backpage.com/classifieds/AllCities\">backpage.com</a> \r\n      \r\n\r\n      &nbsp;&copy;&nbsp;Copyright&nbsp;2014\r\n    </div><!-- .footerText -->\r\n\r\n    <div class=\"footerDisclaimer\">\r\n      bellingham.backpage.com is an interactive computer service that enables access by multiple users and should not be treated as the publisher or speaker of any information provided by another information content provider.\r\n    </div><!-- .footerDisclaimer -->\r\n  </div><!-- #tlFooter -->\r\n\r\n  </div><!-- #pageBackground -->\r\n  \r\n  \r\n\r\n  \r\n    </body>\r\n    </html>\r\n  \r\n\r\n'''

def main(argv=None):
    '''this is called if run from command line'''
    (prog, args) = interpretCmdLine()
    parser = argparse.ArgumentParser(prog, description='Token Number Extractor')
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
                titleText = post.get('titleText')
                if titleText and titleText.get('content'):
                    tzr = Tokenizer(titleText['content'])
                    titleText['tokens'] = [t for t in tzr.genTokens()]
                else:
                    print >> sys.stderr, "No location text for %r" % url
                locationText = post.get('locationText')
                if locationText and locationText.get('content'):
                    tzr = Tokenizer(locationText['content'])
                    locationText['tokens'] = [t for t in tzr.genTokens()]
                else:
                    print >> sys.stderr, "No title text for %r" % url
                bodyText = post.get('bodyText')
                if bodyText and bodyText.get('content'):
                    tzr = Tokenizer(bodyText['content'])
                    bodyText['tokens'] = [t for t in tzr.genTokens()]
                else:
                    print >> sys.stderr, "No body text for %r" % url
            js = json.dumps(post, sort_keys=True, indent=None)
            print >> sys.stdout, "%s\t%s" % (url, js)

# call main() if this is run as standalone
if __name__ == "__main__":
    sys.exit(main())
