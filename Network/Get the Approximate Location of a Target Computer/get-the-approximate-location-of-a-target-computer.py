##Tips for formatting your coordinates
##Use the degree symbol instead of "d".
##Use periods as decimals, not commas.
##Incorrect: 41,40338, 2,17403. Correct: 41.40338, 2.17403.
##List your latitude coordinates before longitude coordinates.
##Check that the first number in your latitude coordinate is between -90 and 90.
##Check that the first number in your longitude coordinate is between -180 and 180.
import urllib2
import re
req = urllib2.Request('https://geoiptool.com/')
try:
    res = urllib2.urlopen(req)
    data = res.read()
    patterns = [r'lat:\s(\-|[0-9])+[.][0-9]+', r'lng:\s(\-|[0-9])+[.][0-9]+']
    ll = []
    for i in patterns:
        match = re.search(i, data)
        if match:
            fval = match.group().split()[1]
            ll.append(fval)
    lat = ll[0]
    lng = ll[1]
    print 'http://www.google.com/maps/place/{},{}'.format(lat, lng)
except URLError as e:
    print e
except HTTPError as e:
    print e.code
