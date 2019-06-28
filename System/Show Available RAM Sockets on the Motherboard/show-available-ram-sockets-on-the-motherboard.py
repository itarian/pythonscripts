import os
import ctypes

Drive = os.environ['SYSTEMDRIVE']
GetRamSlots = "wmic memphysical get memorydevices"
GetRamSoltCapacity = "wmic memphysical get MaxCapacity" 
GetUsedSolt = "wmic MEMORYCHIP get Banklabel,DeviceLocator,MemoryType,TypeDetail,speed"
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

with disable_file_system_redirection():
    Run_GetRamSlots = os.popen(GetRamSlots).read()
    Run_GetRamSoltCapacity = os.popen(GetRamSoltCapacity).read()
    Run_GetUsedSolt = os.popen(GetUsedSolt).read()
    Run_GetFreeMemory = os.popen(GetFreeMemory).read()
print "Getting RAM details.. \n"
for i in [i.strip() for i in Run_GetRamSlots.split('\n') if 'MemoryDevices' not in i if i.strip()]:
    print "The Number of RAM slots available:"+i+"\n"

for i in [i.strip() for i in Run_GetRamSoltCapacity.split('\n') if 'MaxCapacity' not in i if i.strip()]:
    B = int(i)
    GB = 1024*1024.0
    Convert = B/GB
    print "The capacity of each RAM per slot is:",Convert , "GB"
    print "\n"
c = 0 
for i in [i.strip() for i in Run_GetUsedSolt.split('\n') if 'BankLabel' not in i if i.strip()]:
    c =c+1
print "The number of used slot(s):", c
print "The details of the used slots:"
print Run_GetUsedSolt


print "The installed RAM memory details:"
print Run_GetFreeMemory
print "\n"



