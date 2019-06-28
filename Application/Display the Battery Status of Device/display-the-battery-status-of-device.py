import os
command=os.popen('WMIC Path Win32_Battery Get BatteryStatus').read()
if "BatteryStatus" in command:
    os.popen(r'powershell "Set-ExecutionPolicy RemoteSigned"').read()
    charge_left=os.popen("powershell (Get-WmiObject -Class Win32_Battery).estimatedchargeremaining").read()
    print type(charge_left)
    print "Battery charge left is: ",charge_left
    charge=os.popen("powershell (Get-WmiObject -Class Win32_Battery -ea 0).BatteryStatus").read()
    charge=int(charge)
    dict={1:'Battery is discharging',2:'Battery is charging',3:'Fully Charged',4:'Battery is low',5:'Critical!!'}
    print dict[charge]   
else:
    print "No battery in the device to display the status"
