val=60 ## delays for 1 minute.It will delay the timeout setting
message="Hi, Please leave your computer from 1PM to 2PM, We need to do some maintenance activities." ## Does not support multi line message.
title="Message from: Administrator"

import ctypes
import time
from threading import Thread
from ctypes.wintypes import HWND, LPWSTR, UINT

_user32 = ctypes.WinDLL('user32', use_last_error=True)

_MessageBoxW = _user32.MessageBoxW
_MessageBoxW.restype = UINT 
_MessageBoxW.argtypes = (HWND, LPWSTR, LPWSTR, UINT)

def MessageBoxW(hwnd, text, caption, utype):
    result = _MessageBoxW(hwnd, text, caption, utype)
    if not result:
        raise ctypes.WinError(ctypes.get_last_error())
    return result

def main():
    result = MessageBoxW(None, message, title , 0)
    if result == 1:
        print "User pressed ok button"
    else:
        print "User doesnt pressed any option"
    time.sleep(val)   

if __name__ == "__main__":
    main()
