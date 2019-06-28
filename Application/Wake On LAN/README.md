What is Wake on LAN??

Wake-on-LAN (WoL) is an Ethernet or token ring computer networking standard that allows a computer to be turned on or awakened by a network message.The message is usually sent to the target computer by a program executed on a device connected to the same local area network, such as a smartphone. It is also possible to initiate the message from another network by using subnet directed broadcasts or a WOL gateway service. Equivalent terms include wake on WAN, remote wake-up, power on by LAN, power up by LAN, resume by LAN, resume on LAN and wake up on LAN. If the computer being awakened is communicating via Wi-Fi, a supplementary standard called Wake on Wireless LAN (WoWLAN) must be employed.

For more information on Wake on LAN about the sofware and Hardware requirements please refer this link https://en.wikipedia.org/wiki/Wake-on-LAN

NOTE:

Run this Script in any of the system connected to your network from an Python Idle Installed on it.

Please follow the below steps for proper running of the script.

Step 1: Note all MAC addresses of the computers where you want to use the script.

Step 2: Install Python 2.7 on a computer (within the LAN) where you plan to run the script. This means that this PC needs to be always on (not on sleep or hibernate mode).
https://www.python.org/ftp/python/2.7.14/python-2.7.14.msi

Step 3: Copy and paste the script ( https://scripts.comodo.com/frontend/web/topic/wake-on-lan ) in IDLE. In the script, make sure to declare the MAC address(es) of the computer(s) you want to wake up.
Example: list1=["EC-B1-A9-2F-1A-3Z","54-0F-CF-34-9z-8A"]

Feel free to review IDLE setups and how to use it from online sources.
https://www.youtube.com/results?search_query=python+2.7+IDLE

Step 4: Run the script as needed.

 

Please Refer this script if you want to turn on your Computer from Sleep Mode.
