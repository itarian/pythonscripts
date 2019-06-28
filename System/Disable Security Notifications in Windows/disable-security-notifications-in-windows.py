import _winreg
import os

lk = ['HKEY_CURRENT_USER\\Software\\Policies\\Microsoft\\Windows\\Explorer','HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\PushNotifications']
lv = ['DisableNotificationCenter', 'ToastEnabled']
lt = [_winreg.REG_DWORD, _winreg.REG_DWORD]
ld = [1, 0]
d = {'lk':lk, 'lv':lv, 'lt':lt, 'ld':ld}
rl = []
c = 0
for i in d['lk']:
    li = i.split(os.sep)
    rkey = getattr(_winreg, li[0])
    skey = os.sep.join(li[1:])
    try:
        ok = _winreg.OpenKey(rkey, skey, 0, _winreg.KEY_ALL_ACCESS)
    except:
        _winreg.CreateKeyEx(rkey, skey, 0, _winreg.KEY_ALL_ACCESS)
        ok = _winreg.OpenKey(rkey, skey, 0, _winreg.KEY_ALL_ACCESS)
    try:
        _winreg.SetValueEx(ok, d['lv'][c], 0, d['lt'][c], d['ld'][c])
        rl.append(1)
    except:
        rl.append(0)
    c += 1

if rl[0] == 1 and rl[1] == 1:
    print 'security notifications is disabled successfully'
else:
    print 'sorry, security notifications is not disabled!'
