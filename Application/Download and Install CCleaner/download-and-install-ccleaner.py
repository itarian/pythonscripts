import urllib
import os

def main(Path, URL='http://download.piriform.com/ccsetup523.exe', sCMD='/S'):
    if os.path.exists(Path):
        fn = URL.split('/')[-1]
        fp = os.path.join(Path, fn)
        try:
            with open(fp, 'wb') as f:
                try:
                    f.write(urllib.urlopen(URL).read())
                    print fp
                except Exception as e:
                    print e
        except Exception as e:
            print e
        try:
            os.popen(fp+' '+sCMD).read()
            return 'Great! Successfully Installed'
        except Exception as e:
            return e
    else:
        return 'No path: '+Path+' is exist'


print main('C:\\Users\\Prime\\Downloads')
