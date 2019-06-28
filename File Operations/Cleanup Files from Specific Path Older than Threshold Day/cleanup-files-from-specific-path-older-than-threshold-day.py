path=r"C:\Program Files (x86)\Comodo\Comodo ITSM\rmmlogs" ## Here mention the path of th file
Threshold_day='1' ## Here mention number of days to delete file more than given days
print "Threshold days given in the script: "+ Threshold_day
print "****************************************"
import os
import time
import ctypes
import datetime
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

with disable_file_system_redirection():
    result=os.listdir(path)
    print '*********Cleanup logs **********'
    for i in result:           
        print "File Name: "+ i
        fpath=os.path.join(path,i);
        str_date= time.ctime(os.stat(fpath).st_ctime)
        d_date = datetime.strptime(str_date , '%a %b %d %H:%M:%S %Y')
        now = datetime.now() 
        file2_date=now.strftime("%Y-%m-%d %H:%M:%S")
        d_d2 = datetime.strptime( file2_date,"%Y-%m-%d %H:%M:%S")
        file1_date = d_date.strftime("%Y-%m-%d %H:%M:%S")
        print "File Creation date: "+ file1_date
        print "Current date: "+ file2_date
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
            try:
                    if os.path.isfile(fpath):
                        os.chmod(fpath,0644)
                        os.remove(fpath)
                        print "Deleting file:"+ i
                        print "Deleted Successfully"
            except Exception as error:
                print "The files working in another process:" +  fpath +"\n"
                            
