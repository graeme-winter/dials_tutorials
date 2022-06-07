Python Scripting
================

Since much of DIALS is written in Python there is a lot you can do using the DIALS python interpreter `dials.python`. In particular, you can perform fine grained analysis or ask specific questions which the program authors have not answered for you.

Any non-trivial program could potentially be quite involved, but asking simple questions about e.g. spots is quite simple - for example "what is the distribution in spot sizes, in terms of signal pixels?" This explores sufficient terrain in the DIALS environment that it does something useful, without being punishing to follow along with.

DIALS Concepts
--------------

DIALS has two main types of data: the reflection data kept in files called `thing.refl` e.g. `indexed.refl` and then experiment descriptions in `thing.refl` e.g. `indexed.refl`. To ask this question we need only look at the reflections. The reflection data are kept in a "reflection table" which you can think of as a spreadsheet with one row for each reflection, and different columns for things like the X, Y position on the detector, image number and so on. Unlike a spreadsheet however data items can be _complex_ i.e. be themselves vectors (like a position in space, as `xyz.px.values` or Miller indices) or "ragged" e.g. the reflection shoe boxes from spot finding, where the boxes themselves vary in dimensions from one reflection to the next.

Inside DIALS the data are handled by CCTBX `flex` arrays, which can be converted to `numpy` arrays if needed with no copying. `flex` also includes operations for e.g. mathematical operations and histogram generation, which we will use here.

To measure the spot size in terms of signal pixels, we need to know which pixels were signal and create an array of the number of such pixels. The pixels have "flag" values assigned in spot finding, which characterise them as e.g. peak, background, overloaded. Signal pixels are masked as "foreground" as they are not... background, so for each spot in the list we need to count the number of pixels which have the foreground flag. For bonus points, let's also filter out only the indexed reflections.

Practicalities
--------------

This tutorial was _not_ written based on knowing all the syntax: it was written by knowing how to open a DIALS reflection file in Python and knowing that `help(thing)` prints Python help. So, the start set of command lines looked like:

```python
from dials.array_family import flex
data = flex.reflection_table.from_file("indexed.refl")
help(data)
```

A little "poking around" indicated how to filter on indexed reflections:

```python
data = data.select(data.get_flags(data.flags.indexed))
```

and then how to read the shoebox mask

```python
data[0]["shoebox"].count_mask_values(MaskCode.Foreground)
```

This then means we can collate all the data we want. Adding the bits to collate all the data into an array then make a histogram was relatively straightforward:

```python
import sys

from dials.array_family import flex
from dials.algorithms.shoebox import MaskCode


def analysis(filename):
    data = flex.reflection_table.from_file(filename)
    data = data.select(data.get_flags(data.flags.indexed))

    pixels = flex.int()

    for j in range(data.size()):
        pixels.append(data[j]["shoebox"].count_mask_values(MaskCode.Foreground))

    hist = flex.histogram(pixels.as_double(), data_min=0, data_max=1000, n_slots=100)

    for centre, value in zip(hist.slot_centers(), hist.slots()):
        print(centre, value)


if __name__ == "__main__":
    analysis(sys.argv[1])
```
