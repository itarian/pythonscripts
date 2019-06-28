import urllib2,re,ssl,os,socket,sys,platform,uuid
print  "Computer Name: " +socket.gethostname() 
print "FQDN: " +socket.getfqdn()
print "System Platform: "+sys.platform
print "Machine: " +platform.machine()
print "Node " +platform.node()
print "Platform: "+platform.platform()
print "Pocessor: " +platform.processor()
print "System OS: "+platform.system()
print "Release: " +platform.release()
print "Version: " +platform.version()
print "\n"
req = urllib2.Request('https://ipinfo.io/')
context = ssl._create_unverified_context()
c=0
res = urllib2.urlopen(req,context=context)
data = res.read()

values = re.search(r'"ip":\s"(.*)",\n.*"city":\s"(.*)",\n.*"region":\s"(.*)",\n.*"country":\s"(.*)",\n.*"loc":\s"(.*)",\n.*"hostname":\s"(.*)",\n.*"postal":\s"(.*)",\n.*"org":\s"(.*)"',data)
if values:
    ip = values.group(1)
    city = values.group(2)
    state = values.group(3)
    country = values.group(4)
    location = values.group(5)
    organization = values.group(8)

print "IP Address: "+ip
print "City: "+city
print "State: "+state
print "Country: "+country
print "Location(Latitude,Longitude): "+location
print "Organization: "+organization

