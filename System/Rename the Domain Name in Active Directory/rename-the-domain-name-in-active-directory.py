# -*- coding: utf-8 -*-

Domain="c1ops"
ext=".com"

import os
import subprocess
from subprocess import PIPE, Popen
import re
import codecs
import shutil

Domain_name=Domain+ext
Domain_U=Domain.upper()
b=[]
f=[]

try:
    file_dir=os.environ['PROGRAMDATA']+r'\temp'
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)      
except:
    file_dir=os.environ['SYSTEMDRIVE']


def run(cmd):
    os.chdir(file_dir)
    obj = subprocess.Popen(cmd, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = obj.communicate()
    return out

def change_name():
    with open(file_dir+'\\test_test.txt', 'r+') as dr:
        data=dr.readlines()
        for i in data:
            j=re.findall('<DNSname>(.*)</DNSname>', i)
            z=re.findall('<NetBiosName>(.*)</NetBiosName>', i)
            ge=str(z)
            if ge.isupper():
                ge=ge.replace("'","")
                ge=ge.replace("[","")
                ge=ge.replace("]","")
                b.append(ge)
            if not j:
                pass
            else:
                g=str(j)               
                g=g.replace("'","")
                g=g.replace("[","")
                g=g.replace("]","")
                b.append(g)

    with open(file_dir+'\\test_test.txt') as f:
        with open(file_dir+'\\test_convert.txt', "w") as f1:
            for line in f:
                if b[-1] in line:
                    line=line.replace(b[-1], Domain_U)
                    f1.write(line)
                elif b[-2] in line:
                    line=line.replace(b[-2], Domain_name)
                    f1.write(line)
                else:
                    f1.write(line)


def covert_xml():
    if os.path.exists(xml_file):
        os.remove(xml_file)

    with codecs.open(file_dir+'\\test_convert.txt', encoding="utf-8") as input_file:
        with codecs.open(xml_file, "w", encoding="utf-16") as output_file:
            shutil.copyfileobj(input_file, output_file)

    os.remove(file_dir+'\\test_convert.txt')
    os.remove(file_dir+'\\test_test.txt')
    

    if os.path.exists(xml_file):
        print "Domainlist.xml has created\n"

    
cmd1="rendom /list"
res=run(cmd1)
print res
xml_file=file_dir+r'\\Domainlist.xml'
if os.path.isfile(xml_file):
    sourceEncoding = "utf-16"
    targetEncoding = "utf-8"
    source = open(xml_file)
    target = open(file_dir+'\\test_test.txt', "w")
    target.write(unicode(source.read(), sourceEncoding).encode(targetEncoding))
    source.close()
    target.close()
    change_name()
    covert_xml()
    
else:
    print "Couldn't create Domainlist.xml file"


cmd2="rendom /upload"
res=run(cmd2)
print res
if "A domain rename operation is already in progress" in res:
    cmd3="rendom /end"
    res=run(cmd3)
    print res
    print "\nKilled the exisiting Process\n"
    res=run(cmd2)
    print res

cmd4="rendom /prepare"
res=run(cmd4)
print res

cmd5="rendom /execute"
res=run(cmd5)
print res
print "\n\nSYSTEM IS ABOUT TO RESTART TO CHANGE EFFECT\n\n"
