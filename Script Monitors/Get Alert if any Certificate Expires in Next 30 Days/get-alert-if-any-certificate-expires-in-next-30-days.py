threshold=30
import os
import sys

def alert(arg):
	sys.stderr.write("%d%d%d" % (arg, arg, arg))

def monitorCertExp(threshold):
    def ecmd(CMD):
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
            OBJ = Popen(CMD, shell = True, stdout = PIPE, stderr = PIPE)
        out, err = OBJ.communicate()
        ret=OBJ.returncode
        if ret==0:
            return out.strip()
        else:
            return err.strip()
    def writepsfile(s, p, f):
        import os
        fp=os.path.join(p, f)
        with open(fp, 'wb') as w:
            w.write(s)
        if os.path.isfile(fp):
            return fp
        else:
            return
    import os
    import time
    list1=[]
    temp=os.environ['TEMP']
    cfp=os.path.join(temp, 'getAllCerts_%s.CSV'%(time.strftime('%d%m%y')))
    s=r'''
$Threshold = %s
$Deadline = (Get-Date).AddDays($Threshold)
$Date = Get-Date -Format "yyMMdd"
$ReportPath = "%s"
$Certificates = Get-ChildItem Cert: -Recurse | Where-Object {$_.Subject -ne $null}
$Report =@()
ForEach ($Certificate in $Certificates)
{
    If ($Certificate.NotAfter -le $Deadline){
            $Report += New-Object PSObject -Property @{
                CertificateSubject = $Certificate.Subject
                ExpiresAfter = $Certificate.NotAfter
                ExpiresIn = ($Certificate.NotAfter - (Get-Date)).Days
            }
    }
}
If (($Report | Measure-Object).Count -gt 0) {
        $Report | Select-Object CertificateSubject, ExpiresAfter, ExpiresIn | Sort ExpiresAfter | Export-CSV -Path $ReportPath -NoTypeInformation
		}

Remove-Variable Treshold, Deadline, Certificates, Report, Date -ErrorAction SilentlyContinue
'''%(str(threshold), cfp)
    pf=writepsfile(s, temp, 'getAllCerts.ps1')
    if pf:
        ecmd('powershell -executionpolicy bypass -file %s'%pf)
    if os.path.isfile(cfp):
        os.remove(pf)
        with open(cfp) as r:
            list=r.readlines()
        os.remove(cfp)
    if len(list)>1:
        for i in [(''.join(i.split(',')[:-2]), i.split(',')[-2], i.split(',')[-1]) for i in list]:
            list1.append('{:<170} {:>25}'.format(i[0].replace('"', ''), i[1].replace('"','')))
    if list1:
        return list1
    else:
        return

result=monitorCertExp(threshold)
if len(result)>1:
    temp='\n'
    alert(1)
    for i in result:
        temp+='%s\n'%i
    print temp
else:
    alert(0)
    print 'No Expiring Certificates Found :)'

