from azure import *
from azure.storage import *
import os
import urllib2
import util
from util import elapsed, genDatestamps
from glob import iglob
import subprocess
import shutil
# from hadoop.io.SequenceFile import CompressionType
from hadoop.io import Text
from hadoop.io import SequenceFile
import datetime
import simplejson as json
import re

# corresponds to r25784 from memex/toddler svn repository

# The following code creates a BlobService object using the storage
# account name and account key. Replace 'myaccount' and 'mykey' with
# the real account and key.

myaccount="karmadigstorage"
mykey="TJbdTjRymbBHXLsDtF/Nx3+6WXWN0uwh3RG/8GPJQRQyqg+rkOzioczm5czPtr+auGFhNeBx8GTAfuCufRyw8A=="
mycontainer='arch'

bs = BlobService(account_name=myaccount, account_key=mykey)
#bs.create_container(mycontainer)
#bs.set_container_acl(mycontainer, x_ms_blob_public_access='container')

CRAWLAGENTS= ["churl",
              "core042",
              "core043",
              "core044",
              "crawl061",
              "crawl071",
              "crawl072",
              "crawl073",
              "crawl074",
              "crawl081",
              "crawl082",
              "crawl083",
              "crawl084",
              "crawl091",
              "crawl101",
              "crawl102",
              "crawl103",
              "crawl104",
              "crawl131",
              "crawl132",
              "crawl133",
              "crawl134",
              "crawl135",
              "crawl136",
              "crawl137",
              "data051",
              "dixiechicks",
              "karma-dig-1",
              "karma-dig-2",
              "karma-dig-3",
              "karma-dig-4",
              "keep",
              "master041",
              "memex204",
              "sigma",
              "studio",
              "thrall01",
              "thrall02",
              "thrall03",
              "thrall04",
              "ubirr",
              "vassal01",
              "vassal02",
              "vassal03",
              "vassal04",
              "wat011",
              "wat012",
              "wat013",
              "wat015",
              "wat021",
              "wat022",
              "wat026",
              "wat027",
              "wat028",
              "wat029",
              "wat031",
              "wat032",
              "wat033",
              "wat034",
              "wat035",
              "wat036"]

DATESTAMPS = [ds for ds in genDatestamps(start=20140101, end=20140201)]
DATESTAMPS = [ds for ds in genDatestamps(start=20140101, end=20140103)]
DATESTAMPS = [ds for ds in genDatestamps(start=20130101, end=20141231)]

SITEKEYS = True

def downloadBackpageAds(datestamps=DATESTAMPS, crawlAgents=CRAWLAGENTS):
    start = datetime.datetime.now()
    for ds in datestamps:
        for crawlAgent in crawlAgents:
            url = "http://wat.s3-us-gov-west-1.amazonaws.com/data/escort/crawl/%s__%s.tgz" % (crawlAgent, ds)
            dailyDir = os.path.join("/home/philpot/arch", crawlAgent, str(ds))
            if os.path.isdir(dailyDir):
                print "already fetched dir %s" % dailyDir
            else:
                downloadTo = os.path.join("/home/philpot/arch", crawlAgent, "%s__%s.tgz" % (crawlAgent, ds))
                util.ensureDirectoriesExist(downloadTo)
                if util.checkUrl(url):
                    print >> sys.stderr, "Fetch %s" % url
                    util.chunkedFetchUrl(url, downloadTo)
                    print >> sys.stderr, "Extract %s" % url
                    try:
                        subprocess.check_call(["tar", "x", "-z", "-C", os.path.join("/home/philpot/arch", crawlAgent), "-f", downloadTo])
                    except subprocess.CalledProcessError as e:
                        print >> sys.stderr, "Failed to extract from %s" % downloadTo
                    print >> sys.stderr, "Delete tarball %s" % downloadTo
                    os.remove(downloadTo)
                    print >> sys.stderr, "Drop images from %s" % (os.path.join("/home/philpot/arch", crawlAgent, str(ds)))
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), "images1.backpage.com"), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), "images2.backpage.com"), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), "images3.backpage.com"), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), "www..backpage.com"), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-alabama.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-albany.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-albuquerque.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-arizona.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-atlanta.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-austin.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-baltimore.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-biloxi.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-boston.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-buffalo.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-carolina.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-chicago.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-dallas.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-dc.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-denver.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-guide.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-hartford.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-hawaii.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-houston.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-indiana.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-kansascity.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-la.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-lasvegas.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-louisville.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-miami.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-michigan.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-minn.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-naples.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-nashville.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-nebraska.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-newjersey.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-nola.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-northflorida.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-ny.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-ohio.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-oklahoma.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-philly.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-pittsburgh.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-portland.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-providence.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-reno.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-sandiego.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-sanjose.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-seattle.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-stlouis.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-tampa.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-utah.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-virginia.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'cdn-w.eros-wisconsin.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-alabama.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-albany.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-albuquerque.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-arizona.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-atlanta.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-austin.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-baltimore.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-biloxi.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-boston.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-buffalo.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-carolina.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-chicago.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-dallas.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-dc.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-denver.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-guide.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-hartford.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-hawaii.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-houston.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-indiana.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-kansascity.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-la.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-lasvegas.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-louisville.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-miami.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-michigan.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-minn.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-naples.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-nashville.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-nebraska.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-newjersey.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-nola.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-northflorida.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-ny.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-ohio.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-oklahoma.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-philly.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-pittsburgh.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-portland.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-providence.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-reno.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-sandiego.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-sanjose.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-seattle.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-stlouis.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-tampa.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-utah.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-virginia.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.eros-wisconsin.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.cityvibe.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'images.cityvibe.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'classifieds.myredbook.com'), True)
                    shutil.rmtree(os.path.join("/home/philpot/arch", crawlAgent, str(ds), 'www.humaniplex.com'), True)
                else:
                    print >> sys.stderr, "No such URL %s" % url
    end = datetime.datetime.now()
    delta = end - start
    print >> sys.stderr, "ELAPSED downloadBackpageAds is %s" % elapsed(delta)

def dbpa(datestamps=DATESTAMPS, crawlAgents=CRAWLAGENTS):
    return downloadBackpageAds(datestamps=datestamps, crawlAgents=crawlAgents)

def download(datestamps=DATESTAMPS, crawlAgents=CRAWLAGENTS):
    return downloadBackpageAds(datestamps=datestamps, crawlAgents=crawlAgents)
            
def store(datestamps=DATESTAMPS, crawlAgents=CRAWLAGENTS, limit=sys.maxint):
    start = datetime.datetime.now()
    i=0
    remaining = limit
    for crawlAgent in crawlAgents:
        for datestamp in datestamps:
            for glob in iglob(os.path.join('/home/philpot/arch', crawlAgent, str(datestamp), '*.backpage.com', "FemaleEscorts")):
                sentinel = os.path.join(glob, "..", "PROCESSED")
                if os.path.isfile(sentinel):
                    print "skipping completed %s" % os.path.normpath(os.path.dirname(sentinel))
                else:
                    print "processing %s" % os.path.normpath(os.path.dirname(sentinel))
                    for root, dirnames, filenames in os.walk(glob):
                        for filename in filenames:
                            pathname = os.path.join(root, filename)
                            rel = os.path.relpath(pathname, start='/home/philpot/arch')
                            destination = urllib2.quote(rel)
                            # if limit < sys.maxint:
                            #     print "will store %s as %s (enc %s)" % (pathname, rel, destination)
                            #     print """bs.put_block_blob_from_path(%s, %s, %s, x_ms_blob_content_type='text/html')""" % (mycontainer, destination, pathname)

                            try:
                                bs.put_block_blob_from_path(mycontainer, destination, pathname,
                                                            x_ms_blob_content_type='text/html')
                            except WindowsAzureError as e:
                                print >> sys.stderr, "Azure failure [%r], skipping"
                            i += 1
                            if i%100 == 0:
                                print i
                            remaining -= 1
                            if remaining <= 0:
                                return
                    print "processed %s" % os.path.normpath(os.path.dirname(sentinel))
                    util.touch(sentinel)
                print "delete ads dir %s" % glob
                shutil.rmtree(glob)
    end = datetime.datetime.now()
    delta = end - start
    print >> sys.stderr, "ELAPSED store is %s" % elapsed(delta)

def downloadStore(datestamps=DATESTAMPS, crawlAgents=CRAWLAGENTS):
    start = datetime.datetime.now()
    for datestamp in datestamps:
        for crawlAgent in crawlAgents:
            download([datestamp],[crawlAgent])
            store([datestamp],[crawlAgent])
    end = datetime.datetime.now()
    delta = end - start
    print >> sys.stderr, "ELAPSED downloadStore is %s" % elapsed(delta)

# def listAll():
#     for blob in bs.list_blobs(mycontainer):
#         print blob.name, blob.url
#         # print "url", blob.url
#         # util.info(blob)
#         # util.info(blob.properties)

# def listAll2():
#     for blob in bs.list_blobs(mycontainer, prefix="thrall01"):
#         print blob.name, blob.url
#         # print "url", blob.url
#         # util.info(blob)
#         # util.info(blob.properties)

# compare
# http://stackoverflow.com/a/24303682/2077242


