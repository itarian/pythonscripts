import os
import tempfile
def deletetempfiles():
    for rt, di, fi in os.walk(tempfile.gettempdir()):
        for fn in fi:
            try:
                os.remove(os.path.join(rt, fn))
            except Exception as e:
                print e
if __name__=='__main__':
    deletetempfiles()
