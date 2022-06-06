Python Scripting
================

Since much of DIALS is written in Python there is a lot you can do using the DIALS python interpreter `dials.python`. In particular, you can perform fine grained analysis or ask specific questions which the program authors have not answered for you.

Any non-trivial program could potentially be quite involved, but asking simple questions about e.g. spots is quite simple - for example "what is the distribution in spot sizes, in terms of signal pixels?" This explores sufficient terrain in the DIALS environment that it does something useful, without being punishing to follow along with.

DIALS Concepts
--------------

DIALS has two main types of data: the reflection data kept in files called `thing.refl` e.g. `indexed.refl` and then experiment descriptions in `thing.refl` e.g. `indexed.refl`. To ask this question we need only look at the reflections. The reflection data are kept in a "reflection table" which you can think of as a spreadsheet with one row for each reflection, and different columns for things like the X, Y position on the detector, image number and so on.