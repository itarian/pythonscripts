path=r"C:\Users\C1-En_230\Downloads"  # Give the Path want to monitor
path_to_bckup=r"C:\Users\C1-En_230\Desktop\Backup" #Give the path where want to store backedup files.


import os
import ctypes
import re
import time
import shutil
import datetime
import socket
import platform
import sys


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


def file_owner(filename):
    import ctypes as ctypes
    from ctypes import wintypes as wintypes

    advapi32 = ctypes.WinDLL('advapi32', use_last_error=True)

    # required constants
    ERROR_INSUFFICIENT_BUFFER = 0x007A
    OWNER_SECURITY_INFORMATION = 0x00000001

    # related constants
    ERROR_INVALID_FUNCTION = 0x0001
    ERROR_FILE_NOT_FOUND   = 0x0002
    ERROR_PATH_NOT_FOUND   = 0x0003
    ERROR_ACCESS_DENIED    = 0x0005
    GROUP_SECURITY_INFORMATION     = 0x00000002
    DACL_SECURITY_INFORMATION      = 0x00000004
    SACL_SECURITY_INFORMATION      = 0x00000008
    LABEL_SECURITY_INFORMATION     = 0x00000010
    ATTRIBUTE_SECURITY_INFORMATION = 0x00000020
    SCOPE_SECURITY_INFORMATION     = 0x00000040
    BACKUP_SECURITY_INFORMATION    = 0x00010000
    UNPROTECTED_SACL_SECURITY_INFORMATION = 0x10000000
    UNPROTECTED_DACL_SECURITY_INFORMATION = 0x20000000
    PROTECTED_SACL_SECURITY_INFORMATION   = 0x40000000
    PROTECTED_DACL_SECURITY_INFORMATION   = 0x80000000

    # type definitions
    LPBOOL  = ctypes.POINTER(wintypes.BOOL)
    LPDWORD = ctypes.POINTER(wintypes.DWORD)
    PSID = ctypes.POINTER(wintypes.BYTE)
    PSECURITY_DESCRIPTOR = ctypes.POINTER(wintypes.BYTE)
    SECURITY_INFORMATION = wintypes.DWORD

    class SID_NAME_USE(wintypes.DWORD):
        _sid_types = dict(enumerate('''
            User Group Domain Alias WellKnownGroup DeletedAccount
            Invalid Unknown Computer Label'''.split(), 1))

        def __init__(self, value=None):
            if value is not None:
                if value not in self.sid_types:
                    raise ValueError('invalid SID type')
                wintypes.DWORD.__init__(value)

        def __str__(self):
            if self.value not in self._sid_types:
                raise ValueError('invalid SID type')
            return self._sid_types[self.value]

    PSID_NAME_USE = ctypes.POINTER(SID_NAME_USE)

    # function pointer prototypes

    def _check_bool(result, func, args,
                    WinError=ctypes.WinError,
                    get_last_error=ctypes.get_last_error):
        if not result:
            raise WinError(get_last_error())
        return args

    # msdn.microsoft.com/en-us/library/aa446639
    advapi32.GetFileSecurityW.errcheck = _check_bool
    advapi32.GetFileSecurityW.argtypes = (
        wintypes.LPCWSTR,     # _In_      lpFileName
        SECURITY_INFORMATION, # _In_      RequestedInformationRequested
        PSECURITY_DESCRIPTOR, # _Out_opt_ pSecurityDescriptor
        wintypes.DWORD,       # _In_      nLength
        LPDWORD)              # _Out_     lpnLengthNeeded

    # msdn.microsoft.com/en-us/library/aa446651
    advapi32.GetSecurityDescriptorOwner.errcheck = _check_bool
    advapi32.GetSecurityDescriptorOwner.argtypes = (
        PSECURITY_DESCRIPTOR,  # _In_  pSecurityDescriptor
        ctypes.POINTER(PSID),  # _Out_ pOwner
        LPBOOL)                # _Out_ lpbOwnerDefaulted

    # msdn.microsoft.com/en-us/library/aa379166
    advapi32.LookupAccountSidW.errcheck = _check_bool
    advapi32.LookupAccountSidW.argtypes = (
        wintypes.LPCWSTR, # _In_opt_  lpSystemName
        PSID,             # _In_      lpSid
        wintypes.LPCWSTR, # _Out_opt_ lpName
        LPDWORD,          # _Inout_   cchName
        wintypes.LPCWSTR, # _Out_opt_ lpReferencedDomainName
        LPDWORD,          # _Inout_   cchReferencedDomainName
        PSID_NAME_USE)    # _Out_     peUse

    def get_file_security(filename, request):
        length = wintypes.DWORD()
        # N.B. This query may fail with ERROR_INVALID_FUNCTION
        # for some filesystems.
        try:
            advapi32.GetFileSecurityW(filename, request, None, 0,
                ctypes.byref(length))
        except WindowsError as e:
            if e.winerror != ERROR_INSUFFICIENT_BUFFER:
                raise
        if not length.value:
            return None
        sd = (wintypes.BYTE * length.value)()
        advapi32.GetFileSecurityW(filename, request, sd, length,
            ctypes.byref(length))
        return sd

    def look_up_account_sid(sid):
        SIZE = 256
        name = ctypes.create_unicode_buffer(SIZE)
        domain = ctypes.create_unicode_buffer(SIZE)
        cch_name = wintypes.DWORD(SIZE)
        cch_domain = wintypes.DWORD(SIZE)
        sid_type = SID_NAME_USE()
        advapi32.LookupAccountSidW(None, sid, name, ctypes.byref(cch_name),
            domain, ctypes.byref(cch_domain), ctypes.byref(sid_type))
        return name.value, domain.value, sid_type

    def get_file_owner(filename):
        sd = get_file_security(filename, OWNER_SECURITY_INFORMATION)
        sid = PSID()
        sid_defaulted = wintypes.BOOL()
        advapi32.GetSecurityDescriptorOwner(sd, ctypes.byref(sid),
            ctypes.byref(sid_defaulted))
        name, domain, sid_type = look_up_account_sid(sid)
        return name, domain, sid_type



    import sys


    if isinstance(filename, bytes):
        filename = filename.decode('mbcs')

    name, domain, sid_type = get_file_owner(filename)

    if domain:
        name =  '{0}\\{1}'.format(domain, name)
    print("\nFile : {0}".format(filename))
    print("Owner: {0} ({1})".format(name, sid_type))


    