def listAll(prefix=None, outstream=sys.stdout):
    total = 0
    # bs = BlobService(account_name='<accountname>', account_key='<accountkey>')
    next_marker = None
    while True:
        try:
            blobs = bs.list_blobs(mycontainer, maxresults=5000, marker=next_marker, prefix=prefix)
        except WindowsAzureError as e:
            print >> sys.stderr, "Failed to fetch [%s], exiting" % prefix
            break
        next_marker = blobs.next_marker
        # print(next_marker)
        # print blobs[0].name
        total += len(blobs)
        for blob in blobs:
            try:
                print >> outstream, blob.url
            except WindowsAzureError as e:
                print >> sys.stderr, "Failed on %s, skipping" % blob
        if next_marker is None:
            break
    return total

def listByDatestamp(datestamp, crawlAgents=CRAWLAGENTS):
    total = 0
    with open('/tmp/%s.byDatestamp' % datestamp, 'w') as f:
        for crawlAgent in crawlAgents:
            size = listAll(prefix="%s/%s" % (crawlAgent, datestamp), outstream=f)
            total += size
    return total

def genBlobs(datestamps=DATESTAMPS, crawlAgents=CRAWLAGENTS, sitekeys=SITEKEYS):
    "List the matching blobs in container"
    for datestamp in datestamps:
        for crawlAgent in crawlAgents:
            prefix="%s/%s" % (crawlAgent, datestamp)
            next_marker = None
            while True:
                try:
                    blobs = bs.list_blobs(mycontainer, maxresults=5000, marker=next_marker, prefix=prefix)
                except WindowsAzureError as e:
                    print >> sys.stderr, "Failed to fetch [%s], exiting" % prefix
                    break
                next_marker = blobs.next_marker
                # we fetched the blobs, now iterate over it
                for blob in blobs:
                    try:
                        if sitekeys==[]:
                            yield blob
                        else:
                            m = re.match(r"""https://karmadigstorage.blob.core.windows.net/arch/(.*)/(\d{8})/(.*).backpage.com""", blob.url)
                            sitekey = m.group(3)
                            if sitekey in sitekeys:
                                yield blob
                    except WindowsAzureError as e:
                        print >> sys.stderr, "Failed on %s, skipping" % blob
                if next_marker is None:
                    break

def genUrls(datestamps=DATESTAMPS, crawlAgents=CRAWLAGENTS, sitekeys=SITEKEYS):
    for blob in genBlobs(datestamps=datestamps, crawlAgents=crawlAgents, sitekeys=sitekeys):
        yield blob.url

def materializeUrls(urls, destFile, sequence=True):
    start = datetime.datetime.now()
    if sequence:
        writer = SequenceFile.createWriter(destFile, Text, Text)
    else:
        writer = open(destFile, 'w')
    for url in urls:
        if sequence:
            key = Text()
            key.set(url)
            value = Text()
            # I'm not at all sure why we would want to decode, not encode here
            # this is the only thing that worked
            value.set(Text.decode(json.dumps(util.chunkedFetchUrlText(url))))
            writer.append(key, value)
        else:
            key = url
            value = json.dumps(util.chunkedFetchUrlText(url))
            line = "%s\t%s" % (url, value)
            print >> writer, line
    writer.close()
    end = datetime.datetime.now()
    delta = end - start
    print >> sys.stderr, "ELAPSED materializeUrls is %s" % elapsed(delta)

def materializeTextUrls(urls, destFile, sequence=True):
    start = datetime.datetime.now()
    if sequence:
        writer = SequenceFile.createWriter(destFile, Text, Text)
    else:
        writer = open(destFile, 'w')
    for url in urls:
        if sequence:
            key = Text()
            key.set(url)
            value = Text()
            # I'm not at all sure why we would want to decode, not encode here
            # this is the only thing that worked
            value.set(Text.decode(json.dumps(util.chunkedFetchUrlText(url))))
            writer.append(key, value)
        else:
            key = url
            value = json.dumps(util.chunkedFetchUrlText(url))
            line = "%s\t%s" % (url, value)
            print >> writer, line
    writer.close()
    end = datetime.datetime.now()
    delta = end - start
    print >> sys.stderr, "ELAPSED materializeUrls is %s" % elapsed(delta)



testUrls=["https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/bellingham.backpage.com/FemaleEscorts/120-morning-special-dont-miss-this-25/14910841",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/bellingham.backpage.com/FemaleEscorts/160-incall-special-_w_a_y-_-_b_e_t_t_e_r_-160-24/9436459",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/bellingham.backpage.com/FemaleEscorts/andgtimply-amazing-pecials-21/15073501",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/bellingham.backpage.com/FemaleEscorts/andgtimply-amazing-pecials-available-247-21/15075819",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/bellingham.backpage.com/FemaleEscorts/are-you-looking-for-something-with-no-strings-attached/12995854",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/bellingham.backpage.com/FemaleEscorts/baby-girl-has-arrived-28/15056065",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/bellingham.backpage.com/FemaleEscorts/back-and-in-bel-100180-360-389-1455-22/14951600"]

nwUrls = []
# from dig.tool.data.nwurls import nwUrls

