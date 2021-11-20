# Shell Scripting Exercise

Find and save a file with the real names of who we are sharing this computer with. 

```
who
```

Says who is logged in right now, with their username, which could well be meaningless. 

```
awk '{print $3}'
```

will print the third token (i.e. "word" where words are separated by spaces) in every line. 

```
sort
```

by default just performs an alphabetic sort - which is very useful if we want to run

```
uniq
```

to get the unique instances of the usernames. We don't want to count them, just remove duplicates. With these commands we can do quite a lot, but to do something with _every_ one of these is beyond a one liner unless you get excited by that kind of thing. So, we need a script. 

```
$(who)
```

will run `who` and then replace the _value_ of what comes out of that on the command line - in this case that will be nonsense but if we combine the tools above we can get a nice list of unique user names. Once we have that list of user names, we can do a `for` loop:

```
for name in alice bob cherry; do 
echo ${name}
done
```

will print:

```
alice
bob
cherry
```

On our systems we can get a real person name using a command called `getent` (which you will never need again, so don't bother to remember this):

```
getent password ${name}
```

Will print what we know about the person with that username, separated by colons. To get what we want we can use another program `cut` which splits up lines, for named delimiters e.g. 

```
cut -d :
```

but we also have to say what _field_ we want (i.e. _which_ thing between `:`) so we count along and figure we want number 5, so

```
cut -d : -f 5
```

will extract the names we want. Finally, we can save these names with:

```
> ${USER}.names
```

which will write the output not to the screen but to a file which should be called "_your_ username".names. Getting the job done will involve connecting some of the commands above, using pipes, then using the `for` loop and sub shell `$(command | other)` stuff in the right way. 