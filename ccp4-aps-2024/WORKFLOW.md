# Processing in Detail: Simple Insulin to Learn Workflow (CCP4 / APS 2024)

## Introduction

DIALS processing may be performed by either running the individual tools (spot finding, indexing, refinement, integration, symmetry, scaling, exporting to MTZ) or you can run `xia2`, which makes (hopefully) informed choices for you at each stage. In this tutorial we will run through each of the steps in turn, taking a look at the output as we go. We will also look at enforcing the correct lattice symmetry.

The aim of this tutorial is to introduce you to the tools, not teach about data processing - it is assumed you have some idea of the overall process from e.g. associated lectures. With the graphical tools, I am not making so much effort to explain the options as simply "playing" will give you a chance to learn your way around and also find the settings which work for you. Particularly with looking at diffraction images, the "best" settings are very personal.

## DIALS version

This tutorial assumes you are using [DIALS version 3.20 or later](https://dials.github.io/installation.html) and that you have this set up (i.e. you've sourced the setup file).

If you are running at home on Linux or macOS then you should be able to reproduce the results in here. If you are on Windows, try installing the Linux version in a WSL terminal using e.g. Ubuntu or using the version from CCP4, but be aware that there may be small differences in the output.

## Tutorial data

The following example uses cubic insulin collected on beamline i04-1 at Diamond Light Source: TODO upload to Zenodo and add a link. The purposes of this is _not_ to be an interesting data set, rather to show how the tools work when there are no problems as a preamble to processing more interesting data sets [in the main tutorial](./README.md).

## Files

DIALS creates two principal file types:

- experiment files called `something.expt`
- reflection files called `something.refl`

"Experiment" in DIALS has a very specific meaning - the capturing of data from one set of detector, beam, goniometer and crystal - so if you have two scans from one crystal this is two experiments, if you have two lattices on one data set this is two experiments. In most cases you can ignore this distinction though.

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
dials.import ../Insulin_6_2.nxs
```

will read the metadata from this `NeXus` file and write `imported.expt` from this. It is important to note that for well-behaved data (i.e. anything which is well-collected from a well-behaved sample) the commands below will often be identical after importing. The output from importing describes what was found: this should correspond to our expectations.

```
Ethics-Gradient work :) [main] $ cat dials.import.log 
DIALS (2018) Acta Cryst. D74, 85-97. https://doi.org/10.1107/S2059798317017235
DIALS 3.dev.953-g748efeb99
The following parameters have been modified:

input {
  experiments = <image files>
}

--------------------------------------------------------------------------------
  format: <class 'dxtbx.format.FormatNXmxDLS.FormatNXmxDLS'>
  template: /Users/graeme/data/i04-1-run3-ins/Insulin_6_2.nxs:1:1800
  num images: 1800
  sequences:
    still:    0
    sweep:    1
  num stills: 0
--------------------------------------------------------------------------------
Writing experiments to imported.expt
```

Once you have `imported.expt` you can, if you like, look at the content with `dials.show` as `dials.show imported.expt`. This is a general program in DIALS to allow you to print the current state of models, with output which looks like:

```
DIALS (2018) Acta Cryst. D74, 85-97. https://doi.org/10.1107/S2059798317017235
The following parameters have been modified:

input {
  experiments = imported.expt
}

Experiment 0:
Experiment identifier: af2eaa2f-7f6a-e188-464b-6adfde052baf
Image template: /Users/graeme/data/i04-1-run3-ins/Insulin_6_2.nxs
Detector:
Panel:
  name: /entry/instrument/detector/module
  type: SENSOR_PAD
  identifier: 
  pixel_size:{0.075,0.075}
  image_size: {3108,3262}
  trusted_range: {0,31881}
  thickness: 0.45
  material: Si
  mu: 3.27636
  gain: 1
  pedestal: 0
  fast_axis: {1,0,0}
  slow_axis: {0,-1,0}
  origin: {-108.3,120.975,-177.904}
  distance: 177.904
  pixel to millimeter strategy: ParallaxCorrectedPxMmStrategy
    mu: 3.27636
    t0: 0.45


