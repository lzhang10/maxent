#!/usr/bin/env python

import os
import sys
import string
from glob import glob

try:
    os.spawnvp
    def runcmd(*cmd):
	return os.spawnvp(os.P_WAIT,cmd[0],cmd)
except AttributeError:
    def runcmd(*cmd):
	return os.system(string.join(cmd," "))
    
failed = []
success = []

for test in glob("test_*"):
    if os.access(test, os.X_OK) == 0: continue
    print "**",test
    result = os.system('./' + test)
    if os.WIFEXITED(result):
	status = os.WEXITSTATUS(result)
    else:
	status = 1
    if status:
	print "** FAIL: ",test
	failed.append(test)
    else:
        success.append(test)
	
print ""
print "SUMMARY:"
print "Total %d scripts run, %d success, %d failed" % ((len(success) + \
        len(failed)), len(success), len(failed))
if failed:
    print "FAILED: " + ", ".join(failed)
    sys.exit(1)
else:
    print "No test scripts crashed."
