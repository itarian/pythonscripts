def initiatepm():
    import time 
    import os 
    os.popen(r'powershell "Set-ExecutionPolicy RemoteSigned"').read()
    print 'Setting OS Patch scanning.....'
    os.popen(r'powershell   "Write-EventLog -LogName System -Source Microsoft-Windows-WindowsUpdateClient -EventId 26 -Message \"Comodo custom event to trigger patch mangment scan\"  " ').read()
    print "Triggered OS Patch Scanning"
    time.sleep(61*60)
    os.popen(r'powershell   "Write-EventLog -LogName System -Source Microsoft-Windows-WindowsUpdateClient -EventId 26 -Message \"Comodo custom event to trigger patch mangment scan\"  " ').read()
    print "Initiated OS Patch Scanning"


initiatepm()
