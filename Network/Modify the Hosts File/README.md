Please use the script to modify the Hosts file on your windows machine which helps you to update the website list that you want to block surfing on your endpoint.

You can change the variable 'content' as per your requirement.

If you want to block www.facebook.com and www.msdn.com then you can change the variable values as follows
content=r'''1.1.1.1 www.facebook.com
1.1.1.2 www.msdn.com'''

Note:
your list of IP address and website domain should be as r'''IP1<space>Domain1<enter>IP2<space>Domain2'''
 

This Script run as a "System User"

This Script run as a system User.