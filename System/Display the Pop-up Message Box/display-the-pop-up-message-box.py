# -*- coding: utf-8 -*-
message="This is regarding getting confirmation from you to have your time. Are you available now ?" #edit with your message here
title="Message from administrator" #edit with your title here
import Tkinter as tk
import tkMessageBox as messagebox
root = tk.Tk().withdraw()
value=messagebox.askquestion(title, message)
if value == 'yes' :
    print "User clicked Yes Option"
    print 'The following message is sent to the user.\n%s'%message
else:
    print "User clicked No Option"
 
