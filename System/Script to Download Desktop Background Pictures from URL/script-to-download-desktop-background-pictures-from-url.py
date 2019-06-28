import os
ps_content=r'''
# script parameters, feel free to change it 
$downloadFolder = "C:\Users\john\Desktop\picture"
$searchFor = "red rose"
$nrOfImages = 20

# create a WebClient instance that will handle Network communications 
$webClient = New-Object System.Net.WebClient

# load System.Web so we can use HttpUtility
Add-Type -AssemblyName System.Web

# URL encode our search query
$searchQuery = [System.Web.HttpUtility]::UrlEncode($searchFor)

$url = "http://www.bing.com/images/search?q=$searchQuery&first=0&count=$nrOfImages&qft=+filterui%3alicense-L2_L3_L4"

# get the HTML from resulting search response
$webpage = $webclient.DownloadString($url)

# use a 'fancy' regular expression to finds Urls terminating with '.jpg' or '.png'
$regex = "[(http(s)?):\/\/(www\.)?a-z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-z0-9@:%_\+.~#?&//=]*)((.jpg(\/)?)|(.png(\/)?)){1}(?!([\w\/]+))"

$listImgUrls = $webpage | Select-String -pattern $regex -Allmatches | ForEach-Object {$_.Matches} | Select-Object $_.Value -Unique

# let's figure out if the folder we will use to store the downloaded images already exists
if((Test-Path $downloadFolder) -eq $false) 
{
  Write-Output "Creating '$downloadFolder'..."

  New-Item -ItemType Directory -Path $downloadFolder | Out-Null
}


foreach($imgUrlString in $listImgUrls) 
{
  [Uri]$imgUri = New-Object System.Uri -ArgumentList $imgUrlString

  # this is a way to extract the image name from the Url
  $imgFile = [System.IO.Path]::GetFileName($imgUri.LocalPath)

  # build the full path to the target download location
  $imgSaveDestination = Join-Path $downloadFolder $imgFile

  Write-Output "Downloading '$imgUrlString' to '$imgSaveDestination'..."

  $webClient.DownloadFile($imgUri, $imgSaveDestination)  
} 
         
'''

def ecmd(command):
    import ctypes
    from subprocess import PIPE, Popen
    
    class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)
    
    with disable_file_system_redirection():
        obj = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = obj.communicate()
    ret=obj.returncode
    if ret==0:
        if out:
            return out.strip()
        else:
            return ret
    else:
        if err:
            return err.strip()
        else:
            return ret

file_name='powershell_file.ps1'
file_path=os.path.join(os.environ['TEMP'], file_name)
with open(file_path, 'wb') as wr:
    wr.write(ps_content)

ecmd('powershell "Set-ExecutionPolicy RemoteSigned"')
print ecmd('powershell "%s"'%file_path)