psUrls = []
psUrls = ["https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/gentlemens-choices-curvacious-frames-duo-specials-lacey-incall-all-the-curves-you-desire-21/14911153",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/misty-130-100-360-270-8143-my-home-and-arms-are-warm-44/5942490",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/only-in-town-for-the-nightyoung-blondeandlots-of-fun-go-home-feeling-like-u-won-5-22/14946777",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/olympia.backpage.com/FemaleEscorts/misty-130-100-360-270-8143-my-home-and-arms-are-warm-44/5942490",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/olympia.backpage.com/FemaleEscorts/only-in-town-for-the-nightyoung-blondeandlots-of-fun-go-home-feeling-like-u-won-5-22/14946777",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/olympia.backpage.com/FemaleEscorts/gentlemens-choices-curvacious-frames-duo-specials-lacey-incall-all-the-curves-you-desire-21/14911153",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/olympia.backpage.com/FemaleEscorts/misty-130-100-360-270-8143-my-home-and-arms-are-warm-44/5942490",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/your-gilr-next-door-new-asian-girlfriend-just-arrived-outcall-and-incall-22/15166708",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/r-u-a-mature-male-seeking-a-busty-seductive-blonde-30/15250952",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/sexy-asian-linda-your-tender-passionate-girlfriend-30/15046200",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/your-gilr-next-door-new-asian-girlfriend-just-arrived-outcall-and-incall-22/15166708",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/r-u-a-mature-male-seeking-a-busty-seductive-blonde-30/15250952",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/sexy-asian-linda-your-tender-passionate-girlfriend-30/15046200",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/sweet-and-sexy-blonde-25/14866049",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/your-gilr-next-door-new-asian-girlfriend-just-arrived-outcall-and-incall-22/15166708",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/bellingham.backpage.com/FemaleEscorts/gemini-in-mukilteo-severett-37/14912435",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/bellingham.backpage.com/FemaleEscorts/im-available-now360-202-3837-incall-or-outcall-i-want-it-too/14944987",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/bellingham.backpage.com/FemaleEscorts/gemini-in-mukilteo-severett-37/14912435",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/bellingham.backpage.com/FemaleEscorts/im-available-now360-202-3837-incall-or-outcall-i-want-it-too/14944987",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/bellingham.backpage.com/FemaleEscorts/geminiis-coming-back-to-bellingham-tonight-one-night-only-37/14912435",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/bellingham.backpage.com/FemaleEscorts/im-available-now360-202-3837-incall-or-outcall-i-want-it-too/14944987",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/huge-dds-double-your-pleasure-double-your-fun-sumner-incall-38/15115395",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/olympia.backpage.com/FemaleEscorts/hot-mami-exotic-erotic-new-in-town-30/15234917",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/olympia.backpage.com/FemaleEscorts/huge-dds-double-your-pleasure-double-your-fun-sumner-incall-38/15115395",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/olympia.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/olympia.backpage.com/FemaleEscorts/hot-mami-exotic-erotic-new-in-town-30/15234917",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/olympia.backpage.com/FemaleEscorts/huge-dds-double-your-pleasure-double-your-fun-sumner-incall-38/15115395",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/olympia.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/available-now-thick-mixed-puetro-rican-round-booty-natural-double-ds-ready-to-play-24/15255613",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/bran-new-girl-xmas-time-only-curvy-latina-24/15217760",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/brand-new-ebony-sexy-petite-treat-upscale-beauty-in-kent-21/15253174",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/crazy-skillspretty-fcjuicy-lips-simpy-the-best-20/15237208",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/curly-hair-caramel-melody-hott-exotic-playmate-2062182433-yummysexyy-d-ic-specials-21/14613451",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/available-now-thick-mixed-puetro-rican-round-booty-natural-double-ds-ready-to-play-24/15255613",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/brand-new-ebony-sexy-petite-treat-upscale-beauty-in-kent-21/15253174",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/crazy-skillspretty-fcjuicy-lips-simpy-the-best-20/15237208",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/curly-hair-caramel-melody-hott-exotic-playmate-2062182433-yummysexyy-d-ic-specials-21/14613451",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/dynamic-ddduo-busty-beautys-and-big-bootys-2-4-1-pecial-100-23/14438534",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/im-horny-hugeddds-double-ur-pleasure-double-ur-fun-monroe-incall-37/10877231",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/2-sweet-petite-freaks-you-would-love-to-meet-specials-specials-25/15125817",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/available-now-thick-mixed-puetro-rican-round-booty-natural-double-ds-ready-to-play-24/15255613",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/curly-hair-caramel-melody-hott-exotic-playmate-2062182433-yummysexyy-d-ic-specials-21/14613451",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/dynamic-ddduo-busty-beautys-and-big-bootys-2-4-1-pecial-100-23/14438534",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/im-horny-hugeddds-double-ur-pleasure-double-ur-fun-monroe-incall-37/10877231",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/andgt-double-click-here-new-years-eve-fun-andlt-33/15251055",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/blah-blahblah-blahblah-blahblah-blahblah-blah-33/15218820",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/come-play-with-this-double-dd-viet-princess-70-20/15148327",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/end-of-the-yr-special-2-girls-or-1-asia-and-kylee-andhearts-pleasure-experts-2-for-the-price-of-1-23/14835263",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/latenight-tacoma-incall-sexy-latinas-fetish-specials-21/15240608",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/start-your-new-year-off-right-with-double-trouble-30/15216272",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/100-new-years-tacoma-incall-sexy-latina-130hr-specials-21/15240608",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/2s-better-than-one-double-the-funstunning-hot-mami-exotic-and-erotic-filipino-30/15079246",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/andgt-double-click-here-new-years-eve-fun-andlt-33/15251055",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/blah-blahblah-blahblah-blahblah-blahblah-blah-33/15218820",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/come-play-with-this-double-dd-viet-princess-70-20/15148327",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/end-of-the-yr-special-2-girls-or-1-asia-and-kylee-andhearts-pleasure-experts-2-for-the-price-of-1-23/14835263",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/start-your-new-year-off-right-with-double-trouble-30/15216272",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/tacoma.backpage.com/FemaleEscorts/100hhr-tacoma-mall-incall-sexy-latina-150hr-all-night-21/15240608",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/tacoma.backpage.com/FemaleEscorts/2s-better-than-one-double-the-funstunning-hot-mami-exotic-and-erotic-filipino-30/15079246",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/tacoma.backpage.com/FemaleEscorts/andgt-double-click-here-new-years-eve-fun-andlt-33/15251055",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/tacoma.backpage.com/FemaleEscorts/blah-blahblah-blahblah-blahblah-blahblah-blah-33/15218820",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/bellingham.backpage.com/FemaleEscorts/rated-pleasure-x-service-27/15191058",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/bellingham.backpage.com/FemaleEscorts/rated-pleasure-x-service-27/15191058",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/bellingham.backpage.com/FemaleEscorts/rated-pleasure-x-service-27/15191058",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/4-tonightearly-moring-only-the-1-and-only-exocet-sharee-dont-miss-my-specials-military-specials-28/14973609",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/come-play-with-the-naughtiest-playmate-of-2013-24/14650613",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/craving-someone-like-me-available-now-23/15231708",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/happy-new-year-special-xoxo-sharee-28/15254576",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/take-a-first-class-trip-w-a-busty-brunette-into-2014-24/14873686",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/the-irresistible-chocolate-playmate-erotic-lil-mami-21/15039922",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/w-h-i-t-e-_g_r_l-sxy-little-treat-outcalls-4-you-120-22/11294142",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/olympia.backpage.com/FemaleEscorts/4-tonightearly-moring-only-the-1-and-only-exocet-sharee-dont-miss-my-specials-military-specials-28/14973609",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/olympia.backpage.com/FemaleEscorts/come-play-with-the-naughtiest-playmate-of-2013-24/14650613",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/olympia.backpage.com/FemaleEscorts/craving-someone-like-me-available-now-23/15231708",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/olympia.backpage.com/FemaleEscorts/happy-new-year-special-xoxo-sharee-28/15254576",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/olympia.backpage.com/FemaleEscorts/holiday-specials-amazing-busty-blonde-curvy-sexy-sweet-treat-well-reviewed-27/14832483",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/olympia.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/olympia.backpage.com/FemaleEscorts/take-a-first-class-trip-w-a-busty-brunette-into-2014-24/14873686",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/olympia.backpage.com/FemaleEscorts/the-irresistible-chocolate-playmate-erotic-lil-mami-21/15039922",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/olympia.backpage.com/FemaleEscorts/w-h-i-t-e-_g_r_l-sxy-little-treat-outcalls-4-you-120-22/11294142",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/olympia.backpage.com/FemaleEscorts/4-tonightearly-moring-only-the-1-and-only-exocet-sharee-dont-miss-my-specials-military-specials-28/14973609",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/olympia.backpage.com/FemaleEscorts/craving-someone-like-me-available-now-23/15231708",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/olympia.backpage.com/FemaleEscorts/happy-new-year-special-xoxo-sharee-28/15254576",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/olympia.backpage.com/FemaleEscorts/holiday-specials-amazing-busty-blonde-curvy-sexy-sweet-treat-well-reviewed-27/14832483",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/olympia.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/olympia.backpage.com/FemaleEscorts/the-irresistible-chocolate-playmate-erotic-lil-mami-21/15039922",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/olympia.backpage.com/FemaleEscorts/w-h-i-t-e-_g_r_l-sxy-little-treat-outcalls-4-you-120-22/11294142",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/angel-white-seductive-playmate-22/15253245",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/call-me-206-774-0664-sexy-korean-ruby-outcalls-only-22/14400095",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/crazy-h0t-white-classy-playmate-22/14805915",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/curly-hair-caramel-melody-hott-exotic-playmate-2062182433-yummysexyy-d-ic-specials-21/14613451",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/exclusive-erotic-hands-on-and-totally-unrushed-5-starr-touch-persian-24/15243823",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/exotic-petite-gorgeous-playmate-23/15249710",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/exotic-stunning-playmate-juicy-lips-and-curvy-hips-filipinospanish-20/15082504",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/extremely-hott-killer-body-real-pics-safe-and-discreet-24/15244140",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/hot-asian-classy-playmate-outcall-and-incall-22/15172622",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/lynnwood-flawless-super-hot-model-type-ebonyandasian-erotic-fun-25/7492224",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/mixed-exotic-playmate-avail-now-call-now-specials-22/15246117",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/new-asian-hot-body-call-me-206-774-0892-outcall-only-sexy-zora-23/15247861",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/new-beautiful-scandinavian-bombshell-100-spcl-247-21/14614142",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/new-discreet-adult-companion-andplaymate-beautiful-sexysweetfun-and-intelligent-too-26/15194583",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/new-playmate-in-town-specials-all-night-long-20/14823505",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/oo-naughty-never-looked-this-nice-oo-23/9964433",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/outcall-only-call-me-206-774-0892-hong-kong-sexy-zora-23/15254506",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/p-a-y-t-o-n-g-o-o-d-last-day-a-mouth-28/15228294",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/playmate-candy-shop-new-flavor-candy-red-w-new-sweet-tooth-special-23/15248863",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/rare-one-of-a-kind-playmate-they-say-a-pic-is-worth-a-thousand-words-click-here-for-special100fun-22/6709337",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/real-good-playmate-i-am-your-real-sexy-girl-real-pics-25/15112050",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/sexy-seductive-freak-available-all-night-specials-21/15237234",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/super-sexy-absoutly-stunning-blonde-playmate-21/15228813",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/visiting-sexy-hot-asian-girl-ready-to-please-you-come-join-youll-love-24/15045943",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/amazing-green-eyed-yummy-playmate-ready-2-play-100-real-pics-20/12480342",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/and-call-me-today-206-774-0892-hong-kong-sexy-zora-outcall-only-and-23/15259406",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/angel-white-seductive-playmate-22/15253245",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/c_a_t_c_h-me-_-w_h_i_l_e-u-c_a_n-_-80-special-20/12892003",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/call-me-206-774-0664-sexy-korean-ruby-outcalls-only-22/14400095",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/curly-hair-caramel-melody-hott-exotic-playmate-2062182433-yummysexyy-d-ic-specials-21/14613451",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/exotic-petite-gorgeous-playmate-23/15249710",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/exotic-stunning-playmate-juicy-lips-and-curvy-hips-filipinospanish-20/15082504",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/hot-100-real-bombshell-persian-24/15261623",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/hot-asian-classy-playmate-outcall-and-incall-22/15172622",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/ma-g-i-c-a-lly-de-li-c-i-ou-s-24/15256498",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/new-beautiful-scandinavian-bombshell-100-spcl-247-21/14614142",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/new-discreet-adult-companion-andplaymate-beautiful-sexysweetfun-and-intelligent-too-26/15194583",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/new-playmate-in-town-specials-all-night-long-20/14823505",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/only-in-town-till-2morrow-tall-sexyslim-playmate-23/15259819",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/oo-naughty-never-looked-this-nice-oo-23/9964433",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/outcall-only-call-me-206-774-0892-hong-kong-sexy-zora-23/15254506",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/persian-dreamgirl-_-100-independent-24/15259630",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/rare-one-of-a-kind-playmate-they-say-a-pic-is-worth-a-thousand-words-click-here-for-special100fun-22/6709337",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/real-good-playmate-i-am-your-real-sexy-girl-real-pics-25/15112050",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/sexy-exotic-gorgeous-green-eyed-cutie-20/14104581",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/sexy-freak-next-dooramazingly-delicious-specials-now-20/14629280",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/sexy-seductive-freak-available-all-night-specials-21/15237234",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/sexy-steamy-one-of-a-kind-playdate-with-the-ultimate-playmate-22/11253768",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/super-sexy-absoutly-stunning-blonde-playmate-21/15228813",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/visiting-sexy-hot-asian-girl-ready-to-please-you-come-join-youll-love-24/15045943",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/amazing-green-eyed-yummy-playmate-ready-2-play-100-real-pics-20/12480342",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/and-call-me-today-206-774-0892-hong-kong-sexy-zora-outcall-only-and-23/15259406",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/angel-white-seductive-playmate-22/15253245",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/c_a_t_c_h-me-_-w_h_i_l_e-u-c_a_n-_-80-special-20/12892003",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/call-me-206-774-0664-sexy-korean-ruby-outcalls-only-22/14400095",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/crazy-h0t-white-classy-playmate-22/14805915",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/curly-hair-caramel-melody-hott-exotic-playmate-2062182433-yummysexyy-d-ic-specials-21/14613451",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/exotic-stunning-playmate-juicy-lips-and-curvy-hips-filipinospanish-20/15082504",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/gorgeous-exotic-petite-playmate-22/15266320",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/gorgeous-playmate-23/12310709",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/hot-asian-classy-playmate-outcall-and-incall-22/15172622",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/ma-g-i-c-a-lly-de-li-c-i-ou-s-24/15256498",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/mmmm-your-favorite-redhead-playmate-new-pics-23/15266215",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/n-willing-and-ready-hottie-seductive-playmate-specials-all-night-21/15266905",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/new-asian-hot-body-call-me-206-774-0892-outcall-only-sexy-zora-23/15266676",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/new-discreet-adult-companion-andplaymate-beautiful-sexysweetfun-and-intelligent-too-26/15194583",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/new-playmate-nsea-outcall-only-150hr-20/14823505",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/only-in-town-till-2morrow-tall-sexyslim-playmate-23/15259819",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/oo-naughty-never-looked-this-nice-oo-23/9964433",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/persian-dreamgirl-_-100-independent-24/15259630",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/rare-one-of-a-kind-playmate-they-say-a-pic-is-worth-a-thousand-words-click-here-for-special100fun-22/6709337",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/real-good-playmate-i-am-your-real-sexy-girl-real-pics-25/15112050",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/sexy-exotic-gorgeous-green-eyed-cutie-20/14104581",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/sexy-freak-next-dooramazingly-delicious-specials-now-20/14629280",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/sexy-steamy-one-of-a-kind-playdate-with-the-ultimate-playmate-22/11253768",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/super-sexy-absoutly-stunning-blonde-playmate-21/15228813",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/visiting-sexy-hot-asian-girl-ready-to-please-you-come-join-youll-love-24/15045943",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/100-rose-two-for-one-specials-dont-miss-out-26/14684929",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/5star-ebony-playmate-360-761-9917-22/15150524",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/a-unforgettable-stimulating-experiance-aib-n-cas-27/13567054",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/and-22/15173854",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/and-kk-you-will-love-my-skills-bremerton-out-calls-22/15164765",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/early-bird-specials-your-lil-secret-military-specials-21/15208776",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/gorgeous-100-real-boot-playmate-22/13438525",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/happy-new-year-be-my-1st-14-callers-get-my-super-special-deal-5060-247-100-me-28/15173121",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/i-am-absolutely-a-dream-come-true-click-here-two-for-one-special-26/14891552",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/i-am-the-sexist-asian-in-town-100-rose-special-26/14734898",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/im-back-platinum-blonde-playmate-b-e-a-u-t-i-f-u-l-21/15194279",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/incall-and-military-pecial-super-knk-ebonyandasian-playmate-perky-tits-bubble-booty-cutie-25/8830073",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/new-hotties-in-town-andhearts-ebonyandbunny-duo-big-melon-booties-and-addictive-curves-22/15045510",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/new-in-town-thick-big-booty-beauty-up-all-nite-26/15243486",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/new-pics-christmas-specials-unwrap-your-present-early-bremerton-out-calls-22/15203012",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/platinum-blonde-playmate-b-e-a-u-t-i-f-u-l-21/15207288",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/red-lover-seductive-playmate-23/15196075",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/sexy-independent-playmate-lover-22/14833601",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/specials-_-your-little-secret-_-21/15200463",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/specials-newpics-a-perfect-bonde-ptit-pmt-ready-now-20/13504477",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/super-sweet-sexy-curvy-asian-treat-dont-miss-out-26/14798856",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/t-bs-22/15136285",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/this-sensational-playmate-is-ready-2-cater-2-every-1-of-your-deepest-and-naughtiest-fantasy-24/12263603",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/toe-curling-rotc-pleaure-w-exotic-bu-atisfing-big-b00-best-in-town-25/10435185",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/top-notch-exotic-italian-playmate-available-for-bremerton-out-calls-now-22/15103148",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/tt-_-wt-_-tt-ss-_-21/15198188",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/ultimate-playmate-call-kandiee-702-608-3055-27/13443312",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/waiting-for-the-w-22/15147667",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/x-o-x-o-new-secret-playmate-x-o-x-o-24/14857156",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/100-rose-two-for-one-specials-dont-miss-out-26/14684929",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/a-unforgettable-stimulating-experiance-aib-n-cas-27/13567054",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/and-22/15173854",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/cute-_-_-curvy-_-_-36dd-_-_blonde-_kitten_-100-real-pics-27/14568420",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/early-bird-specials-your-lil-secret-military-specials-21/15208776",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/g_e_n_t_-l_e-_-m_e_n_s_-_-c_h_o_i_-c_-e_-two-for-one-special-26/14795794",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/gorgeous-100-real-boot-playmate-22/13438525",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/happy-new-year-be-my-1st-14-callers-get-my-super-special-deal-5060-247-100-me-28/15173121",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/happy-new-years-specials-newpics-a-perfect-bonde-ptit-pmt-ready-now-20/13504477",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/i-am-absolutely-a-dream-come-true-click-here-two-for-one-special-26/14891552",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/i-am-the-sexist-asian-in-town-100-rose-special-26/14734898",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/incall-and-military-pecial-super-knk-ebonyandasian-playmate-perky-tits-bubble-booty-cutie-25/8830073",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/luv-what-i-do-so-much-im-running-a-30-off-new-years-special-dont-miss-it-360-761-9917-22/15150524",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/new-hotties-in-town-andhearts-ebonyandbunny-duo-big-melon-booties-and-addictive-curves-22/15045510",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/new-in-town-thick-big-booty-beauty-up-all-nite-26/15243486",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/new-ot-sexy-bl0nde-gorgeous-playmate-new-0t-21/15188379",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/new-ot-sexy-bl0nde-gorgeous-playmate-new-0t-21/15195567",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/new-pics-christmas-specials-unwrap-your-present-early-bremerton-out-calls-22/15203012",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/platinum-blonde-playmate-b-e-a-u-t-i-f-u-l-21/15207288",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/red-lover-seductive-playmate-23/15196075",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/sexy-independent-playmate-lover-22/14833601",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/specials-_-your-little-secret-_-21/15200463",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/super-sweet-sexy-curvy-asian-treat-dont-miss-out-26/14798856",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/t-bs-22/15136285",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/top-notch-exotic-italian-playmate-100-bremerton-out-calls-til-8pm-22/15103148",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/ultimate-playmate-call-kandiee-702-608-3055-27/13443312",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/waiting-for-the-w-22/15147667",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/x-o-x-o-new-secret-playmate-x-o-x-o-24/14857156",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/tacoma.backpage.com/FemaleEscorts/and-22/15173854",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/early-bird-inout-specials-duos-23/13994560",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/olympia.backpage.com/FemaleEscorts/early-bird-inout-specials-duos-23/13994560",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/olympia.backpage.com/FemaleEscorts/early-bird-inout-specials-duos-23/13994560",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/me-real-upscale-freaky-blonde-sweet-treat-new-and-friendly-21/15237000",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/me-real-upscale-freaky-blonde-sweet-treat-new-and-friendly-21/15237000",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/gorgeous-all-natural-redhead-goddess-27/15224269",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/me-real-upscale-freaky-blonde-sweet-treat-new-and-friendly-21/15237000",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/dream-girl-special-your-_ebony-fantasy-_-26/14576616",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/light-dark-or-white-your-choice-holiday-special-18/15222142",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/youve-been-_-a_-bad-boy-_-go-to-_-my-room_-_-25/11528421",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/dream-girl-special-your-_ebony-fantasy-_-26/14576616",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/light-dark-or-white-your-choice-holiday-special-18/15222142",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/youve-been-_-a_-bad-boy-_-go-to-_-my-room_-_-25/11528421",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/bellingham.backpage.com/FemaleEscorts/andgtimply-amazing-pecials-21/15073501",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/bellingham.backpage.com/FemaleEscorts/andgtimply-amazing-pecials-available-247-21/15075819",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/bellingham.backpage.com/FemaleEscorts/juc-thck-up-all-day-and-nght-specials-25/15073617",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/bellingham.backpage.com/FemaleEscorts/andgtimply-amazing-pecials-21/15073501",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/bellingham.backpage.com/FemaleEscorts/andgtimply-amazing-pecials-available-247-21/15075819",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/bellingham.backpage.com/FemaleEscorts/juc-thck-up-all-day-and-nght-specials-25/15073617",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/bellingham.backpage.com/FemaleEscorts/andgtimply-amazing-pecials-21/15073501",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/bellingham.backpage.com/FemaleEscorts/andgtimply-amazing-pecials-available-247-21/15075819",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/bellingham.backpage.com/FemaleEscorts/juc-thck-up-all-day-and-nght-specials-25/15073617",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/early-bird-inout-specials-duos-23/13994560",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/gentlemens-choices-curvacious-frames-duo-specials-lacey-incall-all-the-curves-you-desire-21/14911153",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/hot-blond-available-now/15246331",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/misty-130-100-360-270-8143-my-home-and-arms-are-warm-44/5942490",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/s-e-x-y-sk-i-l-l-e-d-and-e-x-t-r-e-m-e-l-y-a-d-d-i-c-t-i-v-e-23/13933539",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/olympia.backpage.com/FemaleEscorts/early-bird-inout-specials-duos-23/13994560",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/olympia.backpage.com/FemaleEscorts/hot-blond-available-now/15246331",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/olympia.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/olympia.backpage.com/FemaleEscorts/misty-130-100-360-270-8143-my-home-and-arms-are-warm-44/5942490",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/olympia.backpage.com/FemaleEscorts/early-bird-inout-specials-duos-23/13994560",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/olympia.backpage.com/FemaleEscorts/gentlemens-choices-curvacious-frames-duo-specials-lacey-incall-all-the-curves-you-desire-21/14911153",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/olympia.backpage.com/FemaleEscorts/hot-blond-available-now/15246331",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/olympia.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/olympia.backpage.com/FemaleEscorts/misty-130-100-360-270-8143-my-home-and-arms-are-warm-44/5942490",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/amazing-puerto-rican-looking-to-playkarmen-80-special-25/15235413",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/gorgeous-pretty-face-perfect-body-amazing-curves-21/15228751",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/seattle.backpage.com/FemaleEscorts/super-sexy-absoutly-stunning-blonde-playmate-21/15228813",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/duos-seahawks-specails-south-center-incall-asian-22/14994840",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/dynamic-ddduo-busty-beautys-and-big-bootys-2-4-1-pecial-100-23/14438534",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/i-am-the-extremely-exotic-girl-youve-been-looking-for-20/15261632",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/lets-start-the-year-offs-rightkarmen-80-special-25/15235413",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/new-pics-new-year-2-girl-special-one-on-one-or-a-duo-book-now-22/15196628",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/seattle.backpage.com/FemaleEscorts/super-sexy-absoutly-stunning-blonde-playmate-21/15228813",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/duos-seahawks-specails-south-center-incall-asian-22/14994840",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/dynamic-ddduo-busty-beautys-and-big-bootys-2-4-1-pecial-100-23/14438534",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/lets-start-the-year-offs-rightkarmen-80-special-25/15235413",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/seattle.backpage.com/FemaleEscorts/new-pics-new-year-2-girl-special-one-on-one-or-a-duo-book-now-22/15196628",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/and-22/15173854",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/bring-in-the-new-year-new-pix-tacoma-duos-avail-reviewed-36/12225381",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/brunette-babe-23/15230558",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/im-back-platinum-blonde-playmate-b-e-a-u-t-i-f-u-l-21/15194279",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/italian-and-mexicana-mixed-buetty-21/15238963",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/new-hotties-in-town-andhearts-ebonyandbunny-duo-big-melon-booties-and-addictive-curves-22/15045510",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/platinum-blonde-playmate-b-e-a-u-t-i-f-u-l-21/15207288",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/sexi-mexi-open-247-com-take-a-ride-on-the-whild-side-23/15035604",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/t-bs-22/15136285",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/tt-_-wt-_-tt-ss-_-21/15198188",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/visiting-blonde-freak-80-costco-size-booty-duos-160-2-hotties-25/10092074",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/visitingblonde-frk-5o-inch-booty-vuluptious-feelso-good-80-juicy-n-beautiful-25/9964367",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/tacoma.backpage.com/FemaleEscorts/waiting-for-the-w-22/15147667",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/2s-better-than-one-double-the-funstunning-hot-mami-exotic-and-erotic-filipino-30/15079246",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/and-22/15173854",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/bring-in-the-new-year-new-pix-tacoma-duos-avail-reviewed-36/12225381",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/brunette-babe-23/15230558",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/index.html",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/italian-and-mexicana-mixed-buetty-let-21/15238963",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/new-hotties-in-town-andhearts-ebonyandbunny-duo-big-melon-booties-and-addictive-curves-22/15045510",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/platinum-blonde-playmate-b-e-a-u-t-i-f-u-l-21/15207288",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/sexi-mexi-open-247-com-take-a-ride-on-the-whild-side-23/15035604",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/t-bs-22/15136285",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/visiting-blonde-freak-80-costco-size-booty-duos-160-2-hotties-25/10092074",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/visitingblonde-frk-5o-inch-booty-vuluptious-feelso-good-80-juicy-n-beautiful-25/9964367",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/tacoma.backpage.com/FemaleEscorts/waiting-for-the-w-22/15147667",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/tacoma.backpage.com/FemaleEscorts/2s-better-than-one-double-the-funstunning-hot-mami-exotic-and-erotic-filipino-30/15079246",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/tacoma.backpage.com/FemaleEscorts/and-22/15173854",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/bellingham.backpage.com/FemaleEscorts/luscious-lexi-_-23/10899702",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/bellingham.backpage.com/FemaleEscorts/rated-pleasure-x-service-27/15191058",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/bellingham.backpage.com/FemaleEscorts/the-best-of-the-bestgrgeus-thiick-blondesmk-n-ht-26/15161614",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/bellingham.backpage.com/FemaleEscorts/luscious-lexi-_-23/10899702",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/bellingham.backpage.com/FemaleEscorts/rated-pleasure-x-service-27/15191058",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140102/bellingham.backpage.com/FemaleEscorts/the-best-of-the-bestgrgeus-thiick-blondesmk-n-ht-26/15161614",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/bellingham.backpage.com/FemaleEscorts/luscious-lexi-_-23/10899702",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/bellingham.backpage.com/FemaleEscorts/rated-pleasure-x-service-27/15191058",
          "https://karmadigstorage.blob.core.windows.net/arch/churl/20140103/bellingham.backpage.com/FemaleEscorts/the-best-of-the-bestgrgeus-thiick-blondesmk-n-ht-26/15161614"]


