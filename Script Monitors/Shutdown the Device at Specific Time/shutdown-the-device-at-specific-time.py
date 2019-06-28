from subprocess import PIPE, Popen

time = 2000
# Run command in CMD
def DoCommandInCMD(command, output=False):
    print("Running command in the CMD: " + str(command))
    objt = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = objt.communicate()
    ret = objt.returncode
    if not out:
        return ret
    else:
        return '%s\n%s' % (out, err)

DoCommandInCMD(r"shutdown -s -t " + str(time))
