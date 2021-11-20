#!/usr/bin/env python

import os
import typer 
import json 
#######
def filterShortcuts(kbs: object, searchStr: str) -> object: 
    pass 


#######
def printShortcuts(kbs: object, pageSize: int, when: bool = False):
    count = 0
    for sc in kbs:
        sout = f'{sc["command"]} : {sc["key"]}'
        if when: sout += f' : when? {sc["when"]}'
        typer.echo(sout)
        if (count := count + 1) == pageSize:
            if typer.confirm("Exit?"): raise typer.Exit()
            else: count =0 


#######
def getShortcutsFromFile(kbsFile: str) -> object:
    jstr = ''
    with open(kbsFile, 'r') as f:
        for line in f.readlines():
            ## ignore any comment lines 
            if not line.lstrip().startswith('//'): jstr += line 

    return json.loads(jstr)


#######
def main(
        kbsFile: str = typer.Option('defaultkeybindings.json', "--kbsFile", "-f"),
        searchStr: str = typer.Option(None, "--searchStr", "-s"),
        countOnly: bool = typer.Option(False, "--count", "-c"),
        when: bool = typer.Option(False, "--when", "-w"),
        pageSize: int = typer.Option(10, "--pageSize", "-p")):
    shortcuts = getShortcutsFromFile(kbsFile)
    if countOnly: 
        typer.echo(f'File {kbsFile} contains {len(shortcuts)} shortcuts')
        raise typer.Exit()
    elif searchStr: typer.echo(f'searching for string: <{searchStr}>')

    printShortcuts(shortcuts, pageSize, when)



if __name__ == "__main__":
    typer.run(main)


