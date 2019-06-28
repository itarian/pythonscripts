
name='"Syria Standard Time"'   #provide the name of the time zone to be changed
#If name is in string, enclose it in '" "'- eg:'"Syria Standard Time"'
#If name is in String+number, enclose it in " " - eg: "UTC+13"

import os
import re
print"-------- TIME ZONE--------\n"

print("The current time zone is")
cur_zon=os.popen("TZUTIL /g ").read()
print cur_zon
print("------CHANGING TIME ZONE------------\n")

change=os.popen("TZUTIL /s "+name).read()
print change

print("The Changed current time zone is")
cur_zone=os.popen("TZUTIL /g ").read()
print cur_zone
