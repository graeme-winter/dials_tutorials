# TL;DR

## Script

This is the shortest script for processing the tutorial data with DIALS assuming you have the data in a parent directory:

```
dials.import /shared/data/projects/zenodo/simple_cubic_insulin/ins10_1.nxs image_range=1,600
dials.find_spots imported.expt
dials.index imported.expt strong.refl
dials.refine indexed.expt indexed.refl
dials.integrate refined.expt refined.refl
dials.symmetry integrated.expt integrated.refl
dials.scale symmetrized.expt symmetrized.refl absorption_level=medium
dials.export scaled.expt scaled.refl
dials.merge scaled.expt scaled.refl
```

This is only processing 120° of one of the data sets but on my laptop runs in about 12 minutes on my laptop. If you run this _before_ working through the tutorial you can spend the time playing with the viewers and looking at the log files (e.g. `less dials.index.log`) rather than waiting for the individual tasks to complete.
