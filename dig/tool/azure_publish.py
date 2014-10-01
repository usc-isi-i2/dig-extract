from azure import *
from azure.storage import *
import os
import urllib2
import dig.pymod.util as util
from dig.pymod.util import elapsed, genDatestamps
import datetime
import simplejson as json
import re
import time
import mimetypes

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

def db2url(tbl='backpage_incoming',
           limit=1,
           user='sqluser', 
           password='sqlpassword',
           # host='karma-dig-db.cloudapp.net',
           host='localhost',
           database='memex_small',
           maxAttempts = 3):
    cnx = mysql.connector.connect(user=user,
                                  password=password,
                                  host=host,
                                  database=database)
    cursor = cnx.cursor()

    query = (("""SELECT url, body, timestamp FROM %s """ % tbl) + 
             (""" LIMIT %s"""))

    query = query % (limit)

    cursor.execute(query)

    urls = []
    for (url, body, timestamp) in cursor:
        print url
        print timestamp
        datestamp = timestamp.strftime('%Y%m%d')
        # follow https://karmadigstorage.blob.core.windows.net/arch/churl/20140101/olympia.backpage.com/FemaleEscorts/100-asian-hi-im-honey-n-im-super-sweet-25/13538952
        crawlAgent = "istr_%s" % database
        destination = os.path.join(crawlAgent, str(datestamp), url[7:])
        # print destination
        # exit(0)
        try:
            success = False
            remainingAttempts = maxAttempts
            while not success and remainingAttempts>0:
                try:
                    size = len(body)
                    status = bs.put_block_blob_from_text(mycontainer, destination, body,
                                                         x_ms_blob_content_type='text/html')
                    print >> sys.stderr, "reload %s as %s / %s: size=%d, status=%s" % (url, mycontainer, destination, size, status)
                    success = True
                    break
                except socket.error as se:
                    remainingAttempts -= 1
                    print >> sys.stderr, "Uploading %s failed, sleep 5 sec, %d more tries" % (pathname, remainingAttempts)
                    time.sleep(5)
                except WindowsAzureError as e:
                    print >> sys.stderr, "Azure failure [%r], skipping"
        except Exception as e:
            print >> sys.stderr, "Total failure per %s" % e

    cnx.close()
    return urls

VERBOSE = False
BUCKET = 'arch'
CONTENT_TYPE = "text/html"


def azure_publish_file(pathname,
                       maxAttempts=3,
                       content_type=CONTENT_TYPE,
                       bucket=BUCKET):
    destination = pathname
    try:
        success = False
        remainingAttempts = maxAttempts
        while not success and remainingAttempts>0:
            try:
                bs.put_block_blob_from_file(mycontainer, destination, pathname,
                                            x_ms_blob_content_type=content_type)
                success = True
                break
            except socket.error as se:
                remainingAttempts -= 1
                print >> sys.stderr, "Uploading %s failed, sleep 5 sec, %d more tries" % (pathname, remainingAttempts)
                time.sleep(5)
            except WindowsAzureError as e:
                print >> sys.stderr, "Azure failure [%r], skipping"
    except Exception as e:
        print >> sys.stderr, "Failed %r" % e


##################################################################

import sys
import os
import argparse
import dig.pymod.util as util
from dig.pymod.util import elapsed, interpretCmdLine
import datetime

# adapted from https://github.com/matteobertozzi/Hadoop/blob/master/python-hadoop/examples/SequenceFileReader.py

def main(argv=None):
    '''this is called if run from command line'''
    start = datetime.datetime.now()
    (prog, args) = interpretCmdLine()
    parser = argparse.ArgumentParser(prog, description='azure_publish')
    parser.add_argument('-d', '--directory', help='directory to publish', 
                        required=False, 
                        action="append",
                        default=[])
    parser.add_argument('-f', '--file', help='file to publish', 
                        required=False, 
                        action="append",
                        default=[])
    parser.add_argument('-t', '--type', help='content type', 
                        required=False,
                        choices=["text/html", "image/jpeg", "image/gif", "image/png"],
                        default="text/html")
    parser.add_argument('-v', '--verbose', help='print to stderr',
                        required=False,
                        default=VERBOSE)

    args = parser.parse_args(args)
    files = args.file
    directories = args.directory
    verbose = args.verbose
    count = 0
    for pathname in files:
        azure_publish_file(pathname, content_type=args.type)
        count += 1
    for directory in directories:
        for file in os.listdir(directory):
            azure_publish_file(file, content_type=args.type)
            count += 1
    end = datetime.datetime.now()
    delta = end - start
    if verbose:
        print >> sys.stderr, "ELAPSED azure_publish is %s" % elapsed(delta)
        print >> sys.stderr, "%d files uploaded" % (count)

# call main() if this is run as standalone
if __name__ == "__main__":
    sys.exit(main())
