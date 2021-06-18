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

## Loops and Files

The main reason we are wanting to write scripts is to allow us to do the same thing over and over again - which is best helped by _loops_ - either counting:

```
for ((j = 0; j < 10; j++)); do echo "j = ${j}"; done
```

or over words:

```
for word in green eggs ham; do echo ${word}; done
```

These words are just things with no spaces in and most usefully they can be things like _file names_:

```
Grey-Area well_139_subset :) $ for f in *_master.h5; do echo $f; done
image_28395_master.h5
image_28396_master.h5
image_28398_master.h5
image_28401_master.h5
image_28404_master.h5
image_28405_master.h5
image_28408_master.h5
image_28413_master.h5
image_28414_master.h5
image_28418_master.h5
image_28420_master.h5
image_28421_master.h5
image_28424_master.h5
image_28425_master.h5
image_28428_master.h5
image_28429_master.h5
image_28432_master.h5
image_28433_master.h5
```

Here we are asking the shell to "glob" (an ancient UNIX word) all the files which end in `_master.h5` - we can use this in a script to process all the `master.h5` files, say. Normally though you may want to make a directory based on this file name, which may be everything which is not `_master.h5` in the filename (so `image_28395` for the first one) - we can automate this, but that is maybe getting a bit advanced for the basic tutorial so we will touch on this later in string editing.

In the meantime, You can just use e,g.

```
for PREFIX in \
image_28395 image_28396 image_28398 image_28401 image_28404 \
image_28405 image_28408 image_28413 image_28414 image_28418 \
image_28420 image_28421 image_28424 image_28425 image_28428 \
image_28429 image_28432 image_28433; do
  mkdir ${PREFIX}
  cd ${PREFIX}
  dials.import ../${PREFIX}_master.h5
  dials.find_spots imported.expt
  cd -
done
```

This includes two new pieces of magic - line continuation with `\` and `cd -`. `\` allows you to continue a long line on the next line - in the shell it just ignores the "enter" at the end of the line and keeps reading, which is useful for keeping your script tidy. `cd -` just hops back to the _previous_ directory, so wherever you were before `cd ${PREFIX}` happened. We have also _unrolled_ the loop which makes it easier to read what is happening - everything from `do` to `done` will be performed for every `PREFIX` in the list. Finally, the loop variable `PREFIX` was defined in upper case, which is a convention from the prehistory of time but a useful one.

## Variables

The previous section had us looping over filenames, and importing them from the parent directory `../` - but what if they are somewhere else? That is easily handled by defining another variable e.g. `DATA_DIR` which can be different to your processing directory:

```
DATA_DIR=/Volumes/Blue2/Data/vmxi-ab5081/well_139_subset

for PREFIX in \
image_28395 image_28396 image_28398 image_28401 image_28404 \
image_28405 image_28408 image_28413 image_28414 image_28418 \
image_28420 image_28421 image_28424 image_28425 image_28428 \
image_28429 image_28432 image_28433; do
  mkdir ${PREFIX}
  cd ${PREFIX}
  dials.import ${DATA_DIR}/${PREFIX}_master.h5
  dials.find_spots imported.expt
  cd -
done
```

This is starting to allow you to run the processing in a much more tidy manner. When we get to `${DATA_DIR}/${PREFIX}_master.h5` the shell does not care that there are two variables here - all it does is replace them both to give the full path to where the data are.

A more complex example provided by a workshop user had the challenge of working through data from several data sets from visits to different beamlines:

```
/Volumes/Data/GMCA/7_19_2019/MK_2_5/collect/Q5_1_*.cbf
/Volumes/Data/GMCA/7_19_2019/MK_2_5/collect/Q5_1_INV_*.cbf
/Volumes/Data/GMCA/GMCA11_19_2019/MK_10_13/collect/C13_1_1_*.cbf
/Volumes/Data/GMCA/GMCA11_19_2019/MK_10_13/collect/C13_1_*.cbf
/Volumes/Data/GMCA/GMCA11_19_2019/MK_9_11/collect/B11_5_1_*.cbf
/Volumes/Data/GMCA/GMCA11_19_2019/MK_9_11/collect/B11_5_1_1_*.cbf
/Volumes/Data/GMCA/GMCA11_19_2019/MK_9_13/collect/B13_5_1_*.cbf
/Volumes/Data/LSCAT/12_2019/MK_1_1/MK_1_1.001_master.h5
/Volumes/Data/LSCAT/12_2019/MK_1_2/MK_1_2.001_master.h5
/Volumes/Data/LSCAT/12_2019/MK_1_8/MK_1_8.001_master.h5
/Volumes/Data/LSCAT/12_2019/MK_1_9/MK_1_9.001_master.h5
/Volumes/Data/LSCAT/12_2019/MK_1_10/MK_1_10.001_master.h5
/Volumes/Data/LSCAT/12_2019/cq136a_2/cq163_2.001_master.h5
/Volumes/Data/LSCAT/12_2019/cq136a_7/cq163_7.001_master.h5
/Volumes/Data/LSCAT/12_2019/cq136a_8/cq163_8.001_master.h5
/Volumes/Data/LSCAT/12_2019/cq136a_10/cq163_10.001_master.h5
/Volumes/Data/LSCAT/3_2020/MK_3_2/mk_3_1_2_2.001_master.h5
/Volumes/Data/LSCAT/3_2020/MK_3_7/mk_3_1_2_7.001_master.h5
```

Here we have a couple of challenges - HDF5 vs. CBF data and a collection of different directories. Happily all the GMCA data are CBF format, all the LSCAT data HDF5, so probably easier to write the same script _twice_ once for each:

```
GMCA_DATA=/Volumes/Data/GMCA

