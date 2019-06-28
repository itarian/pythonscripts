path = r'C:\ProgramData\Comodo\AV Logs Backup'              # Provide the path of the folder.
days=396                                             # Provide the number of days

import os
import time
import shutil

now = time.time()
for f in os.listdir(path):
    fpath=os.path.join(path,f)

    if os.stat(fpath).st_mtime < (now - (days * 86400)):
        print 'path',fpath,' is removed'
        if os.path.isfile(fpath):
            os.remove(fpath);
        if os.path.isdir(fpath):
            shutil.rmtree(fpath)            
    else:
        print fpath,'is not older'
