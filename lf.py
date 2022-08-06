#!/usr/bin/env python

"""
use functions from l.py to print only the files in currenct directory 
"""

from l import getDirectoryInfo, printFiles

printFiles(getDirectoryInfo('.',0))


# end of file 