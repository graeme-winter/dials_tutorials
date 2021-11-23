# Shell Scripting Exercise (Extra Credit Worked Example)

This is a non-trivial worked example to answer a real question: which of the very many data sets I measured on November 18th gave me the highest resolution `xia2-dials` run. One could answer this with some careful book-keeping and a tedious trawl through SynchWeb, but that is not my style. 

Start off in the right place:

```
cd /dls/i03/data/2021/mx30951-8/processed/gw/20211118/TestInsulin
```

This is where all the processing went at that time for these samples. So, we are looking for output from `xia2` running with DIALS - in the Diamond environment this is files called `xia2.txt` in directories called `xia2-dials` but we want to exclude `multi-xia2-dials` so...

```
find . -name 'xia2.txt'
find . -name 'xia2.txt' | grep xia2-dials
find . -name 'xia2.txt' | grep xia2-dials | grep -v multi
```

`grep -v` _excludes_ whatever you say so we will eliminate anything with multi in the filename. OK, so we have the filenames - now we need to find the ones where we processed the data in the right space group - I23 in this case - which means we are looking for `Assuming spacegroup: I 2 3` in the output - 

```
for file in $(find . -name 'xia2.txt' | grep xia2-dials | grep -v multi) ; do 
  echo ${file} $(grep Assuming $file | cut -d : -f 2); 
done | grep 'I 2 3' | awk '{print $1}'
```

This will now output a list containing all the xia2.txt files where the processing was "correct" - next we need to extract the high resolution limit from these - that's in this section of the output:

```
For mx30951v8/xins52/SAD                     Overall    Low     High
High resolution limit                           1.31    3.56    1.31
Low resolution limit                           54.93   54.98    1.33
Completeness                                   99.0   100.0    86.6
```

So:

```
grep "High resolution limit" $(for file in $(find . -name 'xia2.txt' | grep xia2-dials | grep -v multi); do echo ${file} $(grep Assuming $file | cut -d : -f 2);  done | grep 'I 2 3' | awk '{print $1}')
```

will get the resolution line - we want to know the highest shell limit (last number) and the data set this came from (first two tokens separated by `/`) so let's replace `/` with spaces then figure out which tokens we actually _want_ - 

```
grep "High resolution limit" $(for file in $(find . -name 'xia2.txt' | grep xia2-dials | grep -v multi) ; do echo ${file} $(grep Assuming $file | cut -d : -f 2); done | grep 'I 2 3' | awk '{print $1}') | sed 's$/$ $g'
```

(leaning quite heavily on `sed` now, but you can google how to use that) - next we need to re-arrange to have the resolution _first_ so we can sort on it (`sort -rn` gives a reverse numerical sort)

```
grep "High resolution limit" $(for file in $(find . -name 'xia2.txt' | grep xia2-dials | grep -v multi) ; do echo ${file} $(grep Assuming $file | cut -d : -f 2); done | grep 'I 2 3' | awk '{print $1}') | sed 's$/$ $g' | awk '{print $NF, $2, $3}'
```

So then we sort it, then shuffle the tokens back into the order we want for viewing - and learn which was the highest 

```
grep "High resolution limit" $(for file in $(find . -name 'xia2.txt' | grep xia2-dials | grep -v multi) ; do echo ${file} $(grep Assuming $file | cut -d : -f 2); done | grep 'I 2 3' | awk '{print $1}') | sed 's$/$ $g' | awk '{print $NF, $2, $3}' | sort -rn | awk '{print $2"/"$3, $1}'
```

From which we know which is the highest resolution one: this may not be the _best_ data set but however you slice the problem, you can use these tools to get the job done. 