# clu
Python Based Command Line Utilities 

I needed to start working in Windows for real (not using WSL2/Ubuntu on Windows) and started using PowerShell.
The first thing I missed from bash was 'ls -1'.  
ls worked okay but spit out a bunch of information I didn't need, and didn't want to hear about from the screen reader.

So, I could learn to use PowerShell, use git-bash (which I find a bit awkward on the Windows filesystem and seems to have some accessibility issues) or I could write some Python tools to run from the command line.
Writing Python tools sounded a lot more fun and applicable to other areas of development.
So here we are.

## Update 2024-10-04

Quite a long time has passed since starting this clu repo.
And, surprise, I've changed my mind in a few areas.

First, typer.
Sure, it's a cool utility, but it's slower than argparse, and has to be pip installed.
I've removed it from the utils I use most (e.g.,'l', the 'ls' alternative).
And I'm not using it in any new utils (e.g., dodona).
Its still in ckcs mainly because I've mostly abandon ckcs.

## l (with ld and lf being shortcuts) 
This is my answer to 'ls -1'.
I thought it would not only replace 'ls' but also be kind of a 'tree' utility.
I'm not sure I like the 'tree' utility part of it yet, but with the default being to look only in the current (or specified) directory, I think ifs is a decent version of 'ls -1' 

Now l has some command line options to show file sizes and dates.
run: "l --help" for details.

## dodona

aThis is a utility to chat with ChatGPT.
You need your own OpenAI account and API access token.
the help shows the URL with directions to get an API token.
Run: "dodona --help" for details.

## ckcs (Ctrl-k Ctrl-s) - abandon, or at least on the backburner

the name comes from how to view the shortcut keys in Visual Studio Code.
the json file in the data directory comes from looking at the default keyboard shortcuts json file in VS Code.
In that file, I ctrl-a, ctrl-c then ctrl-v it into the data file.

I find the default way of looking through the list of shortcut keys for VS Code to not be great using a screen reader.
This utility is a way to look through the shortcuts using the command line.
It's a work in progress and I'm not sure what that progress will be yet.

I'm a bit hung up on the context for each shortcut.
The context is represented in a "when" property in the shortcut dictionary.
I started analyzing the when fields to find all the unique ones and how often they appear.
I'm not sure what I want to do with that though.
Using that information to group and print the shortcuts seems like a natural application.  
Though given the "when" properties are boolean expressions and some are subsets of others, I'm not sure grouping by whens is straight forward.

I'm going to back burner this for a bit.

One future Item I would like to do is use jijna2 to create HTML pages to display the shortcuts in tables making it easier to vew them with a screen reader.

###### end of README 