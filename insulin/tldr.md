# TL;DR

## Script

This is the shortest script for processing the tutorial data with DIALS assuming you have the data in a parent directory:

```
dials.import ../ins_1_2.nxs [image_range=1,180]
dials.find_spots imported.expt
dials.index imported.expt strong.refl
dials.refine indexed.expt indexed.refl
dials.integrate refined.expt refined.refl
dials.symmetry integrated.expt integrated.refl
dials.scale symmetrized.expt symmetrized.refl
```

If you run this _before_ working through the tutorial you can spend the time looking at the log files (e.g. `cat dials.find_spots.log`) rather than waiting for the individual tasks to complete.

If you're in a hurry looking at the first 180 images (90 degrees) is enough to do something useful, so include the `image_range=1,180` at the import stage.