def check():
    with disable_file_system_redirection():
        os.chdir(path)
        inst=os.popen("cipher").read()
         
    return inst
        


def again():
    with disable_file_system_redirection():
        os.chdir(path)
        ins=os.popen("wmic product get name,identifyingnumber").read()
        if 'Veeam Agent' in ins:
            print "\n Veeam Agent is installed on Endpoint"
            print "\n Veeam agent is Backing up your files, takes time to finish up based on FILE SIZES"
            veeam()
        else:
            print "\nCouldn't find Veeam Agent on Endpoint"
            print "\n Please Install Veeam Agent to start Backup"
        

def veeam ():
    os.chdir(path)
    os.popen('"C:\Program Files\Veeam\Endpoint Backup\Veeam.EndPoint.Manager.exe" /standalone '+path_to_bckup)
    time.sleep(60)
    os.chdir(path_to_bckup)
    so=os.popen('dir').read()
    if "Backup Job" in so:
        print "\n Backup is completed and stored in specified path"



inst=check()

 
if len(inst)>0:
    find=re.findall('E\s(.*)',inst)

    if len(find)>0:
        alert(1)
        print "\nFound Encrypted files on Specified path:\n"
        print "User IP :"+socket.gethostbyname(socket.gethostname())
        print "Os Details :"+platform.platform()
        for f in find:
            fn=path+'\\'+f
            file_owner(fn)
            print "File Created Date : "+time.strftime("%Y/%m/%d",time.localtime(os.path.getctime(path+'\\'+f)))
            print "File Created Time : "+time.strftime("%I:%M:%S %p",time.localtime(os.path.getctime(path+'\\'+f)))
            print "File Modified Date: "+time.strftime("%Y/%m/%d",time.localtime(os.path.getmtime(path+'\\'+f)))
            print "File Modified Time: "+time.strftime("%I:%M:%S %p",time.localtime(os.path.getmtime(path+'\\'+f)))
           
        print "\n Checking for Veeam agent status in Endpoint"
        again()


    else:
        print "No file is Encrypted in Specified path"
        alert(0)



