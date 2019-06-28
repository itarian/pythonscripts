vbs=r'''
Option Explicit 

Dim objshell,path,DigitalID, Result 
Set objshell = CreateObject("WScript.Shell")
'Set registry key path
Path = "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\"
'Registry key value
DigitalID = objshell.RegRead(Path & "DigitalProductId")
Dim ProductName,ProductID,ProductKey,ProductData
'Get ProductName, ProductID, ProductKey
ProductName = "Product Name: " & objshell.RegRead(Path & "ProductName")
ProductID = "Product ID: " & objshell.RegRead(Path & "ProductID")
ProductKey = "Installed Key: " & ConvertToKey(DigitalID) 
ProductData = ProductName  & vbNewLine & ProductID  & vbNewLine & ProductKey
WScript.StdOut.Write(ProductData)


'Convert binary to chars
Function ConvertToKey(Key)
    Const KeyOffset = 52
    Dim isWin8, Maps, i, j, Current, KeyOutput, Last, keypart1, insert
    'Check if OS is Windows 8
    isWin8 = (Key(66) \ 6) And 1
    Key(66) = (Key(66) And &HF7) Or ((isWin8 And 2) * 4)
    i = 24
    Maps = "BCDFGHJKMPQRTVWXY2346789"
    Do
       	Current= 0
        j = 14
        Do
           Current = Current* 256
           Current = Key(j + KeyOffset) + Current
           Key(j + KeyOffset) = (Current \ 24)
           Current=Current Mod 24
            j = j -1
        Loop While j >= 0
        i = i -1
        KeyOutput = Mid(Maps,Current+ 1, 1) & KeyOutput
        Last = Current
    Loop While i >= 0 
    keypart1 = Mid(KeyOutput, 2, Last)
    insert = "N"
    KeyOutput = Replace(KeyOutput, keypart1, keypart1 & insert, 2, 1, 0)
    If Last = 0 Then KeyOutput = insert & KeyOutput
    ConvertToKey = Mid(KeyOutput, 1, 5) & "-" & Mid(KeyOutput, 6, 5) & "-" & Mid(KeyOutput, 11, 5) & "-" & Mid(KeyOutput, 16, 5) & "-" & Mid(KeyOutput, 21, 5)
   
    
End Function
'''
import os
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


def runvbs(vbs):
    workdir=os.environ['PROGRAMDATA']+r'\temp'
    if not os.path.isdir(workdir): 
        os.mkdir(workdir)
    with open(workdir+r'\temprun.vbs',"w") as f :
        f.write(vbs)        
    with disable_file_system_redirection():
        print os.popen('cscript.exe "'+workdir+r'\temprun.vbs"').read()
    if os.path.isfile(workdir+r'\temprun.vbs'):
        os.remove(workdir+r'\temprun.vbs')

runvbs(vbs) 

