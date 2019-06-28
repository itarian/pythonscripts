Hi

A roaming device cannot connect to internal hosts when inside the office network hence 'Host File Configuration' need to be configured additionally in the network interface.

Refer below script to enroll Comodo Dome shield roaming agent using ITSM script procedure,

The script will do following functions one by one in order viz

1. Download cDomeAgent (Roaming agent) from provided URL(Get the download link from Download agent > "ITSM Agent Download link")
2. install it in the Windows devices
3. reboot the device

Note - No security rules will be applied to the roaming device(s) by default. You can create and apply device specific policies according to your requirements.

Please refer https://help.comodo.com/topic-434-1-840-10766-apply-policies-to-networks,-roaming-and-mobile-devices.html

For advice on how to configure and deploy security policies to roaming devices.