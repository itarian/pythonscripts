import os
import re
import filecmp
import difflib
import sys
import sqlite3
def os_platform():
    true_platform = os.environ['PROCESSOR_ARCHITECTURE']
    try:
            true_platform = os.environ["PROCESSOR_ARCHITEW6432"]
    except KeyError:
            pass

    return true_platform



ki=os_platform()
archi=int(filter(str.isdigit, ki))

if archi==64:
   path = "C:\Program Files (x86)\COMODO\Comodo ITSM\pm.db"
elif archi==86:
   path = "C:\Program Files\COMODO\Comodo ITSM\pm.db" 

si=[]
conn = sqlite3.connect(path)
cur = conn.cursor()
cur.execute("SELECT * FROM [spm::mdatabaseversion];")
rows = cur.fetchall()

for i in rows:
    si.append(i)
print si
