content=r'''1.1.1.1 www.facebook.com
2.2.2.2 www.skype.com'''## here mention host file name to change 
 
print 'Before Change: '
with open('C:\Windows\System32\drivers\etc\hosts') as r:
    print r.read()
with open('C:\Windows\System32\drivers\etc\hosts', 'a') as f:
    f.write('\n')
    f.write(content)
print '\n\n\n'
print 'After Change: '
with open('C:\Windows\System32\drivers\etc\hosts') as r:
    print r.read()
