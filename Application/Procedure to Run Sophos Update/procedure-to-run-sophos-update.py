import os;
file='sophosupdate.vbs';
input="""dim objALC : set objALC = CreateObject("ActiveLinkClient.ClientUpdate.1")
objALC.UpdateNow 1,1
"""
fobj= open(file, "w");
fobj.write(input);
fobj.close();
out=os.popen('cscript.exe  '+file).read();
print(out);
os.remove("sophosupdate.vbs")