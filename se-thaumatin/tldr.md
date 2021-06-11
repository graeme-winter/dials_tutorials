# TL;DR

## Script

This is the shortest script for processing the tutorial data with DIALS assuming you have the data in a parent directory:

```
dials.import ../SeThau_1_1_master.h5
dials.find_spots imported.expt
dials.index imported.expt strong.refl
dials.refine indexed.expt indexed.refl
dials.integrate refined.expt refined.refl
dials.symmetry integrated.expt integrated.refl
dials.scale symmetrized.expt symmetrized.refl
dials.export scaled.expt scaled.refl
dials.merge scaled.expt scaled.refl
```

If you run this _before_ working through the tutorial you can spend the time looking at the log files (e.g. `cat dials.find_spots.log`) rather than waiting for the individual tasks to complete.

On one of the virtual machines for the APS workshop this script takes
~ 18 minutes to execute - most of that time spent in
`dials.integrate`. 
