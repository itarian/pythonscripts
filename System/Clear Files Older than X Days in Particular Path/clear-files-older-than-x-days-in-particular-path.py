Threshold_day=itsm.getParameter('Threshold_Value') ## Here mention number of days to delete file more than given days
print "Threshold days given in the script: "+ Threshold_day
print "****************************************"
import os
import time
import ctypes
import datetime
import getpass
import shutil
from datetime import datetime
class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)
drive=os.environ['SystemDrive']
Path=[]
del_dir=[]
USER=os.popen("wmic useraccount get Name").read()
Name=[i.strip() for i in  USER.split("\n") if i.strip()]
Profile=Name[1:]
print 'Deleting files begins...  '
with disable_file_system_redirection(): 
        for j in Profile:
            temp = drive+"\\Users\\%s\\Desktop" %(j)
            del_dir.append(temp);
        for i in del_dir:
            for dirpath, dirnames, files in os.walk(i):
                names=os.listdir(dirpath)
                for i in names:            
                    print "File Name: "+ i
                    fpath= os.path.join(dirpath,i)
                    os.chdir(dirpath)
                    str_date= time.ctime(os.stat(fpath).st_ctime)
                    d_date = datetime.strptime(str_date , '%a %b %d %H:%M:%S %Y')
                    now = datetime.now() 
                    file2_date=now.strftime("%Y-%m-%d %H:%M:%S")
                    d_d2 = datetime.strptime( file2_date,"%Y-%m-%d %H:%M:%S")
                    file1_date = d_date.strftime("%Y-%m-%d %H:%M:%S")
                    file2_date= datetime.strptime(file2_date, "%Y-%m-%d %H:%M:%S").date()
                    file1_date= datetime.strptime(file1_date, "%Y-%m-%d %H:%M:%S").date()
                    date_format = "%Y-%m-%d %H:%M:%S"
                    day1 =  datetime.strptime("%s"%d_date, date_format)
                    day2 =  datetime.strptime("%s"%d_d2, date_format)
                    diff = day2 - day1
                    days = diff.days
                    j=(str(days))
                    days_to_hours = days * 24
                    No_days=(str(days))
                    print "Number Of days from creation:"+ No_days
                    diff_btw_two_times = (diff.seconds) / 3600
                    overall_hours = days_to_hours + diff_btw_two_times
                    No_hours=(str(overall_hours));
                    if No_days > Threshold_day:
                        if os.path.exists(i):                            
                            os.chmod(i,0644)
                            if os.path.isfile(i):
                                os.remove(i)
                            else:
                                shutil.rmtree(i)
                    print "Deleting file:"+ i
                    print "Files Deleted Successfully"
