import os
import tempfile
def showtempfiles():
    for rt, di, fi in os.walk(tempfile.gettempdir()):
        for fn in fi:
            print (os.path.join(rt, fn))
if __name__=='__main__':
    showtempfiles()
