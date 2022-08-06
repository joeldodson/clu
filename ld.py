#!/usr/bin/env python

"""
use functions from l.py to print only the directories in currenct directory 
"""

from l import getDirectoryInfo, printDirectoryInfo

printDirectoryInfo(getDirectoryInfo('.',0), dirsOnly=True)


# end of file 