# materializeUrls(testUrls, "/mnt/resource/staging/test1.seq")
# materializeUrls(genUrls(datestamps=[20140101]), "/mnt/resource/staging/20140101.seq")

def m0():
    try:
        os.remove("/mnt/resource/staging/test1.seq")
    except:
        pass
    materializeUrls(testUrls, "/mnt/resource/staging/test1.seq")

def m():
    try:
        os.remove("/mnt/resource/staging/20140101.seq")
    except:
        pass
    materializeUrls(genUrls(datestamps=[20140101]), "/mnt/resource/staging/20140101.seq")

def matByDate(datestamp):
    try:
        os.remove("/mnt/resource/staging/%s.seq" % datestamp)
    except:
        pass
    materializeUrls(genUrls(datestamps=[datestamp]), "/mnt/resource/staging/%s.seq" % datestamp)

        # start = datetime.datetime.now()
        # logger.info("START extract [%s]", self.source)
        # for sitekey in self.genSitekeys():
        #     self.extractSitekey(sitekey)
        # end = datetime.datetime.now()
        # logger.info("END extract [%s]", self.source)
        # delta = end - start
        # logger.info("ELAPSED extract [%s] is %s", self.source, elapsed(delta))

def matSeveral():
    for sitekey in ['losangeles', 'sanfernandovalley', 'longbeach', 'sangabrielvalley', 'palmdale', 'orangecounty', 'inlandempire']:
        for datestamp in genDatestamps(start=20140101, end=20140110):
            print sitekey, datestamp
            urls = genUrls(datestamps=[datestamp], sitekeys=[sitekey])
            materializeUrls(urls, "/mnt/resource/staging/%s__%s.seq" % (sitekey, datestamp))

