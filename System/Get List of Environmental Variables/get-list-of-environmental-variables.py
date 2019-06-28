import os
for param in os.environ.keys():
    print "%s=%s"%(param, os.environ[param])