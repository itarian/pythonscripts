# -*- coding: utf-8 -*-
message= itsm.getParameter('get_message') ## Does not support multi line message.
title= itsm.getParameter('get_title')
import os
import ctypes

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text,title, style)

value=Mbox(title,message, 3)
if value == 6:
    print "User clicked Yes Option"
    print 'The Message is sent to the user'
elif value == 7:
    print "User clicked No Option"
elif value == 2:
    print "User pressed close option"
