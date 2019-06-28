#Enter 1 to send  csv report in email  #Enter 0 to  print the output in ITSM portal
sendemail=1

#Edit Email recipients and smtp details if you wish to email report
emailto =['xyz@gmail.com','pqr@gmail.com'] 
emailfrom = "yyyyy@gmail.com"
password = "12345678"
smtpserver='smtp.gmail.com'
port=587



import os
import sqlite3
import csv


def CheckApp(AppName):
    import _winreg
    import os
    AppName = AppName.lower()
    def DNDS(rtkey, pK, kA):
        ln = []
        lv = []
        try:
            oK = _winreg.OpenKey(rtkey, pK, 0, kA)
            i = 0
            while True:
                try:
                    bkey = _winreg.EnumKey(oK, i)
                    vkey = os.path.join(pK, bkey)
                    oK1 = _winreg.OpenKey(rtkey, vkey, 0, kA)
                    try:
                        tls = []
                        DN, bla = _winreg.QueryValueEx(oK1, 'DisplayName')
                        DV, bla = _winreg.QueryValueEx(oK1, 'DisplayVersion')
                        _winreg.CloseKey(oK1)
                        ln.append(DN)
                        lv.append(DV)
                    except:
                        pass
                    i += 1
                except:
                    break
            _winreg.CloseKey(oK)
            return zip(ln, lv)
        except:
            return zip(ln, lv)

    rK = _winreg.HKEY_LOCAL_MACHINE
    sK = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
    openedKey = _winreg.OpenKey(rK, sK, 0, _winreg.KEY_READ)
    arch, bla = _winreg.QueryValueEx(openedKey, 'PROCESSOR_ARCHITECTURE')
    arch = str(arch)
    _winreg.CloseKey(openedKey)

    if arch == 'AMD64':
        fList = DNDS(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_WOW64_32KEY | _winreg.KEY_READ)
        fList.extend(DNDS(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_WOW64_64KEY | _winreg.KEY_READ))
        fList.extend(DNDS(_winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_WOW64_32KEY | _winreg.KEY_READ))
        fList.extend(DNDS(_winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_WOW64_64KEY | _winreg.KEY_READ))
    else:
        fList = DNDS(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_READ)
        fList.extend(DNDS(_winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', _winreg.KEY_READ))
    fList = set(fList)

    lr = []
    rs = 0
    for i in fList:
        a, b = i
        if AppName in a.lower():
            lr.append('success: {} is installed'.format(a))
            lr.append('{:<25}{:5}'.format(a, b))
            rs += 1
        else:
            rs += 0
    if rs:
        return True
    return False

k=CheckApp('COMODO Client - Security')
print k
if k:
    if sendemail==1:
        def emailreport(emailto,emailfrom,fileToSend,password,smtpserver,port):
            import smtplib
            import mimetypes
            from email.mime.multipart import MIMEMultipart
            from email import encoders
            from email.message import Message
            from email.mime.audio import MIMEAudio
            from email.mime.base import MIMEBase
            from email.mime.image import MIMEImage
            from email.mime.text import MIMEText
            import os    
            msg = MIMEMultipart()
            msg["From"] = emailfrom
            msg["To"] = ",".join(emailto)
            msg["Subject"] = "Comodo Antivirus log reports in CSV"
            msg.preamble = "Comodo Antivirus log Reports in CSV"
            with open(fileToSend) as fp:
                record = MIMEBase('application', 'octet-stream')
                record.set_payload(fp.read())
                encoders.encode_base64(record)
                record.add_header('Content-Disposition', 'attachment',
                filename=os.path.basename(fileToSend))
                msg.attach(record)
            try:
                server = smtplib.SMTP(smtpserver,port)
                server.ehlo()
                server.starttls()
                server.login(emailfrom, password)
                server.sendmail(emailfrom, emailto, msg.as_string())
                server.quit()
                print("Email sent successfully")
            except Exception as E:
                print (E)


    qurantined='SELECT Path,CommonInfoUserName FROM AvEvents where Action=1'
    lqurantined='Select count(*) FROM AvEvents where Action=1'
    lremoved='Select count(*) FROM AvEvents where Action=2'
    ldetected='Select count(*) FROM AvEvents where Action=4'
    removed='SELECT Path,CommonInfoUserName FROM AvEvents where Action=2'
    detected='SELECT Path,CommonInfoUserName FROM AvEvents where Action=4'
    virtual='SELECT Path,CommonInfoUserName FROM SbEvents  where Action=1'
    lvirtual='Select count(*) FROM SbEvents  where Action=1'
    blocked='SELECT Path,CommonInfoUserName FROM SbEvents  where Action=2'
    lblocked='Select count(*) FROM SbEvents  where Action=2'
    ignored='SELECt Path,CommonInfoUserName FROM SbEvents  where Action=3'
    lignored='Select count(*) FROM SbEvents  where Action=3'

    connect = sqlite3.connect(os.environ['PROGRAMDATA']+r"\Comodo\Firewall Pro\cislogs.sdb")
    operation = connect.cursor()
    fileToSend = os.environ['TEMP']+r'\ComodoAntiviruslogs.csv'

    if sendemail==1:
        import csv
        with open(fileToSend, 'w') as csvfile:
            spamwriter= csv.writer(csvfile, delimiter=' ',quotechar=' ', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow("Qurantine History")    
            for row in operation.execute(lqurantined):
                out=tuple(row)
            if out[0]==0:
                csvfile.write('No Such History Data Available') 
                csvfile.write('\n')
                csvfile.write("\n")
            else:
                spamwriter.writerow("Path,Username")
                for row in  operation.execute(qurantined):    
                    csvfile.write(str(row))
                    csvfile.write('\n')
                    csvfile.write("\n")            
            spamwriter= csv.writer(csvfile, delimiter=' ',quotechar=' ', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow("Threats removed")
            for row in operation.execute(lremoved):
                out=tuple(row)
            if out[0]==0:
                csvfile.write('No Such History Data Available') 
                csvfile.write('\n')
                csvfile.write("\n")
            else:
                spamwriter.writerow("Path,Username")
                for row in  operation.execute(removed):    
                    csvfile.write(str(row))
                    csvfile.write('\n')
                    csvfile.write("\n")
            spamwriter= csv.writer(csvfile, delimiter=' ',quotechar=' ', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow("Threats Detected")
            for row in operation.execute(ldetected):
                out=tuple(row)
            if out[0]==0:
                csvfile.write('No Such History Data Available') 
                csvfile.write('\n')
                csvfile.write("\n")
            else:
                spamwriter.writerow("Path,Username")
                for row in  operation.execute(detected):    
                    csvfile.write(str(row))
                    csvfile.write('\n')
                    csvfile.write("\n")
            spamwriter= csv.writer(csvfile, delimiter=' ',quotechar=' ', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow("Containment History")
            spamwriter.writerow("Run Virtually")
            for row in operation.execute(lvirtual):
                out=tuple(row)
            if out[0]==0:
                csvfile.write('No Such History Data Available') 
                csvfile.write('\n')
                csvfile.write("\n")
            else:
                spamwriter.writerow("Path,Username")
                for row in  operation.execute(virtual):    
                    csvfile.write(str(row))
                    csvfile.write('\n')
                    csvfile.write("\n")
            spamwriter= csv.writer(csvfile, delimiter=' ',quotechar=' ', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow("Blocked applications by containment ")
            for row in operation.execute(lblocked):
                out=tuple(row)
            if out[0]==0:
                csvfile.write('No Such History Data Available') 
                csvfile.write('\n')        
                csvfile.write("\n")
            else:
                spamwriter.writerow("Path,Username")
                for row in  operation.execute(blocked):    
                    csvfile.write(str(row))
                    csvfile.write('\n')
                    csvfile.write("\n")
            spamwriter= csv.writer(csvfile, delimiter=' ',quotechar=' ', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow("Applications ignored by containment (Run Unrestriced) ")
            for row in operation.execute(lignored):
                out=tuple(row)
            if out[0]==0:
                csvfile.write('No Such History Data Available') 
                csvfile.write('\n')
                csvfile.write("\n")
            else:
                spamwriter.writerow("Path,Username")
                for row in  operation.execute(ignored):    
                    csvfile.write(str(row))
                    csvfile.write('\n')
                    csvfile.write("\n")
        csvfile.close()
        emailreport(emailto,emailfrom,fileToSend,password,smtpserver,port)

    if sendemail==0:       
        print("Qurantine History")    
        for row in operation.execute(lqurantined):
            out=tuple(row)
        if out[0]==0:
            print ('No Such History Data Available') 
            print ('\n')        
        else:        
            for row in  operation.execute(qurantined):    
                print(str(row))            
        print("Threats removed")
        for row in operation.execute(lremoved):
            out=tuple(row)
        if out[0]==0:
            print('No Such History Data Available')         
        else:
            print("Path,Username")
            for row in  operation.execute(removed):    
                print(str(row))            
        print("Threats Detected")
        for row in operation.execute(ldetected):
            out=tuple(row)
        if out[0]==0:
            print('No Such History Data Available') 
            print('\n')        
        else:
            print("Path,Username")
            for row in  operation.execute(detected):    
                print(str(row))            
        print("Containment History")
        print ("Run Virtually")
        for row in operation.execute(lvirtual):
            out=tuple(row)
        if out[0]==0:
            print('No Such History Data Available') 
            print('\n')        
        else:
            print("Path,Username")
            for row in  operation.execute(virtual):    
                print(str(row))            
        print("Blocked applications by containment ")
        for row in operation.execute(lblocked):
            out=tuple(row)
        if out[0]==0:
            print('No Such History Data Available') 
            print('\n')        
      
        else:
            print("Path,Username")
            for row in  operation.execute(blocked):    
                print(str(row))                        
        
        print("Applications ignored by containment (Run Unrestriced) ")
        for row in operation.execute(lignored):
            out=tuple(row)
        if out[0]==0:
            print('No Such History Data Available')     
        else:
            print("Path,Username")
            for row in  operation.execute(ignored):    
                print(str(row))
        
else:
    print "Comodo Client Security is not installed in the Endpoint"




