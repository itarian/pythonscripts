Toaddress =itsm.getParameter("Enter_to_Address") # Enter the email id where you want to send screenshot. Type as STRING. 

import time;
import os;
import re;
import ctypes
file='C:\\Windows\Temp\Take-ScreenShot.ps1';
Toaddress='"'+Toaddress+'"'

    
input="""
#############################################################################
# Capturing a screenshot
#############################################################################
$timer = (Get-Date -Format yyy-mm-dd-hhmm)
$File = "C:\ProgramData\$env:computername-$env:username-$timer.bmp"
Add-Type -AssemblyName System.Windows.Forms
Add-type -AssemblyName System.Drawing
# Gather Screen resolution information
$Screen = [System.Windows.Forms.SystemInformation]::VirtualScreen
$Width = $Screen.Width
$Height = $Screen.Height
$Left = $Screen.Left
$Top = $Screen.Top
# Create bitmap using the top-left and bottom-right bounds
$bitmap = New-Object System.Drawing.Bitmap $Width, $Height
# Create Graphics object
$graphic = [System.Drawing.Graphics]::FromImage($bitmap)
# Capture screen
$graphic.CopyFromScreen($Left, $Top, 0, 0, $bitmap.Size)
# Save to file
$bitmap.Save($File) 
Write-Output "Screenshot saved to:"
Write-Output $File
$fileType = $file.Substring(($file.IndexOf('.'))+1) #get image file extension

function do_mail ($myhtml) {

$SMTPServer = "smtp.gmail.com"
$SMTPPort = "587"
$Username = "coneoperations@gmail.com"
$Password = "Comodo@123"
$time = Get-Date
$to = %s
$subject = "Screenshot of $env:computername on $time"
$body = @"
<html>
<body>
<img src="cid:$env:computername-$env:username-$timer.jpg">
</body>
</html>
"@
$attachment = New-Object System.Net.Mail.Attachment -ArgumentList $filepath
$attachment.ContentDisposition.Inline = $True
$attachment.ContentDisposition.DispositionType = "Inline"
$fileType = $filepath.Substring(($filepath.IndexOf('.'))+1) #get image file extension
$attachment.ContentType.MediaType = "image/$fileType" #set mediaType based on $file extension
$attachment.ContentId = '$env:computername-$env:username-$timer.jpg'


$message = New-Object System.Net.Mail.MailMessage
$message.IsBodyHTML = $true
$message.subject = $subject
$message.body = $body
$message.to.add($to)
#$message.cc.add($cc)
$message.from = $username
$message.attachments.add($attachment)

$smtp = New-Object System.Net.Mail.SmtpClient($SMTPServer, $SMTPPort);
$smtp.EnableSSL = $true
$smtp.Credentials = New-Object System.Net.NetworkCredential($Username, $Password);
$smtp.send($message)
$attachment.Dispose();
$message.Dispose();
write-host "Email sent to $to"
#Remove-Item $filepath
} 

# Try uncommenting the following line if you receive errors about a missing assembly
[void][System.Reflection.Assembly]::LoadWithPartialName("System.Drawing")
function ConvertTo-Jpg
{
  [cmdletbinding()]
  param([Parameter(Mandatory=$true, ValueFromPipeline = $true)] $Path)

  process{
    $qualityEncoder = [System.Drawing.Imaging.Encoder]::Quality
    $encoderParams = New-Object System.Drawing.Imaging.EncoderParameters(1)

    # Set JPEG quality level here: 0 - 100 (inclusive bounds)
    $encoderParams.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter($qualityEncoder, 50)
    $jpegCodecInfo = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | where {$_.MimeType -eq 'image/jpeg'}

    if ($Path -is [string]) {
      $Path = get-childitem $Path
    }

    $Path | foreach {
      $image = [System.Drawing.Image]::FromFile($($_.FullName))
      $filePath =  "{0}\{1}.jpg" -f $($_.DirectoryName), $($_.BaseName)
      $image.Save($filePath, $jpegCodecInfo, $encoderParams)
      $image.Dispose()
      Write-host "File converted to JPG"
      write-host $filepath

    }

    do_mail $myhtml

  }

}

#Use function:
# cd to directory with png files
#cd c:\users\$env:username

#Run ConvertTo-Jpg function and send email
Get-ChildItem $file | ConvertTo-Jpg
#Remove BMP
Remove-Item $file
"""%(Toaddress)
fobj=open(file,"w");
fobj.write(input);
fobj.close();

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert  = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)


with disable_file_system_redirection():
    out=os.popen(r'powershell.exe -executionpolicy bypass -file C:\Windows\Temp\Take-ScreenShot.ps1').read();
    print out

