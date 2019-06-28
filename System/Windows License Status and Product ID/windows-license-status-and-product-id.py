import os;
import re;
import ctypes;

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)

tmp = os.environ['TEMP']
filepath = tmp+'\\'+r'GetProductKey.vbs'

decodekey ="""
Set wshShell = CreateObject("Wscript.Shell")
WScript.Echo ConvertToKey(WshShell.RegRead("HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\DigitalProductId"))
Function ConvertToKey(Key)
Const KeyOffset = 52
i = 28
Chars = "BCDFGHJKMPQRTVWXY2346789"
Do
Cur = 0
x = 14
Do
Cur = Cur * 256
Cur = Key(x + KeyOffset) + Cur
Key(x + KeyOffset) = (Cur \ 24) And 255
Cur = Cur Mod 24
x = x -1
Loop While x >= 0
i = i -1
KeyOutput = Mid(Chars, Cur + 1, 1) & KeyOutput
If (((29 - i) Mod 6) = 0) And (i <> -1) Then
i = i -1
KeyOutput = "-" & KeyOutput
End If
Loop While i >= 0
ConvertToKey = KeyOutput
End Function"""

with disable_file_system_redirection():
    with open (filepath,'w+') as obj:
        obj.write(decodekey)
    os.chdir(tmp)
    a=os.getcwd()
    GetKey = os.popen("cscript.exe GetProductKey.vbs").read()
    regex = r"([A-Za-z0-9]{5}-[A-Za-z0-9]{5}-[A-Za-z0-9]{5}-[A-Za-z0-9]{5}-[A-Za-z0-9]{5})"
    result = re.findall(regex,GetKey)
    guid_digital_key=os.popen('cscript C:\Windows\System32\slmgr.vbs /dlv').read();
    os.remove("GetProductKey.vbs")
    guid=os.popen('cscript C:\Windows\System32\slmgr.vbs /dlv').read();
    os_details = os.popen('systeminfo | findstr /B /C:"OS "').read()

if "License Status: Notification" in guid:
    print guid.replace('License Status: Notification','License Status: Windows is not activated');
elif "License Status: Out-Of-Box Grace Period" in guid:
    print guid.replace('License Status: Out-Of-Box Grace Period','License Status: Windows is not activated')
elif "License Status: Out-Of-Tolerance Grace Period" in guid :
    print guid.replace('License Status: Out-Of-Tolerance Grace Period','License Status: Windows is not activated')
elif "License Status: Non-Genuine Grace Period" in guid:
    print guid.replace('License Status: Non-Genuine Grace Period','License Status: Windows is not activated')
elif 'License Status: Extended Grace' in guid:
    print guid.replace('License Status: Extended Grace','License Status: Windows is not activated')
elif 'License Status: Unlicensed' in guid:
    print guid.replace('License Status: Unlicensed','License Status: Windows is not activated')
elif "License Status: Licensed" in guid:
    print guid
else:
    print guid

print "The Digital Product ID is : " +result[0]
print "                                                                                                 "

print "Information on Operating System"
print os_details
