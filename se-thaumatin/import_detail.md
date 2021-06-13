# Import (details)

## Introduction

In importing we create "models" of the data we want to process - this includes an understanding of what the data are, how many scans, where the detector is, wavelength etc. and it is the point where any corrections that are known up front should be made. Hopefully all of the metadata in the images will be correct (in 2021 this is much more likely than it was in 1998!) so really all you are identifying is what input you would like to use.

## Input

The basic operation of `dials.import` is as:

```
dials.import ../*.cbf
```

or

```
dials.import ../*master.h5
```

to import all of the CBF or master files in the parent directory. The output from import will "explain" what it understood from the data (discussed below). At this point you can also include subsets of the data e.g.

```
dials.import ../xtal_1_5_master.h5 image_range=1,100
```

which will import the first 100 images (i.e. 1 to 100 inclusive) for processing - if you know the sample moved out of the beam (say) this can be a useful way of including only the good data.

The most likely parameters for override would be the detector distance with `distance=190` (to indicate that the detector is 190mm away from sample) or `slow_fast_beam_centre=109,105` (again, in mm) - in most cases these should be correct. If you want to copy the beam centre from the processing results of another data set, run `dials.show` on one of the experiment files and look for the `Beam centre` block:

```
Beam centre: 
    mm: (155.99,166.56)
    px: (2079.89,2220.80)
```

DIALS can support much more complex experimental geometries as well as supporting fundamental detector commissioning where you can override all the details - that is material for a different tutorial however. 

## Output

`dials.import` writes a short description of what was imported to the output e.g.:

```
DIALS (2018) Acta Cryst. D74, 85-97. https://doi.org/10.1107/S2059798317017235
DIALS 3.5.0-g82bac9855-release
The following parameters have been modified:

input {
  experiments = <image files>
}

--------------------------------------------------------------------------------
  format: <class 'dxtbx.format.FormatNexusEigerDLS16M.FormatNexusEigerDLS16M'>
  num images: 1800
  sequences:
    still:    0
    sweep:    1
  num stills: 0
--------------------------------------------------------------------------------
Writing experiments to imported.expt
```

If you expected 1800 images as a single sweep, from an Eiger detector, then this looks right. More complex cases e.g. with 4 sweeps of data from a single sample could look like:

```
--------------------------------------------------------------------------------
  format: <class 'dxtbx.format.FormatCBFFullPilatus.FormatCBFFullPilatus'>
  num images: 3450
  sequences:
    still:    0
    sweep:    4
  num stills: 0
--------------------------------------------------------------------------------
Writing experiments to imported.expt
```

In this tutorial we will only be considering single-sweep data. 

The `format` here is more than the file format - it is the specialised
reader code that was found to be appropriate for this data, which
allows certain local customisations. In the case of data from Diamond,
this includes the shadow model for the goniometer.
