import os
cmd=os.popen('launchctl unload -w /System/Library/LaunchAgents/com.apple.notificationcenterui.plist; killall NotificationCenter').read()
cmd1=os.popen('sudo rm /Library/LaunchAgents/com.comodo.osxclient.plist').read()
cmd2=os.popen('sudo shutdown -r now').read()
print 'comodo client communication icon is hided'

