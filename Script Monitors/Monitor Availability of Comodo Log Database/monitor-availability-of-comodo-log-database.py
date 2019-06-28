import os 
import sys 
import _winreg 

def alert(arg):
	sys.stderr.write("%d%d%d" % (arg, arg, arg)) 

# Please use "alert(1)" to turn on the monitor(trigger an alert) 
# Please use "alert(0)" to turn off the monitor(disable an alert) 
# Please do not change above block and write your script below 
import os
import sqlite3
import unicodedata
import getpass
import socket
print '\n'
##li=['Alerts','AvEvents','ConfigChanges','DeviceEvents','DfEvents','Events','FileRatingEvents','FwEvents','Jobs','SbEvents','SecureShoppingEvents','TrustedVendorEvents','UrlFilteringEvents','VsEvents']
##print fin_tables
##p=cmp(li,fin_tables)
##if p ==-1:
##    print 'Deleted tables in the log file'
##else:
##    print 'Matched'
print "USER NAME: "+getpass.getuser()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print "IP-ADDRESS : "+(s.getsockname()[0])
from time import gmtime, strftime
time=strftime("%Y-%m-%d %H:%M:%S", gmtime())
k=[]
data=[]
g=[]
print '\n'
drive=os.environ['SystemDrive']
f_loc=os.path.join(drive,os.sep,"ProgramData","Comodo","Firewall Pro")
if os.path.exists(f_loc):
    f_file=os.path.join(f_loc+'\\'"cislogs.sdb")
    if os.path.isfile(f_file):
        try:
            conn = sqlite3.connect(os.path.join(f_loc+'\\'"cislogs.sdb"))
        except IOError:
            print 'UNABLE TO OPEN THE DATABASE'

        cur = conn.cursor();
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        dd=cur.fetchall()
        c=list(dd)
        for f in range(0,len(c)):
            g.append(unicodedata.normalize('NFKD',c[f][0]).encode('ascii','ignore'))
        fin_tables=[i for i in g if not i in ['sqlite_sequence', 'sqlite_stat1']]

        def t_names(names):
            cur.execute('SELECT * FROM %s'%names)
            de=cur.fetchall()
            k.append(len(de))
        for i in range(0,len(fin_tables)):
            t_names(fin_tables[i])
        s=0
        for i in range(0,len(k)):
            s=s+k[i]
        if s==0:
            print 'COMODO LOG DATABASE, INTERNAL TABLES ENTRIES ARE DELETED:'
            alert(1)

        else:
            print 'COMODO LOG DATABASE, INTERNAL TABLES ENTRIES ARE NOT DELETED'
            alert(0)
        conn.close()     
    else:
        print 'COMODO LOG DATABASE FILE  IS MISISING'
        alert(1)

else:
    print 'CCS path doesnt exists in your system'
    



