This is the monitoring which is used to Hit the alert for removing the ESM, CCS, and install the CCS. This will help us to migrate ESM to ITSM


Refer the below wiki for custom monitoring procedure:
https://wiki.comodo.com/frontend/web/topic/how-to-use-custom-script-procedure-monitoring

Do the following steps:

1.Create a New windows profile in ITSM
2. Add the profile section as Monitoring
3. Select the Run below procedure on the auto-remediation and find the uninstall procedure for CESM or CES or CAVS and select it.

please use this link for the remediation procedure:
https://scripts.comodo.com/frontend/web/topic/automatic-remove-of-esm-agent-ces-and-cavs-from-device-and-installation-of-ccs


4.select the condition Tab and select the add condition and select the custom script to paste the above-mentioned script.

Refer the following wiki for the custom monitoring procedure
https://wiki.comodo.com/frontend/web/topic/how-to-use-custom-script-procedure-monitoring