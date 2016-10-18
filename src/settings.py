import os
import sys

env = os.uname()[1]
test_env = len(sys.argv) > 1 and sys.argv[1] == "test"

if test_env:
    from config.test import *
elif env == "equipo-vagrant":
    from config.vagrant import *
    print "using vagrant"
#else:  
    #production env tbd