Max resolution (at corners): 1.209174
Max resolution (inscribed):  1.701016

Beam:
    probe: x-ray
    wavelength: 0.918076
    sample to source direction : {0,0,1}
    divergence: 0
    sigma divergence: 0
    polarization normal: {0,1,0}
    polarization fraction: 0.999
    flux: 0
    transmission: 1
    sample to source distance: 0

Beam centre: 
    mm: (108.30,120.98)
    px: (1444.00,1613.00)

Scan:
    number of images:   1800
    image range:   {1,1800}
    epoch:    0
    exposure time:    0
    oscillation:   {252,0.2}

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

in this tool there are many settings you can adjust, which could depend on the source of the data and - most importantly - your preferences. Personally the author finds for basic inspection of the images stacking e.g. 5 images makes the lattice clearer for finely sliced images, and adjusting the brightness depending on how your data were collected:

![Image viewer](./images/image-view.png)

If the data are not stacked the spot finding process can also be explored - the controls at the bottom of the "Settings" window allow you to step through these and can be very useful for getting a "computer's eye view" of how the data look (particularly for establishing where the diffraction is visible to.)

## Find Spots

The first "real" task in any processing using DIALS is the spot finding. Since this is looking for spots on every image in the dataset, this process can take some time so by default will use all of the processors available in your machine - if you would like to control this adjust with e.g. `nproc=4` - however the default is usually sensible unless you are sharing the computer with many others.

```
dials.find_spots imported.expt
```

This is one of the two steps where every image in the data set is read and processed and hence can be moderately time-consuming. This contains a reflection file `strong.refl` which contains both the positions of the strong spots and also "images" of the spot pixels which we will use later. You can view these spots on top of the images with

```
dials.image_viewer imported.expt strong.refl
```

to get a sense of what spots were found. You will see that the spots are surrounded by little boxes - these are the _bounding boxes_ of the reflections i.e. the outer extent of the pixels that belong to that spot. The "signal" pixels are highlighted with green blobs giving a sense of what is and is not "strong."

![Image viewer](./images/image-view-spots.png)

The default parameters for spot finding usually do a good job for Pilatus or Eiger images, such as these. However they may not be optimal for data from other detector types, such as CCDs or image plates. Issues with  incorrectly set gain might, for example, lead to background noise being extracted as spots. You can use the image mode buttons to preview how the parameters affect the spot finding algorithm. The final button 'threshold’ is the one on which spots were found, so ensuring this produces peaks at real diffraction spot positions will give the best chance of success.

The second tool for visualisation of the found spots is the reciprocal lattice viewer - which presents a view of the spot positions mapped to reciprocal space.

```
dials.reciprocal_lattice_viewer imported.expt strong.refl
```

No matter the sample orientation you should be able to rotate the space to "look down" the lines of reflections. If you cannot, or the lines are not straight, it is likely that there are some errors in the experiment parameters e.g. detector distance or beam centre. If these are not too large they will likely be corrected in the subsequent analysis.

![Reciprocal viewer](./images/reciprocal-lattice.png)

Have a play with the settings - you can change the beam centre in the viewer to see how nicely aligned spots move out of alignment. Some of the options will only work after you have indexed the data. If the geometry is not accurately recorded you may find it useful to run:

```
dials.search_beam_position imported.expt strong.refl
```

