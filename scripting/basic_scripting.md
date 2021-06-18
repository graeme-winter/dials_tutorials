# Basic Scripting

## Introduction

The [multi-crystal tutorial](../br-lyso-multi/multicrystal.md) made use of some shell scripting to process data sets before looking at `dials` tools for combining and scaling the data. To a seasoned UNIX hack these scripts are straightforward, but less obvious to folks who have had better things to do that learn UNIX scripting. The aim of _this_ tutorial is to introduce the basic elements that are necessary to get the work of the other tutorial done, for your set-up where the data may be arranged differently.

## The Shell

On a Mac, you would use `Terminal.app` - on Linux open a terminal, and on Windows I recommend installing [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10) to give a UNIX-like environment - you would start e.g. an Ubuntu terminal.

The "shell" is the program you are running _within_ your terminal application - often this is `bash` - some more seasoned crystallographers prefer `csh` and my MacBook keeps nagging me to change my shell to `zsh`. These all work approximately the same way though `csh` and friends have a slightly different syntax, so here I will focus on `bash`.

## Scripts

A shell script is a text file with commands for the shell - that is all. If you can run it in a terminal, you can run from a script and vice versa. The script is useful though as you can edit it and run again, so for things where you may want to run multiple times or do the same complicated thing again in future it is very useful. Any command from the shell will work in a script e.g. `mkdir`, `cd` etc. as well as `dials.import` or whatever.

A key part to writing scripts is to find an editor you like - I personally use variations on a theme of `emacs` but `nano`, `kate` and many others exist. Find one you like 🙂 I'm not telling you what will work for you.

## Basic Scripts

If you have a script which contains:

```
echo "Hello, I am a script running in ${SHELL}"
```

and run it with e.g. `bash script.sh` this will print something like

```
Hello, I am a script running in /bin/bash
```

What happened here is it took the value of `SHELL` from "the environment" (a load of variables which live within the shell) and prints the value in place of `${SHELL}` - strictly speaking the `{}` are optional, but they are useful if you want to _add_ stuff to what is printed, so there is no empty space around `SHELL`. You can see what is in the environment with `env` which will usually print a whole lot of UNIX nonsense. One _very_ useful thing is `${PWD}` which is the current directory:

```
Grey-Area well_139_subset :) $ echo $PWD
/Volumes/Blue2/Data/vmxi-ab5081/well_139_subset
```

We will come to rely on this later. 
