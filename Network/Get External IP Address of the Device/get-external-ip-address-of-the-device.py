from urllib2 import urlopen
myip = urlopen('http://ip.42.pl/raw').read()
print myip
