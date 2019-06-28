Refer this procedure to automate the patch management agent installation process. This will also add windows firewall rule to allow patch management services.

Input parameters with example 
command= 'msiexec /i patch_agent.msi /qn AGENTUSERNAME=agent_57dfc372d8e7187e80813def PASSWORD=9251f8493e283f577480f1c7ad9c09f9 CUSTOMER=57dfc372d8e7187e80813def IPADDRESS=staging.patch.comodo.com'