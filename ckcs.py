#!/usr/bin/env python

import os
import typer 
import json 
from typing import List 

app = typer.Typer()

#######
def filterShortcuts(kbs: List, searchStr: str) -> List: 
    searchStr = searchStr.lower()
    typer.echo(f'searching commands for the string <{searchStr}>')
    kbsFound = []
    for sc in kbs:
        if sc["command"].lower().find(searchStr) >= 0:
            kbsFound.append(sc) 
    typer.echo(f'Found {len(kbsFound)} shortcuts')
    return kbsFound 


#######
def printShortcuts(kbs: List, pageSize: int, when: bool = False):
    count = 0
    for sc in kbs:
        sout = f'{sc["command"]} : {sc["key"]}'
        if when: sout += f' : when? {sc["when"]}'
        typer.echo(sout)
        if (count := count + 1) == pageSize:
            if typer.confirm("Exit?"): raise typer.Exit()
            else: count =0 


#######
# NOTE: I'm assuming this file is not ginormous
# otherwise, it needs to be read in one line at a time.
##
def getShortcutsFromFile(kbsFile: str) -> List:
    jstr = ''
    with open(kbsFile, 'r') as f:
        for line in f.readlines():
            ## ignore any comment lines 
            if not line.lstrip().startswith('//'): jstr += line 

    return json.loads(jstr)


#######
@app.callback(invoke_without_command=True)
def main(
        kbsFile: str = typer.Option('data\\defaultkeybindings.json', "--kbsFile", "-f"),
        searchStr: str = typer.Option(None, "--searchStr", "-s"),
        countOnly: bool = typer.Option(False, "--count", "-c"),
        when: bool = typer.Option(False, "--when", "-w"),
        pageSize: int = typer.Option(5, "--pageSize", "-p")
) -> None:
    shortcuts = getShortcutsFromFile(kbsFile)
    if countOnly: 
        typer.echo(f'File {kbsFile} contains {len(shortcuts)} shortcuts')
        raise typer.Exit()
    elif searchStr: 
        shortcuts = filterShortcuts(shortcuts, searchStr)

    printShortcuts(shortcuts, pageSize, when)


if __name__ == "__main__":
    app()
    ## typer.run(main)

## end of file 