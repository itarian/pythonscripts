DATA="Table Of Contents"
URL=r'https://docs.python.org/2/tutorial/errors.html'
import urllib 
import urllib2 
import cookielib
import re
import sys
jar = cookielib.FileCookieJar("cookie")
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar)) 
user_agent={'User-Agent' : "Magic Browser"}
login_request = urllib2.Request(URL)
login_reply = opener.open(login_request)
login_reply_data = login_reply.read()
out=re.findall(DATA,login_reply_data)
if DATA in login_reply_data:
        print "Content is found in webpage as below:"
        print DATA

elif len(out)>0:
        print "Content is found in webpage as below:"
        print "\n"+out[0]
else:
        print "No data"
    
