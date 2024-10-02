#!/usr/bin/env python
""" clu/which.py
build my own little which program for PowerShell 
"""

import shutil
import sys 

def main():
    if len(sys.argv) < 2: 
        print("missing command name")
        return 
    if len(sys.argv) > 2: print(f"ignoreing arguments: {' '.join(sys.argv[2:])}")
    print(f"path for command: {sys.argv[1]}: \n {shutil.which(sys.argv[1])}")



if __name__ == "__main__":
    main() 
