Please refer the script, to generate an alert when the used restore point space of your system meets the certain threshold space and also if there is no restore point is present in your system then it automatically it will Creates Restore Point. 
For example, if the a restore point is 2.00 GB, then we can put the threshold condition as 1.5 GB, if the conditions matched then it will generate an alert.



NOTE: Here, in the below script "Max_rp_size=1.0" , Max_rp_size is the threshold restore point space (size) , value is 1.0=GB, If you want to put restore size as 2GB just replace the value as 2.0 (or) otherwise if you want to put the Threshold restore space(size) as 800MB just give as 0.80.

Please run the script as System Administrator.
Please, Refer the JSON file for execution.

Please refer the wiki guide for how to use the custom monitoring scripts:

 https://forum.mspconsortium.com/forum/products/other-comodo-products/comodo-device-management/wiki-faq-how-to/11486-how-to-use-custom-script-procedure-monitoring