to determine an updated position for the beam centre - ideally the shift that this calculates should be small if the beamline is well-calibrated - if it is a couple of mm or more it may be worth discussing this with the beamline staff! Running the reciprocal lattice viewer with the optimised experiment output:

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
model 1 (129747 reflections):
Crystal:
    Unit cell: 67.3031(14), 67.3035(14), 67.3293(14), 109.4796(4), 109.4814(4), 109.4312(4)
    Space group: P 1
    U matrix:  {{ 0.5947,  0.8039,  0.0044},
                { 0.1567, -0.1105, -0.9815},
                {-0.7885,  0.5844, -0.1916}}
    B matrix:  {{ 0.0149,  0.0000,  0.0000},
                { 0.0052,  0.0158,  0.0000},
                { 0.0091,  0.0091,  0.0182}}
    A = UB:    {{ 0.0131,  0.0127,  0.0001},
                {-0.0072, -0.0107, -0.0179},
                {-0.0104,  0.0075, -0.0035}}
+------------+-------------+---------------+-------------+
|   Imageset |   # indexed |   # unindexed |   % indexed |
|------------+-------------+---------------+-------------|
|          0 |      129747 |          2621 |          98 |
+------------+-------------+---------------+-------------+
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
  
During this process an effort is made to eliminate "outlier" reflections - these are reflections which do not strictly belong to the crystal lattice but are accidentally close to a reciprocal space position and hence can be indexed. Most often this is an issue with small satellite lattices or ice / powder on the sample. Usually this should not be a cause for concern.

## Bravais Lattice Determination (optional!)

Once you have indexed the data you may optionally attempt to infer the correct Bravais lattice and assign this to constrain the unit cell in subsequent processing. If, for example, the unit cell from indexing has all three angles close to 90° and two unit cell lengths with very similar values you could guess that the unit cell is tetragonal. In `dials.refine_bravais_settings` we take away the guesswork by transforming the unit cell to all possible Bravais lattices which approximately match the triclinic unit cell, and then performing some refinement - if the lattice constraints are correct then imposing them should have little impact on the deviations between the observed and calculated reflection positions (known as the R.M.S. deviations). If a lattice constraint is incorrect it will manifest as a significant increase in a deviation - however care must be taken as it can be the case that the true _symmetry_ is lower than the shape of the unit cell would indicate.

In the general case there is little harm in skipping this step, however for information if you run

```
dials.refine_bravais_settings indexed.expt indexed.refl
```

you will see a table of possible unit cell / Bravais lattice / R.M.S. deviations printed in the output - in the case of this tutorial data they will all match, as the true symmetry is cubic.

