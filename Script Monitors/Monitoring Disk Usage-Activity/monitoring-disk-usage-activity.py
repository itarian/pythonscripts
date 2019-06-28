# The script is a template to check UAC status on the device.
threshold=10
import os
import sys
import _winreg
def alert(arg):
    sys.stderr.write("%d%d%d" % (arg, arg, arg))

# Please use "alert(1)" to turn on the monitor(trigger an alert)
# Please use "alert(0)" to turn off the monitor(disable an alert)
# Please do not change above block and write your script below
def disk():
    import os
    import ctypes
    import sys
    import getpass
    import socket
    print "USER NAME: "+getpass.getuser()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print "IP-ADDRESS : "+(s.getsockname()[0])
    from time import gmtime, strftime
    time=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print '\n'
    powershell_script=r"""
    Clear-Host
    $Disk = Get-WmiObject -class Win32_PerfRawData_PerfDisk_LogicalDisk `
    -filter "name= '_Total' "
    $disktranferpersec=$DisK.DiskTransfersPersec
    $a=($disktranferpersec /1000)*0.00009765625
    "disktranferpersec(iops)="+" {0:P0}" -f $a


    $DBytes = $Disk.DiskBytesPerSec;
    "Disk KBytes/sec(Throughput) = "+[int]($DBytes /1000)


    $DRead = $Disk.DiskReadBytesPerSec;
    "Disk Reads/sec = " + ($DRead /1000)
    $DWrite = $Disk.DiskWriteBytesPerSec;
    "Disk Writes/sec = " +($DWrite /1000)

    $PercentDiskTime=$Disk.PercentDiskTime;
    "PercentDisktime= "+($PercentDiskTime)

    $PercentIdleTime=$Disk.PercentIdleTime;
    "DISK IDLE TIME= " +($PercentIdleTime)

    $Avgdiskbytespertransfer=$Disk.AvgDiskBytesPerTransfer;

    "Avg.Disk Bytes/Transfer(Io Size)=  "+($Avgdiskbytespertransfer)

    $avgdisksectranfer=$Disk.AvgDisksecPerTransfer;
    "Avg.DiskSec/transfer(Average Latency)seconds= "+($avgdisksectranfer)

    """

    workdir=os.environ['PROGRAMDATA']+r'\c1_temp'
    if not os.path.isdir(workdir):
        os.mkdir(workdir)


    fobj=open(workdir+r'\io.ps1',"w")
    fobj.write(powershell_script)
    fobj.close()

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
        def ecmd(cmd, r=False):
            import ctypes
            class disable_file_system_redirection:
                _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
                _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
                def __enter__(self):
                    self.old_value = ctypes.c_long()
                    self.success = self._disable(ctypes.byref(self.old_value))
                def __exit__(self, type, value, traceback):
                    if self.success:
                        self._revert(self.old_value)
            from subprocess import PIPE, Popen
            with disable_file_system_redirection():
                OBJ = Popen(cmd, shell = True, stdout = PIPE, stderr = PIPE)
            out, err = OBJ.communicate()
            ret=OBJ.returncode
            if r:
                if ret==0:
                    return out
                else:
                    return err
            else:
                return ret
        out=ecmd(r'powershell.exe -executionpolicy bypass -file "'+workdir+r'\io.ps1"',True)
        v=out.split('\n')[0]
        a,b=v.split("=")
        z=b.strip("%\r\n")
        p= (int(z))
        t= threshold
        if p > t:
            alert(1)
            print v
            print 'Your DISK UTILIZATION is more than  Threshold '
            print '\n'
            print 'For more details of disk UTILIZATION :'
            f=out.split('\n')
            f.pop(0)
            for i in f:
                print'\t' + i

        else:
            print 'Your DISK UTILIZATION is less than Threshold '
            alert(0)


    os.remove(workdir+r'\io.ps1')

disk()
