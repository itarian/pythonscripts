link =r'www.gmail.com' #Provide the url link which you need to check 

import urllib2
import ssl
import ssl
import urllib
import httplib
from urllib2 import Request, urlopen, HTTPError, URLError

if 'http' in link:
    pass

else:
    try:
        link='https://'+link
    except:
        link='http://'+link
try:
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    response = urllib2.urlopen(link,context=gcontext)
    print "The URL is available: ", response.geturl()
    print "This gets the code: ", response.code
    print "The Date is: ", response.info()

except URLError, e:
    print "website not available due to following error..."
    val=e.reason
    print val
    
except HTTPError, e:
    print "website not available due to following error..."
    print e




