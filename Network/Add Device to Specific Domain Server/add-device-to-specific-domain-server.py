
#Enter your domain details
domain_name="test"
domain_ip="10.10.10.10"
domain_admin="Administrator"
domain_pass="Passw0rd"

import os
import re
join_login=domain_name+'\\'+domain_admin
print (join_login)
drive=os.environ['SYSTEMDRIVE']
get_version=os.popen(drive+r'\Windows\System32\WindowsPowerShell\v1.0\powershell.exe "Get-Host | findstr "Version""').read();
version= re.findall("\d",get_version)[0]

dns_command='wmic nicconfig where (IPEnabled=TRUE) call SetDNSServerSearchOrder ("'+domain_ip+'")'
print(dns_command)
set_dns=os.popen(dns_command).read()
print (set_dns)

version_2='''
$secpasswd = ConvertTo-SecureString "%s" -AsPlainText -Force
$creden = New-Object System.Management.Automation.PSCredential ("%s", $secpasswd)
Add-Computer -DomainName "%s"  -Credential  $creden  -PassThru  -Verbose
Restart-Computer -Force
'''

version_2_update=version_2 % (domain_pass,join_login,domain_name)

version_3='''
$secpasswd = ConvertTo-SecureString "%s" -AsPlainText -Force
$creden = New-Object System.Management.Automation.PSCredential ("%s", $secpasswd)
Add-Computer -DomainName "%s" -ComputerName "localhost"  -Credential $creden -Verbose -Force -PassThru
Restart-Computer -Force
'''

version_3_update=version_3 % (domain_pass,join_login,domain_name)



def change_domain(script):
    temp=os.environ['TEMP']
    file=temp+'\\domain_update.ps1'
    obj=open(file,"w")
    obj.write(script)
    obj.close()
    command=drive+'\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe  -executionpolicy RemoteSigned  -File  '+file
    output=os.popen(command).read()
    return(output)

if int(version)==2:
    print change_domain(version_2_update)    
elif int(version) >= 3:
    print change_domain(version_3_update)

else:
    print 'Powershell version in your OS must not be less that 2.0'
try:    
    if os.path.isfile(file):
        os.remove(file)
except:
    pass
