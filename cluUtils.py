
import typer
from typing import Dict 

def orderDictByIntValues(original: Dict) -> Dict:
    """
    I have a dict with string keys with int values.
    The values indicate the number of times the string (that is the key) appears in a structure.
    And many strings can appear the same number of timesf (values are NOT unique)
    I want to look at the strings in descending order based on those values.
    This util is a brute force way to order a dict such that the first element in the dict
    is the most frequent string and so on. 
    The ordering of strings that appear in the other structure the same number of times doesn't matter.
    """
    typer.echo(f'original dict has {len(original.keys())} items')
    resultDict = {}
    ##
    # first find all the unique values 
    vals = set()
    for v in original.values(): vals.add(int(v))
    vals = list(vals)
    vals.sort(reverse=True)
    ## typer.echo(f'there are {len(vals)} : {vals}') 
    ##
    # we have a list of the unique values in descending order.
    # now find the keys in original with values matching entries in the list 
    # and add them to the list in resultDict matching the value in as key 
    for uv in vals:
        ## typer.echo(f'looking for strings that appeared {uv} times')
        listOfStringsPerValue = [s for s in original.keys() if original[s] == uv] 
        resultDict[uv] = listOfStringsPerValue 
        typer.echo(f'value {uv} has {len(listOfStringsPerValue)} strings')
    return resultDict 



