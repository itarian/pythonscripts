import urllib2,re,ssl,os,socket,sys,platform,uuid
print  "Computer Name: " +socket.gethostname() 
req = urllib2.Request('https://iplocation.net/')
context = ssl._create_unverified_context()
c=0
res = urllib2.urlopen(req,context=context)
data = res.read()
patterns =  re.findall('href="\/go\/ip2location(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)',data)
values = ','.join(str(v) for v in patterns)
ki=re.findall('<td>(.*)<',values)
list1=[]
Data=ki[0].split('<')


Data[25]=Data[25].strip('td>')

dict={'Your Public IP Address is ':Data[0]}
for keys,values in dict.items():
    print keys +" =   "+values


