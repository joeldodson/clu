#!/usr/bin/env python

"""
use functions from l.py to print only the directories in currenct directory 
"""

from l import getDirectoryInfo, printDirs

printDirs(getDirectoryInfo('.',0))


# end of file 