```
Chiral space groups corresponding to each Bravais lattice:
aP: P1
oF: F222
oI: I222 I212121
tI: I4 I41 I422 I4122
hR: R3:H R32:H
cI: I23 I213 I432 I4132
mI: I2
+------------+--------------+--------+--------------+----------+-----------+-------------------------------------------+----------+-------------------+
|   Solution |   Metric fit |   rmsd | min/max cc   |   #spots | lattice   | unit_cell                                 |   volume | cb_op             |
|------------+--------------+--------+--------------+----------+-----------+-------------------------------------------+----------+-------------------|
|   *     22 |       0.0384 |  0.041 | 0.779/0.968  |    36000 | cI        | 77.79  77.79  77.79  90.00  90.00  90.00  |   470650 | b+c,a+c,a+b       |
|   *     21 |       0.0372 |  0.04  | 0.781/0.799  |    36000 | hR        | 110.01 110.01  67.35  90.00  90.00 120.00 |   705911 | a+2*b+c,-b+c,a    |
|   *     20 |       0.0384 |  0.04  | 0.779/0.796  |    36000 | hR        | 110.01 110.01  67.35  90.00  90.00 120.00 |   705811 | a+b+2*c,a-c,b     |
|   *     19 |       0.0384 |  0.041 | 0.779/0.797  |    36000 | hR        | 110.00 110.00  67.37  90.00  90.00 120.00 |   705895 | 2*a+b+c,-a+b,c    |
|   *     18 |       0.0338 |  0.04  | 0.779/0.796  |    36000 | hR        | 109.98 109.98  67.37  90.00  90.00 120.00 |   705788 | b-c,-a+c,a+b+c    |
|   *     17 |       0.0375 |  0.039 | 0.622/0.968  |    36000 | tI        | 77.71  77.71  77.74  90.00  90.00  90.00  |   469501 | b+c,a+c,a+b       |
|   *     16 |       0.0375 |  0.04  | 0.505/0.957  |    36000 | tI        | 77.77  77.77  77.75  90.00  90.00  90.00  |   470209 | a+b,b+c,a+c       |
|   *     15 |       0.0384 |  0.04  | 0.491/0.962  |    36000 | tI        | 77.77  77.77  77.75  90.00  90.00  90.00  |   470272 | a+c,a+b,b+c       |
|   *     14 |       0.0375 |  0.039 | 0.957/0.968  |    36000 | oI        | 77.71  77.71  77.75  90.00  90.00  90.00  |   469516 | -a-c,b+c,a+b      |
|   *     13 |       0.0375 |  0.04  | 0.504/0.957  |    36000 | oF        | 77.75 109.98 109.99  90.00  90.00  90.00  |   940536 | -a-c,-a+c,a+2*b+c |
|   *     12 |       0.0384 |  0.04  | 0.491/0.962  |    36000 | oF        | 77.75 109.98 109.99  90.00  90.00  90.00  |   940547 | b+c,-b+c,2*a+b+c  |
|   *     11 |       0.0375 |  0.039 | 0.957/0.957  |    36000 | mI        | 77.72  77.72  77.75  90.00  90.00  90.00  |   469594 | -b-c,-a-c,a+b     |
|   *     10 |       0.0331 |  0.039 | 0.504/0.504  |    36000 | mI        | 67.33 109.99  67.36  90.00 109.49  90.00  |   470295 | b,a-c,-a-b-c      |
|   *      9 |       0.0375 |  0.039 | 0.962/0.962  |    36000 | mI        | 77.72  77.72  77.75  90.00  90.00  90.00  |   469683 | a+c,b+c,-a-b      |
|   *      8 |       0.0338 |  0.039 | 0.493/0.493  |    36000 | mI        | 67.33 109.98  67.36  90.00 109.49  90.00  |   470288 | a,-b+c,-a-b-c     |
|   *      7 |       0.0372 |  0.04  | 0.507/0.507  |    36000 | mI        | 67.33 109.99  67.35  90.00 109.49  90.00  |   470261 | -a,a+2*b+c,-c     |
|   *      6 |       0.0384 |  0.04  | 0.491/0.491  |    36000 | mI        | 67.34 109.99  67.35  90.00 109.48  90.00  |   470283 | -b,-2*a-b-c,-c    |
|   *      5 |       0.006  |  0.037 | 0.633/0.968  |    36000 | oF        | 77.75 109.87 109.94  90.00  90.00  90.00  |   939123 | a+b,-a+b,a+b+2*c  |
|   *      4 |       0.0059 |  0.037 | 0.968/0.968  |    36000 | mI        | 77.72  77.75  77.72  90.00  90.04  90.00  |   469625 | -a-c,-a-b,b+c     |
|   *      3 |       0.0014 |  0.037 | 0.633/0.633  |    36000 | mI        | 67.32 109.87  67.33  90.00 109.47  90.00  |   469594 | c,-a+b,-a-b-c     |
|   *      2 |       0.006  |  0.037 | 0.635/0.635  |    36000 | mI        | 67.30 109.94  67.30  90.00 109.43  90.00  |   469555 | -a,-a-b-2*c,-b    |
|   *      1 |       0      |  0.037 | -/-          |    36000 | aP        | 67.30  67.30  67.33 109.48 109.48 109.43  |   234799 | a,b,c             |
+------------+--------------+--------+--------------+----------+-----------+-------------------------------------------+----------+-------------------+
```

