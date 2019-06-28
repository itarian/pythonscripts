#To define a particular parameter, replace the 'parameterName' inside itsm.getParameter('parameterName') with that parameter's name
kb_list_user=itsm.getParameter('KB_to_Uninstall') # List
import os
import re

match=[]
notmatch=[]
def ecmd(CMD, r=False):
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
    if r:
        return ret
    else:            
        if ret==0:
            return out,ret
        else:
            return err,ret
cmd, ret1=ecmd('dism /online /get-packages /format:table')
#Display the kb_list to user.
print '\n'
if ret1 == 740:
    print 'No KB_UPDATES for security/update, found in your system'
else:
    kb_list=[]
    for i in cmd.split():
        if i.startswith('Package_for_KB'):
            kb_list.append(''.join(i.split(' ')))

    print 'Total number of KBUPDATES present in your system: %d' %len(kb_list)
    print '\nList of kb which are present in your system.'
    for j in range(0,len(kb_list)):
        print '\n\t*)',kb_list[j]
        kb_list[j].strip('Package_for_KB')
    print '\n'
    if len(kb_list) == 0:
        print 'No KB_UPDATES for security/update found in your system'
    elif not kb_list_user and len(kb_list)!=0:
        print 'Please provide kb_update number in the kb_list_user list: '        
    else:
        print "\nUNINSTALLATION OF KB BYTES....."
        for i in range(0,len(kb_list)):
            for j in range(0,len(kb_list_user)):
                if kb_list[i].strip('Package_for_KB') in kb_list_user[j]:                    
                    s= kb_list_user[j]
                    match.append(s)     

if not kb_list_user and len(kb_list)!=0:
    pass
else:
    if match:
        print '\n The below KB numbers specified are Matched with installed updates\n'
        for i in range(0,len(match)):
            print match[i]
            fin=ecmd('DISM.exe /Online /Remove-Package /PackageName:%s /quiet /norestart'%match[i],False)
            fin1=re.findall("\(\'\'\,\s\-(.*)",str(fin))
            if fin1:
                print '\t*)',match[i],'- Uninstall Failed- Update for the specified KB is required and so it cannot be uninstalled'
            else:
                print '\t*)',match[i],'- Uninstall Success- Uninstall KB update successfully'
        
        for i in kb_list_user:
            if not i in match:
                print '\n The below KB numbers specified are not Matched with installed updates\n'
                print '\t*)', i
    else:
        print '\n None of the kb values specified are Matched with installed updates\n' 
