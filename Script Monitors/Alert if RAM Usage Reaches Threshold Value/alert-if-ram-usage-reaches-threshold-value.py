Threshold_Value = 70        #Value in percentage 
oper            = ">="      #Give the operator to compare

import os
import ctypes
import re
import operator
import sys

Ram_avail = []
Drive = os.environ['SYSTEMDRIVE']
GetFreeMemory = 'systeminfo | findstr /'+ Drive +'"Total Physical Memory" /'+Drive+'"Available Physical Memory"'

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

def alert(arg): 
   sys.stderr.write("%d%d%d" % (arg, arg, arg)) 

operator_dict ={
   '>': operator.gt,
   '<': operator.lt,
   '>=': operator.ge,
   '<=': operator.le}

with disable_file_system_redirection():
    Run_GetFreeMemory = os.popen(GetFreeMemory).read()
    process=os.popen('tasklist /v /FI "MEMUSAGE ge 10000" | sort /+67 /R').readlines()

for i in [i.strip() for i in Run_GetFreeMemory.split('\n')  if i.strip()]:
    value = re.sub("\D", "", i)
    Ram_avail.append(value)


value1 = int(Ram_avail[0])
value2 = int(Ram_avail[1])
value3  = value1 - value2
value4 = float(value3)/float(value1)
value5 = value4*100
Ram_Usage = int(value5)
Ram_Mon= (operator_dict[oper](Ram_Usage,Threshold_Value))

if Ram_Mon is True:
    alert(1)
    print "The RAM usage reached its threshold limit \n"
    print "The given threshold is ",Threshold_Value,"Percent"
    print "The Ram usage is ", Ram_Usage,"Percent"
    print "\n"
    print 'Top RAM memory consuming processes \n'
    try:
        for i in range(1,7,1):
            print (process[i])
    except:
        pass
else:
    alert(0)
    print "The RAM usagae falls within the threshold \n "
    print "The given threshold is ",Threshold_Value,"Percent"
    print "\n"
    print "The Ram usage is ", Ram_Usage,"Percent"
    print "\n"