If you wish to use one of the output experiments from this process e.g. `bravais_setting_22.expt` you will need to reindex the reflection data from indexing to match this - we do not output every option of reindexed data as these files can be large. In most cases it is simpler to re-run `dials.index` setting the chosen space group.

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
|     0 |  36000 |  0.32955 |  0.37266 |    0.39759 |
+-------+--------+----------+----------+------------+
```

to:

```
RMSDs by experiment:
+-------+--------+----------+----------+------------+
|   Exp |   Nref |   RMSD_X |   RMSD_Y |     RMSD_Z |
|    id |        |     (px) |     (px) |   (images) |
|-------+--------+----------+----------+------------|
|     0 | 110887 |  0.21138 |  0.19914 |    0.21174 |
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

Before the data may be scaled it is necessary that the crystal symmetry is known - if this was assigned correctly at indexing e.g. `space_group=I213` then you can proceed directly to scaling. In the majority of cases however it will be unknown or not set at this point, so needs to be assigned between integration and scaling. Even if the Bravais lattice was assigned earlier, the correct symmetry _within_ that lattice is needed.

The symmetry analysis in DIALS takes the information from the spot positions and also the spot intensities. The former are used to effectively re-run `dials.refine_bravais_settings` to identify possible lattices and hence candidate symmetry operations, and the latter are used to assess the presence or absence of these symmetry operations. Once the operations are found, the crystal rotational symmetry is assigned by composing these operations into a putative space group. In addition, systematically absent reflections are also assessed to assign a best guess to translational elements of the symmetry - though these are not needed for scaling, they may help with downstream analysis rather than you having to manually identify them.

```
dials.symmetry integrated.expt integrated.refl
```

is how this step is run. At this point it is important to note that the program is trying to identify all symmetry elements, and does not know that e.g. inversion centres are not possible - so for an oP lattice it will be testing for P/mmm symmetry which corresponds to P2?2?2? in standard MX.

In the output you'll see first the individual symmetry operation:

```
Scoring individual symmetry elements

+--------------+--------+------+--------+-----+---------------+
|   likelihood |   Z-CC |   CC |      N |     | Operator      |
|--------------+--------+------+--------+-----+---------------|
|        0.903 |   9.83 | 0.98 | 172280 | *** | 1 |(0, 0, 0)  |
|        0.148 |   4.35 | 0.44 | 341088 |     | 4 |(1, 1, 0)  |
|        0.15  |   4.39 | 0.44 | 332088 |     | 4 |(1, 0, 1)  |
|        0.15  |   4.4  | 0.44 | 332022 |     | 4 |(0, 1, 1)  |
|        0.904 |   9.75 | 0.97 | 332526 | *** | 3 |(1, 0, 0)  |
|        0.904 |   9.74 | 0.97 | 332464 | *** | 3 |(0, 1, 0)  |
|        0.904 |   9.75 | 0.98 | 332462 | *** | 3 |(0, 0, 1)  |
|        0.904 |   9.74 | 0.97 | 332444 | *** | 3 |(1, 1, 1)  |
|        0.903 |   9.84 | 0.98 | 170444 | *** | 2 |(1, 1, 0)  |
|        0.156 |   4.5  | 0.45 | 169708 |     | 2 |(-1, 1, 0) |
|        0.905 |   9.64 | 0.96 | 170348 | *** | 2 |(1, 0, 1)  |
|        0.15  |   4.39 | 0.44 | 166058 |     | 2 |(-1, 0, 1) |
|        0.905 |   9.63 | 0.96 | 169936 | *** | 2 |(0, 1, 1)  |
|        0.15  |   4.38 | 0.44 | 166076 |     | 2 |(0, -1, 1) |
|        0.154 |   4.47 | 0.45 | 171232 |     | 2 |(1, 1, 2)  |
|        0.15  |   4.39 | 0.44 | 166076 |     | 2 |(1, 2, 1)  |
|        0.151 |   4.4  | 0.44 | 166030 |     | 2 |(2, 1, 1)  |
+--------------+--------+------+--------+-----+---------------+
```

