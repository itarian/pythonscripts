The script is to detect all installed or active anti-viruses from an endpoint

Note:

The Windows command "WMIC /Node:localhost /Namespace:\\root\SecurityCenter2 Path AntiVirusProduct Get displayName /Format:List" is to get the Antivirus Tool, Windows Defender and Third Party Anti Viruses.

This script can be run by System user
