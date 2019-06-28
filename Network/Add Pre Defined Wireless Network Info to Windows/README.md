We can add a wireless network to the system using import/export profile option available in the Windows OS.

1. Initially, you should export desired wireless network profile from configured system to network or share path. Please try below command with administrator privilege to achieve it,


netsh wlan show profiles - Shows list of wireless profile available in the system

netsh wlan export profile name="profile-name" folder="networkpath" - Export wireless profile to mentioned folder path

sample network or share path is "\\fileserver.net\Common\network"
sample wireless profile is "Wi-Fi"

2. Now, you can see exported XML file in the network/shared path. Example Wireless Network Connection-"profile-name".xml

3. Finally, run below script with the correct profile_path variable.