Which shows clear 2 and 3 fold symmetry but no 4-fold symmetry. This will prove to be important in the main tutorial as this creates ambiguity. These are followed by the results of composing these into the possible space groups and the likelihood assessment of these - which takes into consideration the elements present in the space group and also those not present:

```
Scoring all possible sub-groups

+-------------------+-----+--------------+----------+--------+--------+------+-------+---------+--------------------+
| Patterson group   |     |   Likelihood |   NetZcc |   Zcc+ |   Zcc- |   CC |   CC- |   delta | Reindex operator   |
|-------------------+-----+--------------+----------+--------+--------+------+-------+---------+--------------------|
| I m -3            | *** |            1 |     5.33 |   9.74 |   4.41 | 0.97 |  0.44 |       0 | b+c,a+c,a+b        |
| I m m m           |     |            0 |     3.2  |   9.73 |   6.53 | 0.97 |  0.65 |       0 | -a-c,b+c,a+b       |
| I 1 2/m 1         |     |            0 |     2.69 |   9.73 |   7.04 | 0.97 |  0.68 |       0 | a+c,b+c,-a-b       |
| I 1 2/m 1         |     |            0 |     2.69 |   9.73 |   7.04 | 0.97 |  0.68 |       0 | -b-c,-a-c,a+b      |
| R -3 :H           |     |            0 |     2.75 |   9.78 |   7.03 | 0.98 |  0.66 |       0 | a+b+2*c,a-c,b      |
| R -3 :H           |     |            0 |     2.75 |   9.79 |   7.03 | 0.98 |  0.66 |       0 | b-c,-a+c,a+b+c     |
| R -3 :H           |     |            0 |     2.75 |   9.79 |   7.03 | 0.98 |  0.66 |       0 | a+2*b+c,-b+c,a     |
| R -3 :H           |     |            0 |     2.76 |   9.79 |   7.03 | 0.98 |  0.66 |       0 | 2*a+b+c,-a+b,c     |
| I 1 2/m 1         |     |            0 |     2.81 |   9.83 |   7.03 | 0.98 |  0.68 |       0 | -a-c,-a-b,b+c      |
| I 4/m m m         |     |            0 |     0.87 |   7.91 |   7.04 | 0.7  |  0.7  |       0 | b+c,a+c,a+b        |
| I 4/m m m         |     |            0 |     0.85 |   7.9  |   7.05 | 0.7  |  0.7  |       0 | a+c,a+b,b+c        |
| I 4/m m m         |     |            0 |     0.85 |   7.9  |   7.05 | 0.7  |  0.7  |       0 | a+b,b+c,a+c        |
| I 4/m             |     |            0 |     1.14 |   8.34 |   7.2  | 0.7  |  0.7  |       0 | a+c,a+b,b+c        |
| I 4/m             |     |            0 |     1.15 |   8.34 |   7.2  | 0.7  |  0.7  |       0 | a+b,b+c,a+c        |
| I 4/m             |     |            0 |     1.23 |   8.41 |   7.18 | 0.71 |  0.7  |       0 | b+c,a+c,a+b        |
| I m -3 m          |     |            0 |     7.41 |   7.41 |   0    | 0.7  |  0    |       0 | b+c,a+c,a+b        |
| P -1              |     |            0 |     2.59 |   9.83 |   7.23 | 0.98 |  0.69 |       0 | a,b,c              |
| F m m m           |     |            0 |     0.3  |   7.64 |   7.34 | 0.71 |  0.7  |       0 | a+b,-a+b,a+b+2*c   |
| F m m m           |     |            0 |     0.18 |   7.55 |   7.37 | 0.7  |  0.7  |       0 | b+c,-b+c,2*a+b+c   |
| F m m m           |     |            0 |     0.18 |   7.55 |   7.37 | 0.7  |  0.7  |       0 | -a-c,-a+c,a+2*b+c  |
| I 1 2/m 1         |     |            0 |     0.26 |   7.64 |   7.38 | 0.72 |  0.7  |       0 | c,-a+b,-a-b-c      |
| I 1 2/m 1         |     |            0 |     0.25 |   7.63 |   7.38 | 0.71 |  0.7  |       0 | -a,-a-b-2*c,-b     |
| I 1 2/m 1         |     |            0 |     0.23 |   7.61 |   7.38 | 0.71 |  0.7  |       0 | -b,-2*a-b-c,-c     |
| I 1 2/m 1         |     |            0 |     0.23 |   7.61 |   7.38 | 0.71 |  0.7  |       0 | b,a-c,-a-b-c       |
| I 1 2/m 1         |     |            0 |     0.23 |   7.61 |   7.38 | 0.71 |  0.7  |       0 | -a,a+2*b+c,-c      |
| I 1 2/m 1         |     |            0 |     0.23 |   7.61 |   7.38 | 0.71 |  0.7  |       0 | a,-b+c,-a-b-c      |
| R -3 m :H         |     |            0 |    -0.47 |   7.08 |   7.55 | 0.71 |  0.7  |       0 | 2*a+b+c,-a+b,c     |
| R -3 m :H         |     |            0 |    -0.47 |   7.08 |   7.55 | 0.71 |  0.7  |       0 | b-c,-a+c,a+b+c     |
| R -3 m :H         |     |            0 |    -0.48 |   7.07 |   7.55 | 0.7  |  0.7  |       0 | a+b+2*c,a-c,b      |
| R -3 m :H         |     |            0 |    -0.48 |   7.07 |   7.55 | 0.7  |  0.7  |       0 | a+2*b+c,-b+c,a     |
+-------------------+-----+--------------+----------+--------+--------+------+-------+---------+--------------------+

Best solution: I m -3
Unit cell: 77.727, 77.727, 77.727, 90.000, 90.000, 90.000
Reindex operator: b+c,a+c,a+b
Laue group probability: 1.000
Laue group confidence: 1.000
```

