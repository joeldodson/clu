#!/usr/bin/env python

"""
a tool to investigate the directory structure, 
including understanding the variety of its contents.

a dictionary is created containing info of the directory tree
starting from the given root directory. 

The dict has the form:

{
    name: str ## absolute path name of the directory described by this dict 
    files: List[str]  ## files in the directory 
    extensions: Dict[str: int]  ## tracking count of types of each file in the directory 
    subdirs: Dict[str: {}]  ## directories within current directory represented by dict of the same form 
    symlinks: List[str]  ## symbolic links, don't follow, just track that they exist 
}
"""
import os 
import json 

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("path", nargs="?", default=".")
parser.add_argument("-d", "--depth", type=int, action="store", default=0)
args = parser.parse_args()

#######
def indent(level: int) -> str:
    return '   ' * level 


#######
def printDirs(dir: dict, level: int = 0):
    print(f'{indent(level)}DIRECTORIES - {len(dir["dirs"].keys())}:')
    for d in dir["dirs"].keys():
        dirpath, dirname = os.path.split(d)
        print(f'{indent(level)}{dirname}') 

#######
def printFiles(dir: dict, level: int = 0):
    print(f'{indent(level)}FILES - {len(dir["files"])}:') 
    for f in dir["files"]:
        print(f'{indent(level)}{f}') 

#######
def printDirectoryInfo(dir: dict, level: int = 0, dirsOnly = False):
    if level > 0: # tired of hearing the directory I'm currently in, only print it if into sup dirs  
        print(f'{indent(level)}DIRECTORY: {dir["name"]}') 

    printDirs(dir, level)
    printFiles(dir, level)

    ## go through dirs again to print the contents of each, if any exists 
    for d in dir["dirs"].keys():
        if dir["dirs"][d]:
            printDirectoryInfo(dir["dirs"][d], level + 1)
    if len(dir["symlinks"]) > 0:
        print(f'{indent(level)}SYMBOLIC LINKS -- {len(dir["symlinks"])}:') 
        for s in dir["symlinks"]:
            print(f'{indent(level)}{s}') 


#######
def getDirectoryInfo(dirname: str, depth: int) -> dict:
    """
    start with an empty dict and fill it with information describing 
    the contents of the current directory as defined at the top of this file.

    if depth is greater than 0, 
    for each sub directory in this directory,
    recursively get itsdirectory information.
    If depth is 0, simply return the dict describing this directory.
    """
    curdir = { 
        'files': [], 
        'extensions': {'noext':0}, 
        'dirs': {},
        'symlinks': []
    }

    curdir['name'] = os.path.abspath(dirname)
    with os.scandir(dirname) as iter:
        for f in iter: 
            if f.is_file(): 
                curdir['files'].append(f.name)
                _, ext = os.path.splitext(f.name)
                ext = ext if (len(ext) > 0) else 'noext'
                if curdir['extensions'].get(ext): curdir['extensions'][ext] += 1
                else: curdir['extensions'][ext]  =1
            elif f.is_dir(): 
                curdir['dirs'][f.path] = None
            elif f.is_symlink(): 
                curdir['symlinks'].append(f.name)

    if depth > 0:
        for dir in curdir['dirs'].keys():
            curdir['dirs'][dir] = getDirectoryInfo(dir, depth - 1)

    return curdir 


#######
def main():
    """
    inspect the file system 
    """
    dirinfo = None 
    if os.path.isdir(args.path):
        dirinfo = getDirectoryInfo(args.path, args.depth)
        printDirectoryInfo(dirinfo)
    else:
        print(f'oh no, you buggered that one. {args.path} is not a directory.')


if __name__ == "__main__":
    main()


""" 
# played with this in repl
print('Walk This Way ...') 
for (dirpath, dirnames, filenames) in os.walk('.'):
    print(f'Directory: {dirpath}')
"""


## end of file 