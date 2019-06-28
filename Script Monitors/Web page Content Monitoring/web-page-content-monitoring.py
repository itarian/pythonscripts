url1="https://c1forum.comodo.com/forum/script-library/11468-script-monitors-index-page?key5sk1=2789f0f32c334602471d2f6a3e61bef1bee08056"
find="Hurray!!! This is a much needed capability...now we have it!!!"
import sys
def alert(arg): 
	sys.stderr.write("%d%d%d" % (arg, arg, arg)) 

import urllib
import re
page=urllib.urlopen(url1).read()
ki=re.findall(find,page)

if len(ki)>0:
    if ki[0]==find:
        print "Content is found in webpage as below:"
        print "\n"+find
        alert(1)
else:
    print "Content is not found"
    alert(0)