Here the symmetry appears to be `I m -3` i.e. 3-fold rotation and three 2-fold mirror axes - and corresponds to some variation of `I2?3` - this information is sufficient for scaling though for structure solution identification of the correct space group is necessary - `dials.symmetry` will also attempt to guess this but in this case it is impossible to see the difference as the screw axes are masked by the centring operation.

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
High resolution limit                           1.38    3.74    1.38    1.20
Low resolution limit                           54.96   55.00    1.40   54.96
Completeness                                   94.8   100.0    64.1    74.7
Multiplicity                                   38.0    40.0    23.5    34.4
I/sigma                                        20.1   108.2     0.4    17.0
Rmerge(I)                                     0.089   0.038   3.580   0.091
Rmerge(I+/-)                                  0.088   0.037   3.489   0.090
Rmeas(I)                                      0.090   0.038   3.659   0.092
Rmeas(I+/-)                                   0.090   0.038   3.644   0.092
Rpim(I)                                       0.014   0.006   0.727   0.015
Rpim(I+/-)                                    0.020   0.008   1.015   0.020
CC half                                       1.000   0.999   0.269   1.000
Anomalous completeness                         94.8   100.0    64.7    73.8
Anomalous multiplicity                         19.8    22.1    12.0    17.9
Anomalous correlation                         0.148   0.231  -0.044   0.188
Anomalous slope                               0.667                        
dF/F                                          0.038                        
dI/s(dI)                                      0.723                        
Total observations                           586945   34847   12553  629390
Total unique                                  15431     871     534   18292
```

as well as a better estimate for the resolution, if this is lower than the full extent of the data. Further up you will also see an analysis of the error model:

```
Error model details:
  Type: basic
  Parameters: a = 0.90579, b = 0.03820
  Error model formula: σ'² = a²(σ² + (bI)²)
  estimated I/sigma asymptotic limit: 28.900
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
