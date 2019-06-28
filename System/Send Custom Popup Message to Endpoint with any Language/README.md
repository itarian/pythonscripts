We recommend this script to send a custom pop-up message to the endpoint user (who is currently logged in)

Give following parameters

message=u"హాయ్ ఎలా ఉన్నారు" ## Does not support multi-line message.
title=u"Message from: Administrator"

Note:
Please follow the below instruction for the script,
1. Please Run the Script as Logged in User

2.you have to configure the parameters before running the script.

The script execution will complete only when the endpoint user responds to the custom message, so the execution log will only be displayed after the endpoint user responds to the message box.

You can modify the title of the message box on the variable - title="your title"
You can modify the message of the message box on the variable - message="your message"