BACKPAGE_SITEKEYS=[["-s","backpage","-i","47N","-i","centraljersey"],
                   ["-s","backpage","-i","ABE","-i","allentown"],
                   ["-s","backpage","-i","ABE","-i","poconos"],
                   ["-s","backpage","-i","ABE","-i","reading"],
                   ["-s","backpage","-i","ABI","-i","abilene"],
                   ["-s","backpage","-i","ABQ","-i","albuquerque"],
                   ["-s","backpage","-i","ABY","-i","albanyga"],
                   ["-s","backpage","-i","ACK","-i","capecod"],
                   ["-s","backpage","-i","ACT","-i","waco"],
                   ["-s","backpage","-i","ACV","-i","humboldt"],
                   ["-s","backpage","-i","ACY","-i","jerseyshore"],
                   ["-s","backpage","-i","AEX","-i","alexandria"],
                   ["-s","backpage","-i","AGS","-i","augusta"],
                   ["-s","backpage","-i","AHN","-i","athensga"],
                   ["-s","backpage","-i","ALB","-i","albany"],
                   ["-s","backpage","-i","ALB","-i","catskills"],
                   ["-s","backpage","-i","ALO","-i","waterloo"],
                   ["-s","backpage","-i","AMA","-i","amarillo"],
                   ["-s","backpage","-i","ANC","-i","anchorage"],
                   ["-s","backpage","-i","ANP","-i","annapolis"],
                   ["-s","backpage","-i","AOH","-i","limaoh"],
                   ["-s","backpage","-i","AOO","-i","altoona"],
                   ["-s","backpage","-i","ARB","-i","annarbor"],
                   ["-s","backpage","-i","ART","-i","watertown"],
                   ["-s","backpage","-i","ATL","-i","atlanta"],
                   ["-s","backpage","-i","ATO","-i","athensoh"],
                   ["-s","backpage","-i","ATW","-i","appleton"],
                   ["-s","backpage","-i","AUS","-i","austin"],
                   ["-s","backpage","-i","AUS","-i","sanmarcos"],
                   ["-s","backpage","-i","AVL","-i","asheville"],
                   ["-s","backpage","-i","AVP","-i","scranton"],
                   ["-s","backpage","-i","AZO","-i","battlecreek"],
                   ["-s","backpage","-i","AZO","-i","kalamazoo"],
                   ["-s","backpage","-i","AZO","-i","swmi"],
                   ["-s","backpage","-i","BDL","-i","hartford"],
                   ["-s","backpage","-i","BDL","-i","springfield"],
                   ["-s","backpage","-i","BFF","-i","scottsbluff"],
                   ["-s","backpage","-i","BFL","-i","bakersfield"],
                   ["-s","backpage","-i","BGM","-i","binghamton"],
                   ["-s","backpage","-i","BGM","-i","oneonta"],
                   ["-s","backpage","-i","BHM","-i","birmingham"],
                   ["-s","backpage","-i","BHM","-i","gadsden"],
                   ["-s","backpage","-i","BHM","-i","tuscaloosa"],
                   ["-s","backpage","-i","BIL","-i","montana"],
                   ["-s","backpage","-i","BIS","-i","bismarck"],
                   ["-s","backpage","-i","BJI","-i","bemidji"],
                   ["-s","backpage","-i","BLI","-i","bellingham"],
                   ["-s","backpage","-i","BMG","-i","bloomingtonin"],
                   ["-s","backpage","-i","BMI","-i","bloomington"],
                   ["-s","backpage","-i","BNA","-i","nashville"],
                   ["-s","backpage","-i","BOI","-i","boise"],
                   ["-s","backpage","-i","BOS","-i","boston"],
                   ["-s","backpage","-i","BPT","-i","beaumont"],
                   ["-s","backpage","-i","BQK","-i","brunswick"],
                   ["-s","backpage","-i","BRL","-i","ottumwa"],
                   ["-s","backpage","-i","BRO","-i","brownsville"],
                   ["-s","backpage","-i","BTR","-i","batonrouge"],
                   ["-s","backpage","-i","BTV","-i","burlington"],
                   ["-s","backpage","-i","BUF","-i","buffalo"],
                   ["-s","backpage","-i","BUF","-i","chautauqua"],
                   ["-s","backpage","-i","BUR","-i","sanfernandovalley"],
                   ["-s","backpage","-i","BWG","-i","bowlinggreen"],
                   ["-s","backpage","-i","BWI","-i","baltimore"],
                   ["-s","backpage","-i","CAE","-i","columbia"],
                   ["-s","backpage","-i","CAK","-i","akroncanton"],
                   ["-s","backpage","-i","CBE","-i","westernmaryland"],
                   ["-s","backpage","-i","CGI","-i","semo"],
                   ["-s","backpage","-i","CHA","-i","chattanooga"],
                   ["-s","backpage","-i","CHO","-i","charlottesville"],
                   ["-s","backpage","-i","CHO","-i","harrisonburg"],
                   ["-s","backpage","-i","CHS","-i","charleston"],
                   ["-s","backpage","-i","CIC","-i","chico"],
                   ["-s","backpage","-i","CID","-i","cedarrapids"],
                   ["-s","backpage","-i","CID","-i","iowacity"],
                   ["-s","backpage","-i","CIU","-i","up"],
                   ["-s","backpage","-i","CKV","-i","clarksville"],
                   ["-s","backpage","-i","CLE","-i","cleveland"],
                   ["-s","backpage","-i","CLL","-i","collegestation"],
                   ["-s","backpage","-i","CLT","-i","charlotte"],
                   ["-s","backpage","-i","CMH","-i","columbus"],
                   ["-s","backpage","-i","CMI","-i","chambana"],
                   ["-s","backpage","-i","COS","-i","coloradosprings"],
                   ["-s","backpage","-i","COU","-i","columbiamo"],
                   ["-s","backpage","-i","CPR","-i","wyoming"],
                   ["-s","backpage","-i","CRP","-i","corpuschristi"],
                   ["-s","backpage","-i","CRW","-i","charlestonwv"],
                   ["-s","backpage","-i","CSG","-i","auburn"],
                   ["-s","backpage","-i","CSG","-i","columbusga"],
                   ["-s","backpage","-i","CVG","-i","cincinnati"],
                   ["-s","backpage","-i","CVN","-i","clovis"],
                   ["-s","backpage","-i","CVO","-i","corvallis"],
                   ["-s","backpage","-i","CWA","-i","wausau"],
                   ["-s","backpage","-i","DAB","-i","daytona"],
                   ["-s","backpage","-i","DAN","-i","danville"],
                   ["-s","backpage","-i","DAY","-i","dayton"],
                   ["-s","backpage","-i","DBQ","-i","dubuque"],
                   ["-s","backpage","-i","DEC","-i","decatur"],
                   ["-s","backpage","-i","DEN","-i","denver"],
                   ["-s","backpage","-i","DFW","-i","arlington"],
                   ["-s","backpage","-i","DFW","-i","dallas"],
                   ["-s","backpage","-i","DFW","-i","denton"],
                   ["-s","backpage","-i","DFW","-i","fortworth"],
                   ["-s","backpage","-i","DHN","-i","dothan"],
                   ["-s","backpage","-i","DLH","-i","duluth"],
                   ["-s","backpage","-i","DRT","-i","delrio"],
                   ["-s","backpage","-i","DSM","-i","desmoines"],
                   ["-s","backpage","-i","DTW","-i","detroit"],
                   ["-s","backpage","-i","DTW","-i","monroemi"],
                   ["-s","backpage","-i","EAT","-i","wenatchee"],
                   ["-s","backpage","-i","EAU","-i","eauclaire"],
                   ["-s","backpage","-i","ECP","-i","panamacity"],
                   ["-s","backpage","-i","EGE","-i","rockies"],
                   ["-s","backpage","-i","EKO","-i","elko"],
                   ["-s","backpage","-i","ELM","-i","elmira"],
                   ["-s","backpage","-i","ELM","-i","twintiers"],
                   ["-s","backpage","-i","ELP","-i","elpaso"],
                   ["-s","backpage","-i","EMT","-i","sangabrielvalley"],
                   ["-s","backpage","-i","ERI","-i","ashtabula"],
                   ["-s","backpage","-i","ERI","-i","erie"],
                   ["-s","backpage","-i","ERI","-i","meadville"],
                   ["-s","backpage","-i","EUG","-i","eugene"],
                   ["-s","backpage","-i","EVV","-i","evansville"],
                   ["-s","backpage","-i","EWR","-i","northjersey"],
                   ["-s","backpage","-i","EYW","-i","keys"],
                   ["-s","backpage","-i","FAR","-i","fargo"],
                   ["-s","backpage","-i","FAT","-i","fresno"],
                   ["-s","backpage","-i","FAY","-i","fayettevillenc"],
                   ["-s","backpage","-i","FDK","-i","frederick"],
                   ["-s","backpage","-i","FLG","-i","flagstaff"],
                   ["-s","backpage","-i","FLO","-i","florence"],
                   ["-s","backpage","-i","FMN","-i","farmington"],
                   ["-s","backpage","-i","FNL","-i","fortcollins"],
                   ["-s","backpage","-i","FNT","-i","flint"],
                   ["-s","backpage","-i","FOD","-i","fortdodge"],
                   ["-s","backpage","-i","FSM","-i","fortsmith"],
                   ["-s","backpage","-i","FWA","-i","fortwayne"],
                   ["-s","backpage","-i","GEG","-i","spokane"],
                   ["-s","backpage","-i","GEV","-i","boone"],
                   ["-s","backpage","-i","GFK","-i","grandforks"],
                   ["-s","backpage","-i","GFL","-i","glensfalls"],
                   ["-s","backpage","-i","GJT","-i","westslope"],
                   ["-s","backpage","-i","GNV","-i","gainesville"],
                   ["-s","backpage","-i","GPT","-i","biloxi"],
                   ["-s","backpage","-i","GRB","-i","greenbay"],
                   ["-s","backpage","-i","GRI","-i","grandisland"],
                   ["-s","backpage","-i","GRR","-i","grandrapids"],
                   ["-s","backpage","-i","GRR","-i","holland"],
                   ["-s","backpage","-i","GSO","-i","greensboro"],
                   ["-s","backpage","-i","GSO","-i","winstonsalem"],
                   ["-s","backpage","-i","GSP","-i","greenville"],
                   ["-s","backpage","-i","GYI","-i","texoma"],
                   ["-s","backpage","-i","HEZ","-i","natchez"],
                   ["-s","backpage","-i","HGR","-i","chambersburg"],
                   ["-s","backpage","-i","HGR","-i","cumberlandvalley"],
                   ["-s","backpage","-i","HGR","-i","martinsburg"],
                   ["-s","backpage","-i","HKY","-i","hickory"],
                   ["-s","backpage","-i","HLG","-i","wheeling"],
                   ["-s","backpage","-i","HNL","-i","honolulu"],
                   ["-s","backpage","-i","HPN","-i","nwct"],
                   ["-s","backpage","-i","HPN","-i","westchester"],
                   ["-s","backpage","-i","HSV","-i","huntsville"],
                   ["-s","backpage","-i","HTS","-i","huntington"],
                   ["-s","backpage","-i","HUF","-i","terrehaute"],
                   ["-s","backpage","-i","HVN","-i","newhaven"],
                   ["-s","backpage","-i","HVN","-i","newlondon"],
                   ["-s","backpage","-i","IAD","-i","dc"],
                   ["-s","backpage","-i","IAD","-i","fredericksburg"],
                   ["-s","backpage","-i","IAD","-i","nova"],
                   ["-s","backpage","-i","IAD","-i","southernmaryland"],
                   ["-s","backpage","-i","IAD","-i","washingtondc"],
                   ["-s","backpage","-i","IAH","-i","galveston"],
                   ["-s","backpage","-i","IAH","-i","houston"],
                   ["-s","backpage","-i","ICT","-i","wichita"],
                   ["-s","backpage","-i","IDA","-i","eastidaho"],
                   ["-s","backpage","-i","IGM","-i","mohave"],
                   ["-s","backpage","-i","ILE","-i","killeen"],
                   ["-s","backpage","-i","ILG","-i","delaware"],
                   ["-s","backpage","-i","ILM","-i","wilmington"],
                   ["-s","backpage","-i","IND","-i","indianapolis"],
                   ["-s","backpage","-i","IPL","-i","imperial"],
                   ["-s","backpage","-i","IPT","-i","williamsport"],
                   ["-s","backpage","-i","IRK","-i","kirksville"],
                   ["-s","backpage","-i","ITH","-i","fingerlakes"],
                   ["-s","backpage","-i","ITH","-i","ithaca"],
                   ["-s","backpage","-i","JAN","-i","jackson"],
                   ["-s","backpage","-i","JAX","-i","jacksonville"],
                   ["-s","backpage","-i","JAX","-i","staugustine"],
                   ["-s","backpage","-i","JBR","-i","jonesboro"],
                   ["-s","backpage","-i","JFK","-i","bronx"],
                   ["-s","backpage","-i","JFK","-i","brooklyn"],
                   ["-s","backpage","-i","JFK","-i","longisland"],
                   ["-s","backpage","-i","JFK","-i","manhattan"],
                   ["-s","backpage","-i","JFK","-i","newyork"],
                   ["-s","backpage","-i","JFK","-i","queens"],
                   ["-s","backpage","-i","JFK","-i","statenisland"],
                   ["-s","backpage","-i","JLN","-i","joplin"],
                   ["-s","backpage","-i","JVL","-i","janesville"],
                   ["-s","backpage","-i","JXN","-i","jacksonmi"],
                   ["-s","backpage","-i","KOA","-i","bigisland"],
                   ["-s","backpage","-i","LAF","-i","tippecanoe"],
                   ["-s","backpage","-i","LAN","-i","lansing"],
                   ["-s","backpage","-i","LAS","-i","lasvegas"],
                   ["-s","backpage","-i","LAW","-i","lawton"],
                   ["-s","backpage","-i","LAX","-i","losangeles"],
                   ["-s","backpage","-i","LBB","-i","lubbock"],
                   ["-s","backpage","-i","LBF","-i","northplatte"],
                   ["-s","backpage","-i","LCH","-i","lakecharles"],
                   ["-s","backpage","-i","LEX","-i","eastky"],
                   ["-s","backpage","-i","LEX","-i","lexington"],
                   ["-s","backpage","-i","LFT","-i","lafayette"],
                   ["-s","backpage","-i","LGB","-i","longbeach"],
                   ["-s","backpage","-i","LGU","-i","logan"],
                   ["-s","backpage","-i","LIH","-i","kauai"],
                   ["-s","backpage","-i","LIT","-i","littlerock"],
                   ["-s","backpage","-i","LMT","-i","klamath"],
                   ["-s","backpage","-i","LNK","-i","lincoln"],
                   ["-s","backpage","-i","LRD","-i","laredo"],
                   ["-s","backpage","-i","LRU","-i","lascruces"],
                   ["-s","backpage","-i","LSE","-i","lacrosse"],
                   ["-s","backpage","-i","LWB","-i","southernwestvirginia"],
                   ["-s","backpage","-i","LWC","-i","lawrence"],
                   ["-s","backpage","-i","LWC","-i","topeka"],
                   ["-s","backpage","-i","LWS","-i","lewiston"],
                   ["-s","backpage","-i","LYH","-i","lynchburg"],
                   ["-s","backpage","-i","MAF","-i","odessa"],
                   ["-s","backpage","-i","MBS","-i","saginaw"],
                   ["-s","backpage","-i","MCE","-i","merced"],
                   ["-s","backpage","-i","MCI","-i","kc"],
                   ["-s","backpage","-i","MCN","-i","macon"],
                   ["-s","backpage","-i","MCO","-i","orlando"],
                   ["-s","backpage","-i","MCW","-i","masoncity"],
                   ["-s","backpage","-i","MDT","-i","harrisburg"],
                   ["-s","backpage","-i","MDT","-i","lancaster"],
                   ["-s","backpage","-i","MDT","-i","york"],
                   ["-s","backpage","-i","MEI","-i","meridian"],
                   ["-s","backpage","-i","MEM","-i","memphis"],
                   ["-s","backpage","-i","MEM","-i","northmiss"],
                   ["-s","backpage","-i","MFD","-i","huntingtonoh"],
                   ["-s","backpage","-i","MFD","-i","mansfield"],
                   ["-s","backpage","-i","MFE","-i","mcallen"],
                   ["-s","backpage","-i","MFR","-i","medford"],
                   ["-s","backpage","-i","MGM","-i","montgomery"],
                   ["-s","backpage","-i","MGW","-i","morgantown"],
                   ["-s","backpage","-i","MHK","-i","manhattanks"],
                   ["-s","backpage","-i","MHT","-i","newhampshire"],
                   ["-s","backpage","-i","MIA","-i","ftlauderdale"],
                   ["-s","backpage","-i","MIA","-i","miami"],
                   ["-s","backpage","-i","MIE","-i","muncie"],
                   ["-s","backpage","-i","MKE","-i","milwaukee"],
                   ["-s","backpage","-i","MKG","-i","muskegon"],
                   ["-s","backpage","-i","MKT","-i","mankato"],
                   ["-s","backpage","-i","MLB","-i","spacecoast"],
                   ["-s","backpage","-i","MLI","-i","quadcities"],
                   ["-s","backpage","-i","MLU","-i","monroe"],
                   ["-s","backpage","-i","MOB","-i","mobile"],
                   ["-s","backpage","-i","MOD","-i","modesto"],
                   ["-s","backpage","-i","MOP","-i","centralmich"],
                   ["-s","backpage","-i","MOT","-i","minot"],
                   ["-s","backpage","-i","MQI","-i","outerbanks"],
                   ["-s","backpage","-i","MRY","-i","monterey"],
                   ["-s","backpage","-i","MSL","-i","shoals"],
                   ["-s","backpage","-i","MSN","-i","madison"],
                   ["-s","backpage","-i","MSP","-i","minneapolis"],
                   ["-s","backpage","-i","MSS","-i","potsdam"],
                   ["-s","backpage","-i","MSY","-i","houma"],
                   ["-s","backpage","-i","MSY","-i","neworleans"],
                   ["-s","backpage","-i","MVW","-i","mtvernon"],
                   ["-s","backpage","-i","MWA","-i","carbondale"],
                   ["-s","backpage","-i","MWH","-i","moseslake"],
                   ["-s","backpage","-i","MYR","-i","myrtlebeach"],
                   ["-s","backpage","-i","OAJ","-i","easternnc"],
                   ["-s","backpage","-i","OAK","-i","eastbay"],
                   ["-s","backpage","-i","OCF","-i","ocala"],
                   ["-s","backpage","-i","OGD","-i","ogden"],
                   ["-s","backpage","-i","OGG","-i","maui"],
                   ["-s","backpage","-i","OKC","-i","oklahomacity"],
                   ["-s","backpage","-i","OKK","-i","kokomo"],
                   ["-s","backpage","-i","OMA","-i","omaha"],
                   ["-s","backpage","-i","ONP","-i","oregoncoast"],
                   ["-s","backpage","-i","ONT","-i","inlandempire"],
                   ["-s","backpage","-i","ORD","-i","chicago"],
                   ["-s","backpage","-i","ORF","-i","chesapeake"],
                   ["-s","backpage","-i","ORF","-i","hampton"],
                   ["-s","backpage","-i","ORF","-i","newportnews"],
                   ["-s","backpage","-i","ORF","-i","norfolk"],
                   ["-s","backpage","-i","ORF","-i","portsmouth"],
                   ["-s","backpage","-i","ORF","-i","suffolk"],
                   ["-s","backpage","-i","ORF","-i","virginiabeach"],
                   ["-s","backpage","-i","ORH","-i","worcester"],
                   ["-s","backpage","-i","OWB","-i","owensboro"],
                   ["-s","backpage","-i","OXR","-i","ventura"],
                   ["-s","backpage","-i","PAE","-i","everett"],
                   ["-s","backpage","-i","PAH","-i","westky"],
                   ["-s","backpage","-i","PBG","-i","plattsburgh"],
                   ["-s","backpage","-i","PBI","-i","westpalmbeach"],
                   ["-s","backpage","-i","PDT","-i","eastoregon"],
                   ["-s","backpage","-i","PDX","-i","portland"],
                   ["-s","backpage","-i","PHD","-i","tuscarawas"],
                   ["-s","backpage","-i","PHL","-i","philadelphia"],
                   ["-s","backpage","-i","PHL","-i","southjersey"],
                   ["-s","backpage","-i","PHN","-i","porthuron"],
                   ["-s","backpage","-i","PHX","-i","phoenix"],
                   ["-s","backpage","-i","PHX","-i","prescott"],
                   ["-s","backpage","-i","PIA","-i","peoria"],
                   ["-s","backpage","-i","PIB","-i","hattiesburg"],
                   ["-s","backpage","-i","PIT","-i","pittsburgh"],
                   ["-s","backpage","-i","PKB","-i","parkersburg"],
                   ["-s","backpage","-i","PMD","-i","palmdale"],
                   ["-s","backpage","-i","PNS","-i","pensacola"],
                   ["-s","backpage","-i","PSC","-i","tricitieswa"],
                   ["-s","backpage","-i","PSP","-i","palmsprings"],
                   ["-s","backpage","-i","PUB","-i","pueblo"],
                   ["-s","backpage","-i","PUW","-i","pullman"],
                   ["-s","backpage","-i","PVD","-i","providence"],
                   ["-s","backpage","-i","PVD","-i","southcoast"],
                   ["-s","backpage","-i","PVU","-i","provo"],
                   ["-s","backpage","-i","PWM","-i","maine"],
                   ["-s","backpage","-i","RAC","-i","racine"],
                   ["-s","backpage","-i","RAP","-i","southdakota"],
                   ["-s","backpage","-i","RBG","-i","roseburg"],
                   ["-s","backpage","-i","RDD","-i","redding"],
                   ["-s","backpage","-i","RDM","-i","bend"],
                   ["-s","backpage","-i","RDU","-i","raleigh"],
                   ["-s","backpage","-i","RFD","-i","rockford"],
                   ["-s","backpage","-i","RIC","-i","richmond"],
                   ["-s","backpage","-i","RID","-i","richmondin"],
                   ["-s","backpage","-i","RMG","-i","nwga"],
                   ["-s","backpage","-i","RNO","-i","reno"],
                   ["-s","backpage","-i","ROA","-i","blacksburg"],
                   ["-s","backpage","-i","ROA","-i","roanoke"],
                   ["-s","backpage","-i","ROC","-i","rochester"],
                   ["-s","backpage","-i","ROW","-i","roswell"],
                   ["-s","backpage","-i","RST","-i","rochestermn"],
                   ["-s","backpage","-i","RSW","-i","fortmyers"],
                   ["-s","backpage","-i","RZT","-i","chillicothe"],
                   ["-s","backpage","-i","SAF","-i","santafe"],
                   ["-s","backpage","-i","SAN","-i","sandiego"],
                   ["-s","backpage","-i","SAT","-i","sanantonio"],
                   ["-s","backpage","-i","SAT","-i","sanantonio"],
                   ["-s","backpage","-i","SAV","-i","hiltonhead"],
                   ["-s","backpage","-i","SAV","-i","savannah"],
                   ["-s","backpage","-i","SBA","-i","santabarbara"],
                   ["-s","backpage","-i","SBM","-i","sheboygan"],
                   ["-s","backpage","-i","SBN","-i","southbend"],
                   ["-s","backpage","-i","SBP","-i","sanluisobispo"],
                   ["-s","backpage","-i","SBY","-i","easternshore"],
                   ["-s","backpage","-i","SCE","-i","pennstate"],
                   ["-s","backpage","-i","SCK","-i","stockton"],
                   ["-s","backpage","-i","SDF","-i","louisville"],
                   ["-s","backpage","-i","SEA","-i","seattle"],
                   ["-s","backpage","-i","SFO","-i","sf"],
                   ["-s","backpage","-i","SGF","-i","springfieldmo"],
                   ["-s","backpage","-i","SGU","-i","stgeorge"],
                   ["-s","backpage","-i","SHV","-i","shreveport"],
                   ["-s","backpage","-i","SIY","-i","siskiyou"],
                   ["-s","backpage","-i","SJC","-i","sanjose"],
                   ["-s","backpage","-i","SKY","-i","sandusky"],
                   ["-s","backpage","-i","SLC","-i","saltlakecity"],
                   ["-s","backpage","-i","SLE","-i","salem"],
                   ["-s","backpage","-i","SMF","-i","sacramento"],
                   ["-s","backpage","-i","SMX","-i","santamaria"],
                   ["-s","backpage","-i","SNA","-i","orangecounty"],
                   ["-s","backpage","-i","SOW","-i","showlow"],
                   ["-s","backpage","-i","SPI","-i","springfieldil"],
                   ["-s","backpage","-i","SPS","-i","wichitafalls"],
                   ["-s","backpage","-i","SQL","-i","sanmateo"],
                   ["-s","backpage","-i","SRB","-i","cookeville"],
                   ["-s","backpage","-i","STC","-i","stcloud"],
                   ["-s","backpage","-i","STJ","-i","stjoseph"],
                   ["-s","backpage","-i","STL","-i","mattoon"],
                   ["-s","backpage","-i","STL","-i","stlouis"],
                   ["-s","backpage","-i","STS","-i","northbay"],
                   ["-s","backpage","-i","SUX","-i","siouxcity"],
                   ["-s","backpage","-i","SVE","-i","susanville"],
                   ["-s","backpage","-i","SWF","-i","hudsonvalley"],
                   ["-s","backpage","-i","SWO","-i","stillwater"],
                   ["-s","backpage","-i","SYR","-i","fairfield"],
                   ["-s","backpage","-i","SYR","-i","syracuse"],
                   ["-s","backpage","-i","SYR","-i","utica"],
                   ["-s","backpage","-i","TBN","-i","loz"],
                   ["-s","backpage","-i","TBR","-i","statesboro"],
                   ["-s","backpage","-i","TCM","-i","olympia"],
                   ["-s","backpage","-i","TCM","-i","tacoma"],
                   ["-s","backpage","-i","TLH","-i","tallahassee"],
                   ["-s","backpage","-i","TOL","-i","toledo"],
                   ["-s","backpage","-i","TPA","-i","lakeland"],
                   ["-s","backpage","-i","TPA","-i","sarasota"],
                   ["-s","backpage","-i","TPA","-i","tampa"],
                   ["-s","backpage","-i","TRI","-i","tricities"],
                   ["-s","backpage","-i","TUL","-i","tulsa"],
                   ["-s","backpage","-i","TUS","-i","sierravista"],
                   ["-s","backpage","-i","TUS","-i","tucson"],
                   ["-s","backpage","-i","TVC","-i","northernmichigan"],
                   ["-s","backpage","-i","TWF","-i","twinfalls"],
                   ["-s","backpage","-i","TXK","-i","texarkana"],
                   ["-s","backpage","-i","TYR","-i","tyler"],
                   ["-s","backpage","-i","TYS","-i","knoxville"],
                   ["-s","backpage","-i","UIN","-i","quincy"],
                   ["-s","backpage","-i","UKI","-i","mendocino"],
                   ["-s","backpage","-i","UTS","-i","huntsvilletx"],
                   ["-s","backpage","-i","VCT","-i","victoriatx"],
                   ["-s","backpage","-i","VIS","-i","visalia"],
                   ["-s","backpage","-i","VJI","-i","swva"],
                   ["-s","backpage","-i","VLD","-i","valdosta"],
                   ["-s","backpage","-i","VRB","-i","treasurecoast"],
                   ["-s","backpage","-i","VYS","-i","lasalle"],
                   ["-s","backpage","-i","WBU","-i","boulder"],
                   ["-s","backpage","-i","WVI","-i","santacruz"],
                   ["-s","backpage","-i","XNA","-i","fayetteville"],
                   ["-s","backpage","-i","YKM","-i","yakima"],
                   ["-s","backpage","-i","YNG","-i","youngstown"],
                   ["-s","backpage","-i","YUM","-i","yuma"],
                   ["-s","backpage","-i","YVR","-i","vancouver"],
                   ["-s","backpage","-i","ZZV","-i","zanesville"]]

def matJanThruJune():
    for datestamp in genDatestamps(20140111,20140630):
        for tup in BACKPAGE_SITEKEYS:
            sitekey = tup[5]
            print sitekey, datestamp
            urls = genUrls(datestamps=[datestamp], sitekeys=[sitekey])
            materializeUrls(urls, "/mnt/resource/staging/%s__%s.seq" % (sitekey, datestamp))
        
def matJan():
    for datestamp in genDatestamps(20140101,20140110):
        for tup in BACKPAGE_SITEKEYS:
            sitekey = tup[5]
            if not sitekey in ['losangeles', 'sanfernandovalley', 'longbeach', 'sangabrielvalley', 'palmdale', 'orangecounty', 'inlandempire']:
                print sitekey, datestamp
                urls = genUrls(datestamps=[datestamp], sitekeys=[sitekey])
                materializeUrls(urls, "/mnt/resource/staging/%s__%s.seq" % (sitekey, datestamp))

