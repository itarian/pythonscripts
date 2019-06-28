This script is used to install fonts from one one machine to another using network share.

Note:

This script should be Run as System User.
Please edit parameters such as share_user, share_pass, Fontpath to install fonts according to your requirement.
"share_user" - This is said to be the network share username for access
"share_pass" -This is said to be the network share password for access
"Fontpath" - The path of the network folder where font files were kept
For Example:

Fontpath=r'\\AKITA-PC\latestfonts'
share_user="Akita"
share_pass="comodo"

It should be Run as System User.