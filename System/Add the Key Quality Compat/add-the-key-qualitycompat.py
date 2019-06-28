def updatereg():
    import _winreg
    with _winreg.CreateKeyEx(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\QualityCompat", 0, _winreg.KEY_WOW64_64KEY | _winreg.KEY_ALL_ACCESS) as key:
        _winreg.SetValueEx(key, "cadca5fe-87d3-4b96-b7fb-a231484277cc", 0, _winreg.REG_DWORD, 0)
        print "Successfully updated the Registry path!"


def initiatepm():
    import time 
    import os 
    os.popen(r'powershell "Set-ExecutionPolicy RemoteSigned"').read()
    print 'Set out Patch management scanning.....'
    os.popen(r'powershell   "Write-EventLog -LogName System -Source Microsoft-Windows-WindowsUpdateClient -EventId 26 -Message \"Comodo custom event to trigger patch mangment scan\"  " ').read()
    time.sleep(60*60)
    print 'Checking patch management scan...'
    os.popen(r'powershell   "Write-EventLog -LogName System -Source Microsoft-Windows-WindowsUpdateClient -EventId 26 -Message \"Comodo custom event to trigger patch mangment scan\"  " ').read()
    print 'Done'

updatereg()
initiatepm()
