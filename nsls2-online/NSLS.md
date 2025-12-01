# Processing in Detail: Simple Lysozyme to Learn Workflow

## Introduction

DIALS processing may be performed by either running the individual tools (spot finding, indexing, refinement, integration, symmetry, scaling, exporting to MTZ) or you can run `xia2`, which makes (we hope) informed choices for you at each stage. In this tutorial we will run through each of the steps in turn, taking a look at the output as we go. We will also look at enforcing the correct lattice symmetry.

The aim of this tutorial is to introduce you to the tools, not teach about data processing - it is assumed you have some idea of the overall process from e.g. other tutorials or lectures. With the graphical tools, I am not making so much effort to explain the options as simply "playing" will give you a chance to learn your way around and also find the settings which work for you. Particularly with looking at diffraction images, the "best" settings are very personal.

## DIALS version

This tutorial assumes you are using a recent version of [DIALS](https://dials.github.io/installation.html) and that you have this set up (i.e. you've sourced the setup file).

If you are running at home on Linux or macOS then you should be able to reproduce the results in here. If you are on Windows, try installing the Linux version in a WSL terminal using e.g. Ubuntu or using the version from CCP4, but be aware that there may be small differences in the output.

## Tutorial data

The tutorial data here are lysozyme data collected at NSLS II - however the _process_ you follow tends to be very similar for almost any data, but the phenomena observed and how you handle them may differ. The data can be downloaded [here](https://drive.google.com/file/d/1T2Vf8kEG9RIT4QB_q_729ntfZUgsuS7d/view?usp=drive_link).

## Files

DIALS creates two principal file types:

- experiment files called `something.expt`
- reflection files called `something.refl`

"Experiment" in DIALS has a very specific meaning - the capturing of data from one set of detector, beam, goniometer and crystal - so if you have two scans from one crystal this is two experiments, if you have two lattices on one data set this is two experiments. In most cases you can ignore this distinction though - it becomes more important in the [more complex tutorials](./COWS_PIGS_PEOPLE.md).

Usually the output filenames will correspond to the name of the DIALS program that created them e.g. `indexed.refl` and `indexed.expt` from `dials.index`. The only deviations from this are on import (see below) where we are only reading experiment models and spot finding where we find _strong_ reflections so write these to `strong.refl` - and we create no models so (by default) there is no output experiment file.

At any time you can _look_ at these files with `dials.show` which will summarise the content of the files to the terminal. You can also `dials.show` reflection files which gives a tabular symmary of the content but this can be rather slow, as the data are much more substantial.

[If you're impatient...](./TLDR.md) - as a note this is essentially the script I would use to have a first look at any data set where I expected the experiment metadata (wavelength, beam centre etc.) to be correct.

## Parameters

All DIALS programs accept parameters in the form of `parameter=value` - in most cases this will be sufficient though some less frequently used options may require "name space" clarification e.g. `index_assignment.method=local`. All of the DIALS programs support the option

```
dials.program -c -e2
```

which will show you all possible configuration options - if you are looking for an option this is the simplest way to search so e.g.

```
dials.index -c -e2 | less
```

will allow you to scroll through the extensive list of options you can adjust. In most cases the defaults are relatively sensible for synchrotron data from a pixel array detector, as we are using in this tutorial.

## Output

In the majority of cases the `dials` programs write their output to `dials.program.log` e.g. `dials.find_spots.log` etc. - everything which is printed to the terminal is also saved in this file, so you can review the processing later. In the case where you are reporting an issue to the developers including these log files in the error report (particularly for the step which failed) is very helpful.

From most stages you can generate a detailed of the current state of processing with:

```
dials.report step.expt step.refl
```

which will generate a HTML html describing the current state of the processing.

## Import

The starting point for any processing with DIALS is to _import_ the data - here the metadata are read and a description of the data to be processed saved to a file named `imported.expt`. This is "human readable" in that the file is JSON format (roughly readable text with brackets around to structure for computers). While you can edit this file if you know what you are doing, usually this is not necessary.

```
dials.import ../LysFMX_01_8704_master.h5
```

will read the metadata from this `master` file and write `imported.expt` from this. It is important to note that for well-behaved data (i.e. anything which is well-collected from a well-behaved sample) the commands below will often be identical after importing. The output from importing describes what was found: this should correspond to our expectations.

```
DIALS (2018) Acta Cryst. D74, 85-97. https://doi.org/10.1107/S2059798317017235
DIALS 3.dev.1386-g1a2d56924
The following parameters have been modified:

input {
  experiments = <image files>
}

--------------------------------------------------------------------------------
  format: <class 'dxtbx.format.FormatNXmxEigerFilewriter.FormatNXmxEigerFilewriter'>
  template: /Users/graeme/data/NSLS/LysFMX_01_8704_master.h5:1:900
  num images: 900
  sequences:
    still:    0
    sweep:    1
  num stills: 0
--------------------------------------------------------------------------------
Writing experiments to imported.expt
```

You will see that the log file includes the additional commands passed in, which is useful for tracing the processing options used. Once you have `imported.expt` you can, if you like, look at the content with `dials.show` as `dials.show imported.expt`. This is a general program in DIALS to allow you to print the current state of models, with output which looks like:

```
DIALS (2018) Acta Cryst. D74, 85-97. https://doi.org/10.1107/S2059798317017235
The following parameters have been modified:

input {
  experiments = imported.expt
}

Experiment 0:
Experiment identifier: 2b1eb41b-a8ec-df7a-fd79-e4515ee364fc
Image template: /Users/graeme/data/NSLS/LysFMX_01_8704_master.h5
Detector:
Panel:
  name: /entry/instrument/detector/module
  type: SENSOR_PAD
  identifier: 
  pixel_size:{0.075,0.075}
  image_size: {4150,4371}
  trusted_range: {0,59991}
  thickness: 0.45
  material: Si
  mu: 3.95847
  gain: 1
  pedestal: 0
  fast_axis: {1,0,0}
  slow_axis: {0,-1,0}
  origin: {-150.15,168.825,-150}
  distance: 150
  pixel to millimeter strategy: ParallaxCorrectedPxMmStrategy
    mu: 3.95847
    t0: 0.45


Max resolution (at corners): 1.022156
Max resolution (inscribed):  1.279456

Beam:
    probe: x-ray
    wavelength: 0.979338
    sample to source direction : {0,0,1}
    divergence: 0
    sigma divergence: 0
    polarization normal: {0,1,0}
    polarization fraction: 0.999
    flux: 0
    transmission: 1
    sample to source distance: 0

Beam centre: 
    mm: (150.15,168.82)
    px: (2002.00,2251.00)

Scan:
    number of images:   900
    image range:   {1,900}
    epoch:    0
    exposure time:    0.02
    oscillation:   {0,0.2}

Goniometer:
    Rotation axis:   {1,0,0}
    Fixed rotation:  {1,0,0,0,1,0,0,0,1}
    Setting rotation:{1,0,0,0,1,0,0,0,1}
```

I recognise that this is quite "computer" in the way that the numbers are presented, but there are a few useful things you can look for in here: does the wavelength, distance, beam centre look OK? Are the number of images what you would expect?

At this point you can also look at the images with the `dials.image_viewer` tool -

```
dials.image_viewer imported.expt
```

in this tool there are many settings you can adjust, which could depend on the source of the data and - most importantly - your preferences. Personally the author finds for basic inspection of the images stacking e.g. 10 images makes the lattice clearer for finely sliced images, and adjusting the brightness depending on how your data were collected:

![Image viewer](./images/image-view.png)

If the data are not stacked the spot finding process can also be explored - the controls at the bottom of the "Settings" window:

![Image viewer: settings](./images/image-view-settings.png)

allow you to step through these and can be very useful for getting a "computer's eye view" of how the data look (particularly for establishing where the diffraction is visible to.)

## Find Spots

The first "real" task in any processing using DIALS is the spot finding. Since this is looking for spots on every image in the dataset, this process can take some time so by default will use all of the processors available in your machine - if you would like to control this adjust with e.g. `nproc=16` - however the default is usually sensible unless you are sharing the computer with many others.

```
dials.find_spots imported.expt
```

This is one of the two steps where every image in the data set is read and processed and hence can be moderately time-consuming. This contains a reflection file `strong.refl` which contains both the positions of the strong spots and also "images" of the spot pixels which we will use later. You can view these spots on top of the images with

```
dials.image_viewer imported.expt strong.refl
```

to get a sense of what spots were found. You will see that the spots are surrounded by little boxes - these are the _bounding boxes_ of the reflections i.e. the outer extent of the pixels that belong to that spot. The "signal" pixels are highlighted with green blobs giving a sense of what is and is not "strong."

![Image viewer](./images/image-view-spots.png)

The default parameters for spot finding usually do a good job for Pilatus or Eiger images, such as these. However they may not be optimal for data from other detector types, such as CCDs or image plates. Issues with incorrectly set gain might, for example, lead to background noise being extracted as spots. You can use the image mode buttons to preview how the parameters affect the spot finding algorithm. The final button 'threshold’ is the one on which spots were found, so ensuring this produces peaks at real diffraction spot positions will give the best chance of success. In most cases you won't need this unless you are involved with something experimental.

The second tool for visualisation of the found spots is the reciprocal lattice viewer - which presents a view of the spot positions mapped to reciprocal space.

```
dials.reciprocal_lattice_viewer imported.expt strong.refl
```

No matter the sample orientation you should be able to rotate the space to "look down" the lines of reflections. If you cannot, or the lines are not straight, it is likely that there are some errors in the experiment parameters e.g. detector distance or beam centre. If these are not too large they will likely be corrected in the subsequent analysis.

![Reciprocal viewer](./images/rlv0.png)

Have a play with the settings - you can change the beam centre in the viewer to see how nicely aligned spots move out of alignment. Some of the options will only work after you have indexed the data. If the geometry is not accurately recorded you may find it useful to run:

```
dials.search_beam_position imported.expt strong.refl
```

to determine an updated position for the beam centre - ideally the shift that this calculates should be small if the beamline is well-calibrated e.g.

```console
Selecting subset of 10000 reflections for analysis
Running DPS using 10000 reflections
Found 6 solutions with max unit cell 102.42 Angstroms.
Old beam centre: 150.15, 168.82 mm (2002.0, 2251.0 px)
New beam centre: 150.27, 169.01 mm (2003.6, 2253.5 px)
Shift: -0.12, -0.19 mm (-1.6, -2.5 px)

Saving optimised experiments to optimised.expt
```

if it is a couple of mm or more it may be worth discussing this with the beamline staff! Running the reciprocal lattice viewer with the optimised experiment output:

```
dials.reciprocal_lattice_viewer optimised.expt strong.refl
```

should show straight lines, provided everything has worked correctly.

## Indexing

The next step will be indexing of the found spots with `dials.index` - by default this uses a 3D FFT algorithm to identify periodicity in the reciprocal space mapped spot positions, though there are other algorithms available which can be better suited to e.g. narrow data sets.

```
dials.index imported.expt strong.refl
```

or

```
dials.index optimised.expt strong.refl
```
   
are the ways to trigger the program, and the most common parameters to set are the `space_group` and `unit_cell` if these are known in advance. While this does index the data it will also perform some refinement with a static crystal model, and indicate in the output the fraction of reflections which have been indexed - ideally this should be close to 100%:

```
Refined crystal models:
model 1 (146823 reflections):
Crystal:
    Unit cell: 38.3357(13), 76.841(3), 76.868(3), 90.0240(7), 90.0099(8), 89.9794(7)
    Space group: P 1
    U matrix:  {{-0.786404, -0.444106,  0.429346},
                {-0.315920,  0.886438,  0.338264},
                {-0.530814,  0.130373, -0.837400}}
    B matrix:  {{ 0.026085,  0.000000,  0.000000},
                {-0.000009,  0.013014,  0.000000},
                { 0.000004,  0.000005,  0.013009}}
    A = UB:    {{-0.020508, -0.005777,  0.005586},
                {-0.008248,  0.011538,  0.004401},
                {-0.013851,  0.001692, -0.010894}}
+------------+-------------+---------------+---------------+-------------+
|   Imageset |   # indexed |   # unindexed |   # unindexed |   % indexed |
|            |             |         total |       non-ice |             |
|------------+-------------+---------------+---------------+-------------|
|          0 |      146823 |         20645 |         17946 |        87.7 |
+------------+-------------+---------------+---------------+-------------+
```

If it is significantly less than 100% it is possible you have a second lattice - adding `max_lattices=2` (say) to the command-line will indicate to the program that you would like to consider attempting to separately index the unindexed reflections after the first lattice has been identified. Often the second lattice is a satellite of the main one, as crystals sometimes split when cooled.

By default the triclinic lattice i.e. with `P1` no additional symmetry is assumed - for the majority of data there are no differences in the quality of the results from assigning the Bravais lattice at this stage, even if as here it is perfectly obvious what the correct answer is.

If successful, `dials.index` writes the experiments and indexed reflections to two new files `indexed.expt` and `indexed.refl` - if these are loaded in the reciprocal lattice viewer you can see which spots have been indexed and if you have multiple lattices switch them "on and off" for comparison.

The process that the indexing performs is quite complex -

- make a guess at the maximum unit cell from the pairwise separation of spots in reciprocal space
- transform spot positions to reciprocal space using the best available current model of the experimental geometry
- perform a Fourier transform of these positions or other algorithm to identify the _basis vectors_ of these positions e.g. the spacing between one position and the next
- determine a set of these basis vectors which best describes the reciprocal space positions
- transform this set of three basis vectors into a unit cell description, which is then manipulated according to some standard rules to give the best _triclinic_ unit cell to describe the reflections - if a unit cell and space group have been provided these will be enforced at this stage
- _assign indices_ to the reflections by "dividing through" the reciprocal space position by the unit cell parallelopiped (this is strictly the actual indexing step)
- take the indexed reflections and refine the unit cell parameters and model of the experimental geometry by comparing where the reflections should be and where they are found
- save the indexed reflections and experiment models to the output files

The indexing process takes place over a number of cycles, where low resolution reflections are initially indexed and refined before including more reflections at high resolution - this improves the overall success of the procedure by allowing some refinement as a part of the process.
  
During this process an effort is made to eliminate "outlier" reflections - these are reflections which do not strictly belong to the crystal lattice but are accidentally close to a reciprocal space position and hence can be indexed. Most often this is an issue with small satellite lattices or ice / powder on the sample. Usually this should not be a cause for concern. To look at the crystal lattice(s) in the reciprocal space crystal frame you can select "crystal frame":

![Reciprocal viewer](./images/rlv1.png)

## Bravais Lattice Determination (optional!)

Once you have indexed the data you may optionally attempt to infer the correct Bravais lattice and assign this to constrain the unit cell in subsequent processing. If, for example, the unit cell from indexing has all three angles close to 90° and two unit cell lengths with very similar values you could guess that the unit cell is tetragonal. In `dials.refine_bravais_settings` we take away the guesswork by transforming the unit cell to all possible Bravais lattices which approximately match the triclinic unit cell, and then performing some refinement - if the lattice constraints are correct then imposing them should have little impact on the deviations between the observed and calculated reflection positions (known as the R.M.S. deviations). If a lattice constraint is incorrect it will manifest as a significant increase in a deviation - however care must be taken as it can be the case that the true _symmetry_ is lower than the shape of the unit cell would indicate.

In the general case there is little harm in skipping this step, however for information if you run

```
dials.refine_bravais_settings indexed.expt indexed.refl
```

you will see a table of possible unit cell / Bravais lattice / R.M.S. deviations printed in the output - in the case of this tutorial data they will all match, as the true symmetry is tetragonal.

```
Selected 18000 / 167469 reflections for calculation
Chiral space groups corresponding to each Bravais lattice:
aP: P1
mP: P2 P21
mC: C2
oP: P222 P2221 P21212 P212121
oC: C2221 C222
tP: P4 P41 P42 P43 P422 P4212 P4122 P41212 P4222 P42212 P4322 P43212
+------------+--------------+--------+--------------+----------+-----------+-------------------------------------------+----------+------------+
|   Solution |   Metric fit |   rmsd | min/max cc   |   #spots | lattice   | unit_cell                                 |   volume | cb_op      |
|------------+--------------+--------+--------------+----------+-----------+-------------------------------------------+----------+------------|
|   *      9 |       0.0316 |  0.069 | 0.920/0.928  |    16808 | tP        | 76.85  76.85  38.34  90.00  90.00  90.00  |   226397 | b,c,a      |
|   *      8 |       0.0292 |  0.067 | 0.920/0.943  |    16904 | oC        | 108.66 108.71  38.33  90.00  90.00  90.00 |   452834 | b+c,-b+c,a |
|   *      7 |       0.0316 |  0.069 | 0.920/0.954  |    16838 | oP        | 38.34  76.84  76.86  90.00  90.00  90.00  |   226409 | a,b,c      |
|   *      6 |       0.0212 |  0.067 | 0.943/0.943  |    16947 | mC        | 108.71 108.66  38.33  90.00  89.98  90.00 |   452837 | b-c,b+c,a  |
|   *      5 |       0.0292 |  0.068 | 0.922/0.922  |    16892 | mC        | 108.66 108.71  38.34  90.00  89.99  90.00 |   452838 | b+c,-b+c,a |
|   *      4 |       0.0228 |  0.067 | 0.920/0.920  |    16957 | mP        | 76.84  38.33  76.87  90.00  90.03  90.00  |   226431 | -b,-a,-c   |
|   *      3 |       0.0316 |  0.069 | 0.934/0.934  |    16835 | mP        | 38.34  76.84  76.86  90.00  90.01  90.00  |   226408 | a,b,c      |
|   *      2 |       0.0259 |  0.07  | 0.954/0.954  |    16953 | mP        | 38.34  76.87  76.84  90.00  89.98  90.00  |   226415 | -a,-c,-b   |
|   *      1 |       0      |  0.067 | -/-          |    17004 | aP        | 38.33  76.84  76.87  90.03  90.01  89.98  |   226434 | a,b,c      |
+------------+--------------+--------+--------------+----------+-----------+-------------------------------------------+----------+------------+
* = recommended solution
```

If you wish to use one of the output experiments from this process e.g. `bravais_setting_9.expt` you will need to reindex the reflection data from indexing to match this - we do not output every option of reindexed data as these files can be large. In most cases it is simpler to re-run `dials.index` setting the chosen space group.

The reader is reminded here - in most cases it is absolutely fine to proceed without worrying about the crystal symmetry at this stage 🙂.

## Refinement

The model is already refined during indexing, but this is assuming that a single crystal model is appropriate for every image in the data set - in reality there are usually small changes in the unit cell and crystal orientation throughout the experiment as the sample is rotated. `dials.refine` will first re-run refinement with a fixed unit cell and then perform scan-varying refinement. If you have indexed multiple sweeps earlier in processing (not covered in this tutorial) then the crystal models will be copied and split at this stage to allow per-crystal-per-scan models to be refined.

By and large one may run:

```
dials.refine indexed.expt indexed.refl
```

without any options and the program will do something sensible - if you compare the R.M.S. deviations from the end of indexing with the end of refinement you should see a small improvement e.g.

```
RMSDs by experiment:
+-------+--------+----------+----------+------------+
|   Exp |   Nref |   RMSD_X |   RMSD_Y |     RMSD_Z |
|    id |        |     (px) |     (px) |   (images) |
|-------+--------+----------+----------+------------|
|     0 |  18000 |  0.58573 |  0.75912 |    0.52028 |
+-------+--------+----------+----------+------------+
```

to:

```
RMSDs by experiment:
+-------+--------+----------+----------+------------+
|   Exp |   Nref |   RMSD_X |   RMSD_Y |     RMSD_Z |
|    id |        |     (px) |     (px) |   (images) |
|-------+--------+----------+----------+------------|
|     0 | 111662 |  0.37178 |  0.36095 |     0.1852 |
+-------+--------+----------+----------+------------+
```

If you look at the output of `dials.report` at this stage you should see small variations in the unit cell and sample orientation as the crystal is rotated - if these do not appear small then it is likely that something has happened during data collection e.g. severe radiation damage.

## Integration

Once you have refined the model the next step is to integrate the data - in effect this is using the refined model to calculate the positions where all of the reflections in the data set will be found and measure the background-subtracted intensities:

```
dials.integrate refined.expt refined.refl
```

By default this will pass through the data twice, first looking at the shapes of the predicted spots to form a reference profile model then passing through a second time to use this profile model to integrate the data, by being fit to the transformed pixel values. This is by far the most computationally expensive step in the processing of the data. By default all the processors in your computer are used, unless we think this will exceed the memory available in the machine. At times, however, if you have a large unit cell and / or a large data set you may find that processing on a desktop workstation is more appropriate than e.g. a laptop. Optionally you can get a sense of what the integration will do by creating the profile model from the refined reflections and performing the prediction - this will allow viewing the predictions on the images without performing the integration steps.

If you know in advance that the data do not diffract to anything close to the edges of the detector you can assign a resolution limit at this stage by adding `prediction.d_min=1.8` (say) to define a 1.8 Å resolution limit - this should in general not be necessary. At the end of integration two new files are created - `integrated.refl` and `integrated.expt` - looking at these in the image viewer e.g.

```
dials.image_viewer integrated.expt integrated.refl
```

can be very enlightening as you should see little red boxes around every reflection. You may see a selection of reflections close to the rotation axis are missed - these are not well modelled or predicted in any program so typically excluded from processing.

## Symmetry analysis

Before the data may be scaled it is necessary that the crystal symmetry is known - if this was assigned correctly at indexing e.g. `space_group=P43212` then you can proceed directly to scaling. In the majority of cases however it will be unknown or not set at this point, so needs to be assigned between integration and scaling. Even if the Bravais lattice was assigned earlier, the correct symmetry _within_ that lattice is needed.

The symmetry analysis in DIALS takes the information from the spot positions and also the spot intensities. The former are used to effectively re-run `dials.refine_bravais_settings` to identify possible lattices and hence candidate symmetry operations, and the latter are used to assess the presence or absence of these symmetry operations. Once the operations are found, the crystal rotational symmetry is assigned by composing these operations into a putative space group. In addition, systematically absent reflections are also assessed to assign a best guess to translational elements of the symmetry - though these are not needed for scaling, they may help with downstream analysis rather than you having to manually identify them.

```
dials.symmetry integrated.expt integrated.refl
```

is how this step is run. At this point it is important to note that the program is trying to identify all symmetry elements, and does not know that e.g. inversion centres are not possible - so for an oP lattice it will be testing for P/mmm symmetry which corresponds to P2?2?2? in standard MX.

In the output you'll see first the individual symmetry operations:

```
Scoring individual symmetry elements

+--------------+--------+------+--------+-----+---------------+
|   likelihood |   Z-CC |   CC |      N |     | Operator      |
|--------------+--------+------+--------+-----+---------------|
|        0.936 |   9.81 | 0.98 | 261656 | *** | 1 |(0, 0, 0)  |
|        0.909 |   9.4  | 0.94 | 527212 | *** | 4 |(1, 0, 0)  |
|        0.922 |   9.55 | 0.95 | 251504 | *** | 2 |(1, 0, 0)  |
|        0.932 |   9.72 | 0.97 | 287812 | *** | 2 |(0, 1, 0)  |
|        0.929 |   9.65 | 0.97 | 252980 | *** | 2 |(0, 0, 1)  |
|        0.919 |   9.51 | 0.95 | 250998 | *** | 2 |(0, 1, 1)  |
|        0.897 |   9.29 | 0.93 | 280636 | **  | 2 |(0, -1, 1) |
+--------------+--------+------+--------+-----+---------------+
```

Which shows clear 2- and 4-fold symmetry. These are followed by the results of composing these into the possible space groups and the likelihood assessment of these - which takes into consideration the elements present in the space group and also those not present:

```
Scoring all possible sub-groups

+-------------------+-----+--------------+----------+--------+--------+------+-------+---------+--------------------+
| Patterson group   |     |   Likelihood |   NetZcc |   Zcc+ |   Zcc- |   CC |   CC- |   delta | Reindex operator   |
|-------------------+-----+--------------+----------+--------+--------+------+-------+---------+--------------------|
| P 4/m m m         | *** |        0.998 |     9.56 |   9.56 |   0    | 0.95 |  0    |       0 | b,c,a              |
| P m m m           |     |        0.001 |     0.29 |   9.68 |   9.4  | 0.97 |  0.94 |       0 | a,b,c              |
| C m m m           |     |        0.001 |    -0.05 |   9.54 |   9.59 | 0.95 |  0.95 |       0 | b-c,b+c,a          |
| P 4/m             |     |        0     |     0.04 |   9.59 |   9.54 | 0.95 |  0.95 |       0 | b,c,a              |
| P 1 2/m 1         |     |        0     |     0.29 |   9.77 |   9.48 | 0.98 |  0.95 |       0 | a,b,c              |
| P 1 2/m 1         |     |        0     |     0.24 |   9.73 |   9.49 | 0.97 |  0.95 |       0 | -a,-c,-b           |
| P 1 2/m 1         |     |        0     |     0.16 |   9.68 |   9.51 | 0.97 |  0.95 |       0 | -b,-a,-c           |
| C 1 2/m 1         |     |        0     |     0.14 |   9.66 |   9.52 | 0.97 |  0.95 |       0 | b-c,b+c,a          |
| C 1 2/m 1         |     |        0     |    -0.02 |   9.55 |   9.57 | 0.96 |  0.95 |       0 | b+c,-b+c,a         |
| P -1              |     |        0     |     0.29 |   9.81 |   9.52 | 0.98 |  0.95 |       0 | a,b,c              |
+-------------------+-----+--------------+----------+--------+--------+------+-------+---------+--------------------+

Best solution: P 4/m m m
Unit cell: 76.856, 76.856, 38.338, 90.000, 90.000, 90.000
Reindex operator: b,c,a
Laue group probability: 0.998
Laue group confidence: 0.998
```

Here the symmetry appears to be `4 / mmm` i.e. 4-fold rotation and three 2-fold mirror axes - and corresponds to some variation of `P4?2?2` - this information is sufficient for scaling though for structure solution identification of the correct space group is necessary - `dials.symmetry` will also attempt to guess this but in this case it is impossible to see the difference as the screw axes are masked by the centring operation.

## Scaling and Merging

During the experiment there are effects which alter the measured intensity of the reflections, not least radiation damage, changes to beam intensity or illuminated volume or absorption within the sample. The purpose of `dials.scale`, like all scaling programs, is to attempt to correct for these effects by using the fact that symmetry related reflections should share a common intensity. By default no attempt is made to merge the reflections - this may be done independently in `dials.merge` - but a table of merging statistics is printed at the end along with resolution recommendations.

```
dials.scale symmetrized.expt symmetrized.refl anomalous=True
```

for anomalous data or

```
dials.scale symmetrized.expt symmetrized.refl
```

for native - this will run everything with the defaults which allows for:

- modest radiation damage
- changes in overall intensity
- modest sample absorption

with the latter being the parameter most likely changed. If you have a data set recorded from a sample containing a large amount of metal (not common in MX) or recorded at long wavelength e.g, for sulphur SAD it may be necessary to adjust the extent to which the absorption correction is constrained with

```
absorption_level=medium
```

_or_

```
absorption_level=high
```

where setting low, the default, corresponds to ~ 1% absorption, medium to ~ 5% and high to ~ 25% - these are not absolute, more a sense of what you may expect. Testing has indicated that setting it too high is unlikely to do any harm, but setting it too low can have a measurable impact on the quality of the data for phasing experiments. `dials.scale` generates a HTML report `dials.scale.html` which includes a lot of information about how the models look, as well as regions of the data which agree well and poorly - from a practical perspective this is the point where you really _know_ about the final quality of the data. The overall summary data are printed to the console and the log file e.g.:

```
            -------------Summary of merging statistics--------------           

                                            Suggested   Low    High  Overall
High resolution limit                           1.08    2.92    1.08    1.02
Low resolution limit                           76.86   77.05    1.09   76.86
Completeness                                   95.9   100.0    60.1    86.9
Multiplicity                                   11.0    12.1     3.6    10.7
I/sigma                                        11.3    73.9     0.1    10.8
Rmerge(I)                                     0.056   0.038   1.857   0.056
Rmerge(I+/-)                                  0.055   0.038   1.802   0.055
Rmeas(I)                                      0.059   0.040   2.164   0.059
Rmeas(I+/-)                                   0.059   0.041   2.250   0.059
Rpim(I)                                       0.017   0.012   1.075   0.017
Rpim(I+/-)                                    0.023   0.015   1.329   0.023
CC half                                       0.999   0.999   0.240   0.999
Anomalous completeness                         92.0   100.0    41.9    81.0
Anomalous multiplicity                          5.9     7.0     2.2     5.8
Anomalous correlation                        -0.199  -0.284  -0.040  -0.272
Anomalous slope                               0.187                        
dF/F                                          0.036                        
dI/s(dI)                                      0.301                        
Total observations                           532820   33428    5365  538135
Total unique                                  48264    2770    1491   50514
```

as well as a better estimate for the resolution, if this is lower than the full extent of the data. Further up you will also see an analysis of the error model:

```
Error model details:
  Type: basic
  Parameters: a = 3.06517, b = 0.01062
  Error model formula: σ'² = a²(σ² + (bI)²)
  estimated I/sigma asymptotic limit: 30.733
```

which is very useful for basic diagnostics. This is immediately comparable with the ISa statistic from XDS. If you have a lot of anomalous signal the difference in error model between `anomalous=true` and `false` can be substantial, as it will be inflating the errors to account for the differences.

## Merging or Exporting

Most downstream software depends on a scaled _and merged_ data set e.g. for molecular replacement, so at the end of processing you can run

```
dials.export scaled.expt scaled.refl
```

to simply export the scaled reflections in MTZ format or

```
dials.merge scaled.expt scaled.refl
```

which will output a scaled and merged MTZ file. At this stage, adding the resolution limit proposed at the end of scaling may be appropriate.
