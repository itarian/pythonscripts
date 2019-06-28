import json
import ssl
from urllib2 import urlopen
context = ssl._create_unverified_context()
exip = urlopen('https://api.ipify.org/',context=context).read()
url = 'http://api.db-ip.com/v2/free/{0}'.format(exip)
response = urlopen(url,context=context)
data = json.load(response)
IP=data['ipAddress']
continentCode=data['continentCode']
continentName = data['continentName']
countryCode=data['countryCode']
countryName=data['countryName']
state=data['stateProv']
city=data['city']
print 'Your loaction details\n '
print 'IP : {0} \ncontinentCode : {1} \ncontinentName : {2} \ncountryCode : {3} \ncountryName : {4} \nstate : {5} \ncity : {6}'.format(IP,continentCode,continentName,countryCode,countryName,state,city)