for PREFIX in \
7_19_2019/MK_2_5/collect/Q5_1 \
7_19_2019/MK_2_5/collect/Q5_1_INV \
GMCA11_19_2019/MK_10_13/collect/C13_1_1 \
GMCA11_19_2019/MK_10_13/collect/C13_1 \
GMCA11_19_2019/MK_9_11/collect/B11_5_1 \
GMCA11_19_2019/MK_9_11/collect/B11_5_1_1 \
GMCA11_19_2019/MK_9_13/collect/B13_5_1 ; do
  WORK=$(basename ${PREFIX})
  mkdir ${WORK}
  cd ${WORK}
  dials.import ${GMCA_DATA}/${PREFIX}_*.cbf
  dials.find_spots imported.expt
  cd -
done

LSCAT_DATA=/Volumes/Data/LSCAT

for PREFIX in \
12_2019/MK_1_1/MK_1_1.001 \
12_2019/MK_1_2/MK_1_2.001 \
12_2019/MK_1_8/MK_1_8.001 \
12_2019/MK_1_9/MK_1_9.001 \
12_2019/MK_1_10/MK_1_10.001 \
12_2019/cq136a_2/cq163_2.001 \
12_2019/cq136a_7/cq163_7.001 \
12_2019/cq136a_8/cq163_8.001 \
12_2019/cq136a_10/cq163_10.001 \
3_2020/MK_3_2/mk_3_1_2_2.001 \
3_2020/MK_3_7/mk_3_1_2_7.001 ; do
  WORK=$(basename ${PREFIX})
  mkdir ${WORK}
  cd ${WORK}
  dials.import ${GMCA_DATA}/${PREFIX}_master.h5
  dials.find_spots imported.expt
  cd -
done
```

Now, it is fair to say I have pulled a 🐰 from a 🎩 here - but don't worry, we will talk through these things now.

## Command Substitution

In the script above we had `WORK=$(basename ${PREFIX})` - this is more variable substitution but with `()` rather than `{}` brackets - this means:

- run `basename ${PREFIX}` - which gives the "end" of `${PREFIX}` after the last `/`
- assign the output of that command to `WORK`

This is a _very_ powerful tool which works in this case as all the end file names (CBF prefixes, master file names) are unique. If this wasn't the case you may want to try and roll all the directory stuff in too, which would work fine:

```
LSCAT_DATA=/Volumes/Data/LSCAT

for PREFIX in \
12_2019/MK_1_1/MK_1_1.001 \
12_2019/MK_1_2/MK_1_2.001 \
12_2019/MK_1_8/MK_1_8.001 \
12_2019/MK_1_9/MK_1_9.001 \
12_2019/MK_1_10/MK_1_10.001 \
12_2019/cq136a_2/cq163_2.001 \
12_2019/cq136a_7/cq163_7.001 \
12_2019/cq136a_8/cq163_8.001 \
12_2019/cq136a_10/cq163_10.001 \
3_2020/MK_3_2/mk_3_1_2_2.001 \
3_2020/MK_3_7/mk_3_1_2_7.001 ; do
  WORK=${PREFIX}
  mkdir -p ${WORK}
  cd ${WORK}
  dials.import ${GMCA_DATA}/${PREFIX}_master.h5
  dials.find_spots imported.expt
  cd -
