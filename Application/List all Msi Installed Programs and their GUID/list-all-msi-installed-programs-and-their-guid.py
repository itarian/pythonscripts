import os
cmd=r"wmic product get name,identifyingnumber"
print os.popen(cmd).read()

