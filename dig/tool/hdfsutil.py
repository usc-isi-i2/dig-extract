from azure import *
from azure.storage import *
import os
import urllib2
import util
from util import elapsed
from glob import iglob
import subprocess
import shutil
# from hadoop.io.SequenceFile import CompressionType
from hadoop.io import Text
from hadoop.io import SequenceFile
import datetime
import simplejson as json

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

DATESTAMPS = [ds for ds in util.genDatestamps(start=20140101, end=20140201)]
DATESTAMPS = [ds for ds in util.genDatestamps(start=20140101, end=20140103)]
DATESTAMPS = [ds for ds in util.genDatestamps(start=20130101, end=20141231)]

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

def genBlobs(datestamps=DATESTAMPS, crawlAgents=CRAWLAGENTS):
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
                        yield blob
                    except WindowsAzureError as e:
                        print >> sys.stderr, "Failed on %s, skipping" % blob
                if next_marker is None:
                    break

def genUrls(datestamps=DATESTAMPS, crawlAgents=CRAWLAGENTS):
    for blob in genBlobs(datestamps=datestamps, crawlAgents=crawlAgents):
        yield blob.url

# def writeData(writer):
#     key = Text()
#     value = Text()

#     key.set('Key')
#     value.set('Value')

#     writer.append(key, value)

# if __name__ == '__main__':
#     writer = SequenceFile.createWriter('test.seq', Text, Text)
#     writeData(writer)
#     writer.close()

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

# nwUrls = []
from dig.tool.data.nwurls import nwUrls

# materializeUrls(testUrls, "/mnt/resource/arch/test1.seq")
# materializeUrls(genUrls(datestamps=[20140101]), "/mnt/resource/arch/20140101.seq")

def m0():
    try:
        os.remove("/mnt/resource/arch/test1.seq")
    except:
        pass
    materializeUrls(testUrls, "/mnt/resource/arch/test1.seq")

def m():
    try:
        os.remove("/mnt/resource/arch/20140101.seq")
    except:
        pass
    materializeUrls(genUrls(datestamps=[20140101]), "/mnt/resource/arch/20140101.seq")

def matByDate(datestamp):
    try:
        os.remove("/mnt/resource/arch/%s.seq" % datestamp)
    except:
        pass
    materializeUrls(genUrls(datestamps=[datestamp]), "/mnt/resource/arch/%s.seq" % datestamp)

        # start = datetime.datetime.now()
        # logger.info("START extract [%s]", self.source)
        # for sitekey in self.genSitekeys():
        #     self.extractSitekey(sitekey)
        # end = datetime.datetime.now()
        # logger.info("END extract [%s]", self.source)
        # delta = end - start
        # logger.info("ELAPSED extract [%s] is %s", self.source, elapsed(delta))
    
print WindowsAzureError