done
```

This would keep the processing structured exactly like the original data - with many subdirectories too. Note well that there is now `mkdir -p` which makes all the parent directories necessary to make the full directory. If you did happen to run with this, when you came to run the tutorial for multi-crystal processing afterwards you'd need to do a teeny bit more UNIX magic.

## The full script

Let's just say, we want to keep the directory structure we have the data in, we want to process it all with the simple `dials` script then merge it all with the `xia2.multiplex` command at the end of the other tutorial, what would that look like? It would be this:

```
GMCA_DATA=/Volumes/Data/GMCA

for PREFIX in \
7_19_2019/MK_2_5/collect/Q5_1 \
7_19_2019/MK_2_5/collect/Q5_1_INV \
GMCA11_19_2019/MK_10_13/collect/C13_1_1 \
GMCA11_19_2019/MK_10_13/collect/C13_1 \
GMCA11_19_2019/MK_9_11/collect/B11_5_1 \
GMCA11_19_2019/MK_9_11/collect/B11_5_1_1 \
GMCA11_19_2019/MK_9_13/collect/B13_5_1 ; do
  WORK=${PREFIX}
  mkdir -p ${WORK}
  cd ${WORK}
  dials.import ${GMCA_DATA}/${PREFIX}_*.cbf
  dials.find_spots imported.expt
  cd -
done

LSCAT_DATA=/Volumes/Data/LSCAT

for PREFIX in \
12_2019/MK_1_1/MK_1_1.001 \
12_2019/MK_1_2/MK_1_2.001 \
12_2019/MK_1_8/MK_1_8.001 \
12_2019/MK_1_9/MK_1_9.001 \
12_2019/MK_1_10/MK_1_10.001 \
12_2019/cq136a_2/cq163_2.001 \
12_2019/cq136a_7/cq163_7.001 \
12_2019/cq136a_8/cq163_8.001 \
12_2019/cq136a_10/cq163_10.001 \
3_2020/MK_3_2/mk_3_1_2_2.001 \
3_2020/MK_3_7/mk_3_1_2_7.001 ; do
  WORK=${PREFIX}
  mkdir -p ${WORK}
  cd ${WORK}
  dials.import ${GMCA_DATA}/${PREFIX}_master.h5
  dials.find_spots imported.expt
  dials.index imported.expt strong.refl
  dials.refine indexed.expt indexed.refl
  dials.integrate refined.expt refined.refl
  cd -
done

mkdir multiplex
cd multiplex
xia2.multiplex $(find .. -name 'integrated.*')
```

The last command at the very end is now doing some more magic - it is running the UNIX `find` command to go find all the `dials.integrate` output then gives it to the `xia2,multiplex` command as input. From this point you can continue the other tutorial.

## Extra Credit

Wait, that UNIX `find` command can just dig everything out? Yup. So we can have:

```
DATA=/Volumes/Blue2/Data/vmxi-ab5081/well_139_subset

for MASTER in $(find ${DATA} -name '*_master.h5'); do
  WORK=$(basename ${MASTER} | sed 's/_master.h5//')
  mkdir -p ${WORK}
  cd ${WORK}
  dials.import ${DATA}/${PREFIX}_master.h5
  dials.find_spots imported.expt
  dials.index imported.expt strong.refl
  dials.refine indexed.expt indexed.refl
  dials.integrate refined.expt refined.refl
  cd -
done
```

What we have done here is to `find` everything which matches `*_master.h5` in `${DATA}` and then make a tidy work directory by grabbing just the master file name and using the UNIX `sed` (stream editor) to strip off the `_master.h5` part of the file name. This is getting pretty advanced but it is pretty powerful and useful to know. The command above could be made something you can run _over and over again_ in a beam time by checking if `${WORK}` exists and only doing the processing if it did not:

```
DATA=/Volumes/Blue2/Data/vmxi-ab5081/well_139_subset

for MASTER in $(find ${DATA} -name '*_master.h5'); do
  WORK=$(basename ${MASTER} | sed 's/_master.h5//')
  if [ ! -d ${WORK} ] then
    mkdir -p ${WORK}
    cd ${WORK}
    dials.import ${DATA}/${PREFIX}_master.h5
    dials.find_spots imported.expt
    dials.index imported.expt strong.refl
    dials.refine indexed.expt indexed.refl
    dials.integrate refined.expt refined.refl
  fi
  cd -
done
```

where we have added `if [ ! -d ${WORK} ] then` which checks if `!` (not) `-d` (is a directory) `${WORK}` then we proceed to do all of the things before we get to `fi`. This would mean if more data have appeared since you last ran the script, they would get processed but the old data would be untouched.
