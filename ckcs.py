#!/usr/bin/env python

import os
import typer 
import json 
from typing import List 
from typing import Dict 
import cluUtils 


## 
# I didn't want to make shortcuts global 
# but could not figure out another wayto have access to the list in the whens command
# I was looking for a way to pass it via a context 
# but was spending way to much time on it.
# So it's global for now.  consider yourself warned.
## 
shortcuts = []

app = typer.Typer()


#######
def findUniqueWhens() -> List:
    """
    return a dict with "when" property from shortcut as key, 
    and number of times that when string appears in the list of shortcuts  
    The number of items in the dict indicates how many unique when properties there are,
    and the values indicate how often that when clause occured. 
    """
    uniqueWhens = {'global': 0}
    for sc in shortcuts:
        when = sc.get("when", None)
        if not when:
            uniqueWhens["global"] += 1
            ## print(f'nowhen == {uniqueWhens["nowhen"]}')
        elif uniqueWhens.get(when, None) != None:
            uniqueWhens[when] += 1             
            ## print(f'{when} == {uniqueWhens[when]}')
        else: 
            uniqueWhens[when] = 1
            ## print(f'new string: {when} == {uniqueWhens[when]}')
    return uniqueWhens  


#######
# hold on to something, this gets a little confusing...
# whensPerAppearance is a dict where the key is the number of time a when appears in a shortcut
# Different whens can appear in the same number of shortcuts though, 
#so the value in the dict is a list of when strings.
# So, so, as we're printing the items in the dict, we have to account for all items in the list of the value, thus all the nesting. 
##
def printWhensPerAppearance(whensPerAppearance: Dict, topN: int = 7) -> None: 
    print(f'The top {topN} whens based on how often each occurs in a shortcut')
    for appearances, whenList in whensPerAppearance.items():
        if (topN := topN - 1) >= 0:
            for when in whenList:
                print(f'When <{when}> appears in {appearances} shortcuts') 
        else: break


#######
# I wanted to have the commands in a package for ckcs commands
# with each command in its own file 
# but I couldn't find a good way to pass around the shortcuts list
# and I didn't want to have to recreate it for each command 
# so ckcs is one big a** file
##
@app.command()
def whens(
        unique: bool = typer.Option(False, "-u", "--unique")
) -> None: 
    """
    the when command is used to analyze the when field of the keyboard shortcuts.
    The when field represents when a shortcut can be used, the state of vscode in which a shortcut is meaningful.
    I was curious how many different states there could be 
    and maybe printing the shortcuts based on groupings of states would be useful.
    """
    print('If not now, WHEN!!??') 
    if unique:
        uniqueWhens = findUniqueWhens()
        whensPerAppearance = cluUtils.orderDictByIntValues(uniqueWhens) 
        printWhensPerAppearance(whensPerAppearance)


#######
def filterShortcuts(searchStr: str) -> List: 
    searchStr = searchStr.lower()
    print(f'searching commands for the string <{searchStr}>')
    kbsFound = []
    for sc in shortcuts:
        if sc["command"].lower().find(searchStr) >= 0:
            kbsFound.append(sc) 
    print(f'Found {len(kbsFound)} shortcuts')
    return kbsFound 


#######
def printShortcuts(pageSize: int, when: bool = False):
    count = 0
    for sc in shortcuts:
        sout = f'{sc["command"]} : {sc["key"]}'
        if when and sc.get("when"): 
            sout += f' : when? {sc["when"]}'
        print(sout)
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
# callback makes 'main' the default command to run if no commands are given 
##
@app.callback(invoke_without_command=True)
def main(ctx: typer.Context,
        kbsFile: str = typer.Option('./data/defaultkeybindings.json', "--kbsFile", "-f"),
        searchStr: str = typer.Option(None, "--searchStr", "-s"),
        countOnly: bool = typer.Option(False, "--count", "-c"),
        when: bool = typer.Option(False, "--when", "-w"),
        pageSize: int = typer.Option(5, "--pageSize", "-p")
) -> None:
    global shortcuts  
    shortcuts = getShortcutsFromFile(kbsFile)
    if not ctx.invoked_subcommand:
        if countOnly: 
            print(f'File {kbsFile} contains {len(shortcuts)} shortcuts')
            raise typer.Exit()
        elif searchStr: 
            shortcuts = filterShortcuts(searchStr)
        printShortcuts(pageSize, when)


if __name__ == "__main__":
    app()
    ## typer.run(main)

## end of file 