This Script will list installed or Available (uninstalled) updates. By setting value as 0 or 1, it will install or uninstall KB which is provided at top of the Script.

Refer the wiki to run the procedure with parameters
https://wiki.comodo.com/frontend/web/topic/how-to-create-and-run-procedures-with-parameters

For Example:

KB="KB3110329"   # Enter the KB value of patch which you want to install or Uninstall.
value=1   # Set value to " 0 " to install and " 1 " to uninstall

The above parameters need to be updated for installing or uninstalling the windows update.

Note: Please edit the following parameters in the script

### PARAMETERS TO BE EDITED UNDER PARAMETERS TAB ###

1.KB_value:
   TYPE: String
    ITSM LABEL: Any name
   Default value: "Provide the KB value which you need to install or uninstall"

2.Set_value_0_to_install_1_for_uninstall:
   TYPE: integer
    ITSM LABEL: Any name
    Default value: "Provide 1 for uninstall, 0 for install"

Run as a System User.
