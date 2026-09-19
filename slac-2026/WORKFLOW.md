# Processing in Detail: Simple Insulin to Learn Workflow (SLAC 2026)

## Introduction

DIALS processing may be performed by either running the individual tools (spot finding, indexing, refinement, integration, symmetry, scaling, exporting to MTZ) or you can run `xia2`, which makes (hopefully) informed choices for you at each stage. In this tutorial we will run through each of the steps in turn using the **DIALS Workflow GUI**, taking a look at the output as we go. We will also look at enforcing the correct lattice symmetry.

The GUI is a thin layer over the standard DIALS command-line programs: each step in the pipeline has a panel where you set a small number of parameters, and the GUI builds and runs the corresponding `dials.something` command for you. The command it is about to run is always shown in blue under **Command**, so everything you do here can be reproduced later from a terminal, and the log files are exactly the same as you would get from the command line.

The aim of this tutorial is to introduce you to the tools, not teach about data processing - it is assumed you have some idea of the overall process from e.g. associated lectures. With the graphical tools, I am not making so much effort to explain the options as simply "playing" will give you a chance to learn your way around and also find the settings which work for you. Particularly with looking at diffraction images, the "best" settings are very personal.

## DIALS version

This tutorial assumes you are using [DIALS version 3.20 or later](https://dials.github.io/installation.html) and that you have this set up (i.e. you've sourced the setup file). The screenshots in this tutorial were taken with DIALS 3.30.

If you are running at home on Linux or macOS then you should be able to reproduce the results in here. If you are on Windows, try installing the Linux version in a WSL terminal using e.g. Ubuntu or using the version from CCP4, but be aware that there may be small differences in the output.

## Tutorial data

If you are at the workshop then the data are already on disk at:

```
/dls/i04/data/2024/mx39148-1/tutorial_data/workflow
```

So replace `../data` or whatever with that. If you are doing this on your own computer, or you are at home, or not part of the workshop then you need to follow these instructions.

The following example uses [cubic insulin collected on beamline i04 at Diamond Light Source](https://zenodo.org/records/8376818): this was collected with a large beam, depositing ~ 1MGy / scan of dose on the sample. To speed things up, you can run with just a subset of the data rather than a full sweep or all four data sets. The purposes of this is _not_ to be an interesting data set, rather to show how the tools work when there are no problems as a preamble to processing more interesting data sets [in the main tutorial](../ccp4-dls-2024/README.md). If you have all the time in the world you can process all four together with only a minor change at the import step.

Fetching the data can be performed by writing a file containing

```
https://zenodo.org/records/8376818/files/ins10_1.nxs
https://zenodo.org/records/8376818/files/ins10_1_000001.h5
https://zenodo.org/records/8376818/files/ins10_1_000002.h5
https://zenodo.org/records/8376818/files/ins10_1_000003.h5
https://zenodo.org/records/8376818/files/ins10_1_000004.h5
https://zenodo.org/records/8376818/files/ins10_1_master.h5
https://zenodo.org/records/8376818/files/ins10_1_meta.h5
```

then:

```
wget -i file.list
```

## Starting the GUI

<!-- TODO: confirm the exact launch command / installation instructions for the DIALS Workflow GUI -->

With DIALS set up in your terminal, launch the DIALS Workflow GUI. Before doing anything else, set the **Working directory** at the top of the window to an empty directory where you want the processing output to go (type the path or use **Browse...**). Every step writes its files into this directory, and the GUI looks there for the input files of the next step. The green **DIALS found on $PATH** label confirms that the GUI can see your DIALS installation.

![DIALS Workflow GUI main window](./images/gui-main-window.png)

The window has three parts:

- **Pipeline steps** down the left hand side - the processing steps in the order you will usually run them. The check box next to each step is ticked once that step has run successfully in the current working directory.
- **Viewing tools** below them - buttons which launch `dials.show`, `dials.image_viewer`, `dials.reciprocal_lattice_viewer` and `dials.report` on the files of your choice.
- The main panel on the right, with tabs for **Setup / Run** (a short description of the step, the input files, the parameters and the **Run** button), **Live Output** (the terminal output of the program as it runs), **Summary** (the key tables pulled out of the log once the step is finished), **Full Log** (the complete `dials.program.log` file) and, for some steps, **Plots**.

If you close the GUI and come back later, set the working directory again and click **Load state from working dir** - the GUI will work out which steps have already been run from the files it finds there.

## Files

DIALS creates two principal file types:

- experiment files called `something.expt`
- reflection files called `something.refl`

"Experiment" in DIALS has a very specific meaning - the capturing of data from one set of detector, beam, goniometer and crystal - so if you have two scans from one crystal this is two experiments, if you have two lattices on one data set this is two experiments. In most cases you can ignore this distinction though.

Usually the output filenames will correspond to the name of the DIALS program that created them e.g. `indexed.refl` and `indexed.expt` from `dials.index`. The only deviations from this are on import (see below) where we are only reading experiment models and spot finding where we find _strong_ reflections so write these to `strong.refl` - and we create no models so (by default) there is no output experiment file.

The GUI fills in the **Experiment file** and **Reflection file** fields of each step with the output of the previous step, so in the straightforward case you never need to type a filename. You can, however, edit these fields if you want to e.g. feed the `optimised.expt` from the beam centre search into indexing.

At any time you can _look_ at these files with the **dials.show** button under Viewing tools, which will summarise the content of the files. You can also show reflection files, which gives a tabular summary of the content, but this can be rather slow, as the data are much more substantial.

[If you're impatient...](../ccp4-dls-2024/TLDR.md) - as a note this is essentially the script I would use to have a first look at any data set where I expected the experiment metadata (wavelength, beam centre etc.) to be correct.

## Parameters

All DIALS programs accept parameters in the form of `parameter=value`. The GUI exposes the handful of parameters you are most likely to want for each step as labelled fields, and anything else can be typed into the **Additional parameters (free text)** box exactly as you would on the command line, e.g. `index_assignment.method=local`. Whatever you type is appended to the command shown in blue.

If you are looking for an option, all of the DIALS programs support

```
dials.program -c -e2
```

from a terminal, which will show you all possible configuration options, so e.g.

```
dials.index -c -e2 | less
```

will allow you to scroll through the extensive list of options you can adjust. In most cases the defaults are relatively sensible for synchrotron data from a pixel array detector, as we are using in this tutorial.

## Output

In the majority of cases the `dials` programs write their output to `dials.program.log` e.g. `dials.find_spots.log` etc. in the working directory - everything which is printed to the **Live Output** tab is also saved in this file, so you can review the processing later. The **Full Log** tab shows this file (click **Refresh from log file** if the step has just finished). In the case where you are reporting an issue to the developers including these log files in the error report (particularly for the step which failed) is very helpful.

From most stages you can generate a detailed report of the current state of processing by clicking **Run and show report in web browser** instead of the plain **Run** button - this runs the step and then `dials.report` on its output, and opens the resulting HTML in your browser. The **dials.report** button under Viewing tools does the same for any pair of files you choose.

## Import

The starting point for any processing with DIALS is to _import_ the data - here the metadata are read and a description of the data to be processed saved to a file named `imported.expt`. This is "human readable" in that the file is JSON format (roughly readable text with brackets around to structure for computers). While you can edit this file if you know what you are doing, usually this is not necessary.

Click **1. Import** in the pipeline steps. Click **Browse files...** and select the `ins10_1.nxs` file (for NeXus / HDF5 data you select the master or `.nxs` file, not the individual `_000001.h5` data files; for a directory of `.cbf` images you would instead use **Add glob pattern...** with e.g. `X14_1_*.cbf.gz`).

![Selecting the master file](./images/gui-import-file-dialog.png)

For this tutorial I am only processing the first 1200 images, so type `1,1200` into the **Image range (start,end)** field. Leave it blank to use all of the images. The command shown in blue updates as you change the fields:

![Import setup](./images/gui-import-setup.png)

Now click **Run dials.import**. The output appears in the **Live Output** tab and describes what was found: this should correspond to our expectations.

```
DIALS (2018) Acta Cryst. D74, 85-97. https://doi.org/10.1107/S2059798317017235
DIALS 3.dev.1215-gb54762037
The following parameters have been modified:

input {
  experiments = <image files>
}
geometry {
  scan {
    image_range = 1 1200
  }
}


Applying input geometry in the following order:
  1. Manual geometry

--------------------------------------------------------------------------------
  format: <class 'dxtbx.format.FormatNXmxDLS16M.FormatNXmxDLS16M'>
  template: /Users/graeme/data/i04-ins-1MGy/ins10_1.nxs:1:1200
  num images: 1200
  sequences:
    still:    0
    sweep:    1
  num stills: 0
--------------------------------------------------------------------------------
Writing experiments to imported.expt
```

You will see that the log file includes the additional parameters passed in, which is useful for tracing the processing options used and in this case confirms that we have read ~1200 images. It is important to note that for well-behaved data (i.e. anything which is well-collected from a well-behaved sample) the steps below will often be run with no changes to the defaults after importing.

Once you have `imported.expt` you can, if you like, look at the content by clicking **dials.show** under Viewing tools. This is a general program in DIALS to allow you to print the current state of models, with output which looks like:

```
Experiment 0:
Experiment identifier: 82dbf00d-4836-aded-b32f-c1789f2de707
Image template: /Users/graeme/data/i04-ins-1MGy/ins10_1.nxs
Detector:
Panel:
  name: /entry/instrument/detector/module
  type: SENSOR_PAD
  identifier: 
  pixel_size:{0.075,0.075}
  image_size: {4148,4362}
  trusted_range: {0,33005}
  thickness: 0.45
  material: Si
  mu: 3.66309
  gain: 1
  pedestal: 0
  fast_axis: {1,0,0}
  slow_axis: {0,-1,0}
  origin: {-159.08,166.6,-170}
  distance: 170
  pixel to millimeter strategy: ParallaxCorrectedPxMmStrategy
    mu: 3.66309
    t0: 0.45


Max resolution (at corners): 1.058512
Max resolution (inscribed):  1.337295

Beam:
    probe: x-ray
    wavelength: 0.953738
    sample to source direction : {0,0,1}
    divergence: 0
    sigma divergence: 0
    polarization normal: {0,1,0}
    polarization fraction: 0.999
    flux: 0
    transmission: 1
    sample to source distance: 0

Beam centre: 
    mm: (159.08,166.60)
    px: (2121.07,2221.33)

Scan:
    number of images:   1200
    image range:   {1,1200}
    epoch:    0
    exposure time:    0
    oscillation:   {0,0.1}

Goniometer:
    Rotation axis:   {1,0,0}
    Fixed rotation:  {1,0,0,0,1,0,0,0,1}
    Setting rotation:{1,0,0,0,1,0,0,0,1}
    Axis #0 (phi):  {1,-0.0037,0.002}
    Axis #1 (chi):  {-0.0046,0.0372,-0.9993}
    Axis #2 (omega):  {1,0,0}
    Angles: 0,0,0
    scan axis: #2 (omega)    
```

I recognise that this is quite "computer" in the way that the numbers are presented, but there are a few useful things you can look for in here: does the wavelength, distance, beam centre look OK? Are the number of images what you would expect? If the beam centre, distance or wavelength look wrong here, fix them before going further (the **Additional parameters** box on the import panel accepts e.g. `distance=160`) - nothing else happens at this stage, so it is cheap to re-run.

At this point you can also look at the images by clicking **dials.image_viewer** under Viewing tools and giving it `imported.expt` (leave the reflection file blank). In this tool there are many settings you can adjust, which could depend on the source of the data and - most importantly - your preferences. Personally the author finds for basic inspection of the images stacking e.g. 10 images makes the lattice clearer for finely sliced images, and adjusting the brightness depending on how your data were collected:

![Image viewer](../ccp4-dls-2024/images/image-view.png)

If the data are not stacked the spot finding process can also be explored - the controls at the bottom of the "Settings" window allow you to step through these and can be very useful for getting a "computer's eye view" of how the data look (particularly for establishing where the diffraction is visible to.)

If you have the time and interest to download all four data sets from the deposition above, you can import all four at once by selecting all four `.nxs` files in the file dialog, or with **Add glob pattern...** and `../ins10_?.nxs`. Then proceed through the entire tutorial with _all four sweeps_ - note though that this is only possible without changing the defaults as the data were taken from a single sample, with the goniometer rotations correctly recorded. [The main tutorial](../ccp4-dls-2024/README.md) covers what to do if this is not the case.

Once the step has finished, the check box next to **1. Import** is ticked and the GUI moves on to the next step.

## Find Spots

The first "real" task in any processing using DIALS is the spot finding. Since this is looking for spots on every image in the dataset, this process can take some time so by default will use all of the processors available in your machine - if you would like to control this set the **nproc** field - however the default is usually sensible unless you are sharing the computer with many others.

Click **2. Find Spots**. The **Experiment file** is already set to `imported.expt` from the previous step, so simply click **Run dials.find_spots**.

![Find spots setup](./images/gui-find-spots-setup.png)

This is one of the two steps where every image in the data set is read and processed and hence can be moderately time-consuming. You can follow its progress in the **Live Output** tab, and if you need to abandon it the **Stop** button is enabled while a step is running.

![Find spots running](./images/gui-find-spots-live-output.png)

The output is a reflection file `strong.refl` which contains both the positions of the strong spots and also "images" of the spot pixels which we will use later. You can view these spots on top of the images by clicking **dials.image_viewer** under Viewing tools - a small dialog asks for the experiment file (`imported.expt`) and, optionally, the reflection file (`strong.refl`) - then **Launch**.

![Image viewer with strong spots](./images/gui-image-viewer-spots.png)

You will see that the spots are surrounded by little boxes - these are the _bounding boxes_ of the reflections i.e. the outer extent of the pixels that belong to that spot. The "signal" pixels are highlighted giving a sense of what is and is not "strong." Have a play with the settings panel on the right - zoom level, brightness and colour scheme in particular - to find what works for you.

The default parameters for spot finding usually do a good job for Pilatus or Eiger images, such as these. However they may not be optimal for data from other detector types, such as CCDs or image plates. Issues with incorrectly set gain might, for example, lead to background noise being extracted as spots. You can use the image mode buttons and the **Threshold algorithm** / **Sigma background** / **Sigma strong** settings in the image viewer to preview how the parameters affect the spot finding algorithm. The "threshold" view is the one on which spots were found, so ensuring this produces peaks at real diffraction spot positions will give the best chance of success. Any parameters you settle on can be typed into the **Additional parameters** box on the Find Spots panel and the step re-run.

The second tool for visualisation of the found spots is the reciprocal lattice viewer - which presents a view of the spot positions mapped to reciprocal space. Click **dials.reciprocal_lattice_viewer** under Viewing tools and give it `imported.expt` and `strong.refl`.

No matter the sample orientation you should be able to rotate the space to "look down" the lines of reflections. If you cannot, or the lines are not straight, it is likely that there are some errors in the experiment parameters e.g. detector distance or beam centre. If these are not too large they will likely be corrected in the subsequent analysis.

![Reciprocal lattice viewer](./images/gui-reciprocal-lattice-viewer.png)

Have a play with the settings - you can change the beam centre in the viewer to see how nicely aligned spots move out of alignment. Some of the options will only work after you have indexed the data.

If the geometry is not accurately recorded you may find it useful to run the optional step **3. Search Beam Position (optional)**. This takes `imported.expt` and `strong.refl` and writes an `optimised.expt` with an updated position for the beam centre.

![Search beam position](./images/gui-search-beam-position.png)

Ideally the shift that this calculates should be small if the beamline is well-calibrated - if it is a couple of mm or more it may be worth discussing this with the beamline staff! Running the reciprocal lattice viewer with `optimised.expt` and `strong.refl` should show straight lines, provided everything has worked correctly. For this data set the step is not needed, but it does no harm.

## Indexing

The next step will be indexing of the found spots with `dials.index` - by default this uses a 3D FFT algorithm to identify periodicity in the reciprocal space mapped spot positions, though there are other algorithms available which can be better suited to e.g. narrow data sets.

Click **4. Index**. The input files default to `imported.expt` and `strong.refl`; if you ran the beam position search and want to use its result, change the experiment file to `optimised.expt`.

![Index setup](./images/gui-index-setup.png)

The most common parameters to set are the **space_group** and **unit_cell** if these are known in advance - here we leave both blank. The two check boxes at the top of the parameters are for the multi-crystal and multi-sweep cases covered in the [Cows / Pigs / People](./COWS_PIGS_PEOPLE.md) tutorial and can be ignored for now. Click **Run dials.index**.

While this does index the data it will also perform some refinement with a static crystal model, and indicate in the output the fraction of reflections which have been indexed - ideally this should be close to 100%:

```
Refined crystal models:
model 1 (52907 reflections):
Crystal:
    Unit cell: 67.4575(12), 67.4621(13), 67.5064(10), 109.4906(6), 109.5223(5), 109.4697(5)
    Space group: P 1
    U matrix:  {{ 0.2465,  0.5564, -0.7935},
                { 0.9448, -0.3204,  0.0689},
                {-0.2159, -0.7667, -0.6046}}
    B matrix:  {{ 0.0148,  0.0000,  0.0000},
                { 0.0052,  0.0157,  0.0000},
                { 0.0091,  0.0091,  0.0182}}
    A = UB:    {{-0.0007,  0.0015, -0.0144},
                { 0.0130, -0.0044,  0.0013},
                {-0.0127, -0.0176, -0.0110}}
+------------+-------------+---------------+-------------+
|   Imageset |   # indexed |   # unindexed |   % indexed |
|------------+-------------+---------------+-------------|
|          0 |       52907 |          2522 |        95.5 |
+------------+-------------+---------------+-------------+
```

![Index output and launching the image viewer](./images/gui-index-output-image-viewer.png)

If it is significantly less than 100% it is possible you have a second lattice - setting **max_lattices** to `2` (say) will indicate to the program that you would like to consider attempting to separately index the unindexed reflections after the first lattice has been identified. Often the second lattice is a satellite of the main one, as crystals sometimes split when cooled.

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

During this process an effort is made to eliminate "outlier" reflections - these are reflections which do not strictly belong to the crystal lattice but are accidentally close to a reciprocal space position and hence can be indexed. Most often this is an issue with small satellite lattices or ice / powder on the sample. Usually this should not be a cause for concern. To look at the crystal lattice(s) in the reciprocal space crystal frame, open the reciprocal lattice viewer on `indexed.expt` / `indexed.refl` and tick **Show in crystal frame**.

## Bravais Lattice Determination (optional!)

Once you have indexed the data you may optionally attempt to infer the correct Bravais lattice and assign this to constrain the unit cell in subsequent processing. If, for example, the unit cell from indexing has all three angles close to 90° and two unit cell lengths with very similar values you could guess that the unit cell is tetragonal. In `dials.refine_bravais_settings` we take away the guesswork by transforming the unit cell to all possible Bravais lattices which approximately match the triclinic unit cell, and then performing some refinement - if the lattice constraints are correct then imposing them should have little impact on the deviations between the observed and calculated reflection positions (known as the R.M.S. deviations). If a lattice constraint is incorrect it will manifest as a significant increase in a deviation - however care must be taken as it can be the case that the true _symmetry_ is lower than the shape of the unit cell would indicate.

In the general case there is little harm in skipping this step, however for information if you click **5. Bravais Lattice Determination (optional)** and then **Run dials.refine_bravais_settings** (the inputs default to `indexed.expt` and `indexed.refl`) you will see a table of possible unit cell / Bravais lattice / R.M.S. deviations in the output - in the case of this tutorial data they will all match, as the true symmetry is cubic.

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
|   *     22 |       0.1001 |  0.051 | 0.835/0.951  |    12000 | cI        | 77.96  77.96  77.96  90.00  90.00  90.00  |   473773 | b+c,a+c,a+b       |
|   *     21 |       0.1001 |  0.05  | 0.873/0.874  |    12000 | hR        | 110.24 110.24  67.50  90.00  90.00 120.00 |   710380 | a+2*b+c,-b+c,a    |
|   *     20 |       0.1001 |  0.052 | 0.835/0.837  |    12000 | hR        | 110.25 110.25  67.55  90.00  90.00 120.00 |   711095 | a+b+2*c,a-c,b     |
|   *     19 |       0.1001 |  0.051 | 0.539/0.839  |    12000 | tI        | 77.95  77.95  77.96  90.00  90.00  90.00  |   473640 | b+c,a+c,a+b       |
|   *     18 |       0.0971 |  0.05  | 0.550/0.841  |    12000 | tI        | 77.98  77.98  77.94  90.00  90.00  90.00  |   473898 | a+b,b+c,a+c       |
|         17 |       0.0971 |  0.052 | 0.492/0.932  |    12000 | tI        | 77.96  77.96  77.99  90.00  90.00  90.00  |   474003 | a+c,a+b,b+c       |
|   *     16 |       0.0971 |  0.051 | 0.839/0.932  |    12000 | oI        | 77.95  77.98  78.00  90.00  90.00  90.00  |   474063 | a+c,a+b,b+c       |
|   *     15 |       0.1001 |  0.051 | 0.501/0.839  |    12000 | oF        | 77.97 110.24 110.25  90.00  90.00  90.00  |   947615 | -a-b,a+b+2*c,-a+b |
|   *     14 |       0.0971 |  0.051 | 0.839/0.839  |    12000 | mI        | 77.95  77.98  78.00  90.00  90.01  90.00  |   474126 | -a-c,a+b,-b-c     |
|   *     13 |       0.1001 |  0.051 | 0.501/0.501  |    12000 | mI        | 67.51 110.24  67.54  90.00 109.47  90.00  |   473885 | -a,-a-b-2*c,-b    |
|   *     12 |       0.0722 |  0.037 | 0.526/0.841  |    12000 | oF        | 77.88 110.11 110.28  90.00  90.00  90.00  |   945747 | a+c,a+2*b+c,-a+c  |
|   *     11 |       0.0575 |  0.035 | 0.950/0.951  |    12000 | hR        | 110.05 110.05  67.48  90.00  90.00 120.00 |   707843 | 2*a+b+c,-a+b,c    |
|   *     10 |       0.0663 |  0.038 | 0.566/0.932  |    12000 | oF        | 77.91 110.10 110.26  90.00  90.00  90.00  |   945776 | -b-c,2*a+b+c,-b+c |
|   *      9 |       0.0722 |  0.037 | 0.841/0.841  |    12000 | mI        | 77.92  77.89  77.95  90.00  90.09  90.00  |   473148 | a+b,-a-c,b+c      |
|   *      8 |       0.0663 |  0.037 | 0.932/0.932  |    12000 | mI        | 77.90  77.91  77.92  90.00  90.08  90.00  |   472909 | a+c,-b-c,a+b      |
|   *      7 |       0.0575 |  0.03  | 0.586/0.586  |    12000 | mI        | 67.43 110.05  67.49  90.00 109.54  90.00  |   471963 | -a,a+2*b+c,-c     |
|   *      6 |       0.0561 |  0.035 | 0.613/0.613  |    12000 | mI        | 67.45 110.06  67.50  90.00 109.50  90.00  |   472342 | -b,-2*a-b-c,-c    |
|   *      5 |       0.0445 |  0.033 | 0.884/0.884  |    12000 | hR        | 110.27 110.27  67.43  90.00  90.00 120.00 |   710034 | b-c,-a+c,a+b+c    |
|   *      4 |       0.0445 |  0.033 | 0.526/0.526  |    12000 | mI        | 67.43 110.29  67.50  90.00 109.46  90.00  |   473288 | -a-b-c,-a+c,b     |
|   *      3 |       0.0439 |  0.032 | 0.566/0.566  |    12000 | mI        | 67.42 110.27  67.48  90.00 109.43  90.00  |   473134 | -a-b-c,b-c,a      |
|   *      2 |       0.0247 |  0.028 | 0.586/0.586  |    12000 | mI        | 67.39 110.14  67.50  90.00 109.46  90.00  |   472344 | -a-b-c,a-b,c      |
|   *      1 |       0      |  0.028 | -/-          |    12000 | aP        | 67.46  67.46  67.50 109.49 109.52 109.47  |   236271 | a,b,c             |
+------------+--------------+--------+--------------+----------+-----------+-------------------------------------------+----------+-------------------+
```

If you wish to use one of the output experiments from this process e.g. `bravais_setting_22.expt` you will need to reindex the reflection data from indexing to match this - we do not output every option of reindexed data as these files can be large. In most cases it is simpler to go back to **4. Index**, type the chosen space group (e.g. `I23`) into the **space_group** field, and run it again.

The reader is reminded here - in most cases it is absolutely fine to proceed without worrying about the crystal symmetry at this stage 🙂.

## Refinement

The model is already refined during indexing, but this is assuming that a single crystal model is appropriate for every image in the data set - in reality there are usually small changes in the unit cell and crystal orientation throughout the experiment as the sample is rotated. `dials.refine` will first re-run refinement with a fixed unit cell and then perform scan-varying refinement. If you have indexed multiple sweeps earlier in processing (not covered in this tutorial) then the crystal models will be copied and split at this stage to allow per-crystal-per-scan models to be refined.

Click **6. Refine**. The inputs default to `indexed.expt` and `indexed.refl` and by and large one may simply click **Run dials.refine** without setting any options - the program will do something sensible.

![Refine setup](./images/gui-refine-setup.png)

Once it has finished, the **Summary** tab pulls out the key tables from the log. If you compare the R.M.S. deviations from the end of indexing with the end of refinement you should see a small improvement e.g.

```
RMSDs by experiment:
+-------+--------+----------+----------+------------+
|   Exp |   Nref |   RMSD_X |   RMSD_Y |     RMSD_Z |
|    id |        |     (px) |     (px) |   (images) |
|-------+--------+----------+----------+------------|
|     0 |  12000 |  0.25638 |  0.27142 |    0.30518 |
+-------+--------+----------+----------+------------+
```

to:

```
RMSDs by experiment:
+-------+--------+----------+----------+------------+
|   Exp |   Nref |   RMSD_X |   RMSD_Y |     RMSD_Z |
|    id |        |     (px) |     (px) |   (images) |
|-------+--------+----------+----------+------------|
|     0 |  42850 |  0.21098 |  0.20732 |    0.21382 |
+-------+--------+----------+----------+------------+
```

![Refine summary](./images/gui-refine-summary.png)

If you look at the output of `dials.report` at this stage (use **Run and show report in web browser**, or the **dials.report** button with `refined.expt` / `refined.refl`) you should see small variations in the unit cell and sample orientation as the crystal is rotated - if these do not appear small then it is likely that something has happened during data collection e.g. severe radiation damage.

## Integration

Once you have refined the model the next step is to integrate the data - in effect this is using the refined model to calculate the positions where all of the reflections in the data set will be found and measure the background-subtracted intensities.

Click **7. Integrate**. The inputs default to `refined.expt` and `refined.refl`. Click **Run dials.integrate**.

![Integrate setup](./images/gui-integrate-setup.png)

By default this will pass through the data twice, first looking at the shapes of the predicted spots to form a reference profile model then passing through a second time to use this profile model to integrate the data, by being fit to the transformed pixel values. This is by far the most computationally expensive step in the processing of the data. By default all the processors in your computer are used (or the number set in **nproc**), unless we think this will exceed the memory available in the machine - the memory situation report and the way the images are split into blocks are visible in the **Live Output** tab as the step runs. At times, however, if you have a large unit cell and / or a large data set you may find that processing on a desktop workstation is more appropriate than e.g. a laptop.

![Integrate running](./images/gui-integrate-live-output.png)

If you know in advance that the data do not diffract to anything close to the edges of the detector you can assign a resolution limit at this stage by setting **prediction.d_min** to `1.8` (say) to define a 1.8 Å resolution limit - this should in general not be necessary. At the end of integration two new files are created - `integrated.refl` and `integrated.expt` - looking at these in the image viewer (the **dials.image_viewer** button with `integrated.expt` and `integrated.refl`) can be very enlightening as you should see little red boxes around every reflection. You may see a selection of reflections close to the rotation axis are missed - these are not well modelled or predicted in any program so typically excluded from processing.

## Symmetry analysis

Before the data may be scaled it is necessary that the crystal symmetry is known - if this was assigned correctly at indexing e.g. `space_group=I213` then you can proceed directly to scaling. In the majority of cases however it will be unknown or not set at this point, so needs to be assigned between integration and scaling. Even if the Bravais lattice was assigned earlier, the correct symmetry _within_ that lattice is needed.

The symmetry analysis in DIALS takes the information from the spot positions and also the spot intensities. The former are used to effectively re-run `dials.refine_bravais_settings` to identify possible lattices and hence candidate symmetry operations, and the latter are used to assess the presence or absence of these symmetry operations. Once the operations are found, the crystal rotational symmetry is assigned by composing these operations into a putative space group. In addition, systematically absent reflections are also assessed to assign a best guess to translational elements of the symmetry - though these are not needed for scaling, they may help with downstream analysis rather than you having to manually identify them.

Click **8. Symmetry (single crystal)**. The inputs default to `integrated.expt` and `integrated.refl`; click **Run dials.symmetry**. (The **8b. Cosym** and **8c. Correlation Matrix** steps are the multi-crystal equivalents and are covered in the main tutorial.)

![Symmetry setup](./images/gui-symmetry-setup.png)

At this point it is important to note that the program is trying to identify all symmetry elements, and does not know that e.g. inversion centres are not possible - so for an oP lattice it will be testing for P/mmm symmetry which corresponds to P2?2?2? in standard MX.

In the output you'll see first the individual symmetry operation:

```
Scoring individual symmetry elements

+--------------+--------+------+--------+-----+---------------+
|   likelihood |   Z-CC |   CC |      N |     | Operator      |
|--------------+--------+------+--------+-----+---------------|
|        0.946 |   9.97 | 1    |  85410 | *** | 1 |(0, 0, 0)  |
|        0.166 |   4.55 | 0.45 | 168526 |     | 4 |(1, 1, 0)  |
|        0.172 |   4.66 | 0.47 | 148590 |     | 4 |(1, 0, 1)  |
|        0.168 |   4.6  | 0.46 | 155754 |     | 4 |(0, 1, 1)  |
|        0.945 |   9.96 | 1    | 163264 | *** | 3 |(1, 0, 0)  |
|        0.945 |   9.96 | 1    | 148988 | *** | 3 |(0, 1, 0)  |
|        0.945 |   9.95 | 1    | 166456 | *** | 3 |(0, 0, 1)  |
|        0.945 |   9.96 | 1    | 124276 | *** | 3 |(1, 1, 1)  |
|        0.945 |   9.96 | 1    |  90954 | *** | 2 |(1, 1, 0)  |
|        0.162 |   4.47 | 0.45 |  84768 |     | 2 |(-1, 1, 0) |
|        0.945 |   9.95 | 1    |  70454 | *** | 2 |(1, 0, 1)  |
|        0.173 |   4.67 | 0.47 |  63760 |     | 2 |(-1, 0, 1) |
|        0.945 |   9.96 | 1    |  75290 | *** | 2 |(0, 1, 1)  |
|        0.171 |   4.64 | 0.46 |  95580 |     | 2 |(0, -1, 1) |
|        0.161 |   4.46 | 0.45 |  88804 |     | 2 |(1, 1, 2)  |
|        0.16  |   4.43 | 0.44 |  77824 |     | 2 |(1, 2, 1)  |
|        0.159 |   4.41 | 0.44 |  74274 |     | 2 |(2, 1, 1)  |
+--------------+--------+------+--------+-----+---------------+
```

Which shows clear 2 and 3 fold symmetry but no 4-fold symmetry. This will prove to be important in the main tutorial as this creates ambiguity. These are followed by the results of composing these into the possible space groups and the likelihood assessment of these - which takes into consideration the elements present in the space group and also those not present. The bottom of that table and the conclusion are visible in the **Live Output** tab:

![Symmetry output](./images/gui-symmetry-output.png)

```
Best solution: I m -3
Unit cell: 77.890, 77.890, 77.890, 90.000, 90.000, 90.000
Reindex operator: a+b,a+c,-b-c
Laue group probability: 1.000
Laue group confidence: 1.000

+-------------------+-------------------------+
| Patterson group   | Corresponding MX group  |
|-------------------+-------------------------|
| I m -3            | I 2 3                   |
+-------------------+-------------------------+

Analysing systematic absences

Laue group: I m -3
Space groups I 2 3 & I 21 3 cannot be distinguished with systematic absence
analysis, due to lattice centering.
Using space group I 2 3, space group I 21 3 is equally likely.

Saving reindexed experiments to symmetrized.expt in space group I 2 3
Saving 342188 reindexed reflections to symmetrized.refl
```

Here the symmetry appears to be `I m -3` i.e. 3-fold rotation and three 2-fold mirror axes - and corresponds to some variation of `I2?3` - this information is sufficient for scaling though for structure solution identification of the correct space group is necessary - `dials.symmetry` will also attempt to guess this but in this case it is impossible to see the difference as the screw axes are masked by the centring operation. The **Open HTML in web browser** button shows the `dials.symmetry.html` report.

## Scaling and Merging

During the experiment there are effects which alter the measured intensity of the reflections, not least radiation damage, changes to beam intensity or illuminated volume or absorption within the sample. The purpose of `dials.scale`, like all scaling programs, is to attempt to correct for these effects by using the fact that symmetry related reflections should share a common intensity. By default no attempt is made to merge the reflections - this may be done independently in `dials.merge` - but a table of merging statistics is printed at the end along with resolution recommendations.

Click **9. Scale**. The inputs default to `symmetrized.expt` and `symmetrized.refl`. For anomalous data tick the **anomalous** box; for native data leave it unticked. Then click **Run dials.scale**.

![Scale setup](./images/gui-scale-setup.png)

This will run everything with the defaults which allows for:

- modest radiation damage
- changes in overall intensity
- modest sample absorption

with the latter being the parameter most likely changed. If you have a data set recorded from a sample containing a large amount of metal (not common in MX) or recorded at long wavelength e.g, for sulphur SAD it may be necessary to adjust the extent to which the absorption correction is constrained by choosing `medium` _or_ `high` from the **absorption_level** drop-down, where `low`, the default, corresponds to ~ 1% absorption, `medium` to ~ 5% and `high` to ~ 25% - these are not absolute, more a sense of what you may expect. Testing has indicated that setting it too high is unlikely to do any harm, but setting it too low can have a measurable impact on the quality of the data for phasing experiments. The **d_min** field lets you apply a resolution cut-off, e.g. the one suggested by a previous run of scaling. (The **Cluster to scale** drop-down is only used in the multi-crystal workflow, after the Correlation Matrix step.)

`dials.scale` generates a HTML report `dials.scale.html` which includes a lot of information about how the models look, as well as regions of the data which agree well and poorly - from a practical perspective this is the point where you really _know_ about the final quality of the data. Click **Open HTML in web browser** to view it. The overall summary data are printed to the **Live Output** tab and the log file e.g.:

```
            -------------Summary of merging statistics--------------           

                                            Suggested   Low    High  Overall
High resolution limit                           1.29    3.50    1.29    1.05
Low resolution limit                           55.08   55.13    1.31   55.08
Completeness                                  100.0   100.0   100.0    88.7
Multiplicity                                   13.4    12.9    13.1    10.4
I/sigma                                        17.9   104.0     0.4    11.1
Rmerge(I)                                     0.065   0.024   3.437   0.073
Rmerge(I+/-)                                  0.062   0.023   3.306   0.069
Rmeas(I)                                      0.067   0.025   3.576   0.076
Rmeas(I+/-)                                   0.067   0.025   3.584   0.075
Rpim(I)                                       0.018   0.007   0.984   0.022
Rpim(I+/-)                                    0.025   0.009   1.378   0.029
CC half                                       1.000   1.000   0.268   1.000
Anomalous completeness                        100.0   100.0   100.0    79.1
Anomalous multiplicity                          7.0     7.1     6.7     5.6
Anomalous correlation                        -0.019  -0.035  -0.016  -0.013
Anomalous slope                               0.680                        
dF/F                                          0.050                        
dI/s(dI)                                      0.697                        
Total observations                           267970   13812   13029  335453
Total unique                                  19928    1071     994   32271
```

as well as a better estimate for the resolution, if this is lower than the full extent of the data. Further up you will also see an analysis of the error model:

```
Error model details:
  Type: basic
  Parameters: a = 0.82350, b = 0.02606
  Error model formula: σ'² = a²(σ² + (bI)²)
  estimated I/sigma asymptotic limit: 46.595
```

which is very useful for basic diagnostics. This is immediately comparable with the ISa statistic from XDS. If you have a lot of anomalous signal the difference in error model between `anomalous` ticked and unticked can be substantial, as it will be inflating the errors to account for the differences.

## Merging or Exporting

Most downstream software depends on a scaled _and merged_ data set e.g. for molecular replacement, so at the end of processing click **10. Merge / Export**. The inputs default to `scaled.expt` and `scaled.refl`, and the **mode** drop-down chooses between:

- `merge` - runs `dials.merge` and writes a scaled and merged MTZ file (`merged.mtz`), which is what most structure solution / molecular replacement pipelines want
- `export` - runs `dials.export` and simply writes the scaled but unmerged reflections in MTZ format

![Merge / export setup](./images/gui-merge-setup.png)

At this stage, setting the **d_min** field to the resolution limit proposed at the end of scaling may be appropriate. Click **Run dials.merge** (or **Run dials.export**). The **Live Output** shows a summary of the MTZ file that was written, including the columns it contains:

![Merge output](./images/gui-merge-output.png)

## What you end up with

If you look in the working directory at the end (here from a terminal with `ls`) you will find the `.expt` / `.refl` pair from every step, the `dials.*.log` file for every program that was run, the HTML reports from symmetry, scaling and merging, the `bravais_setting_*.expt` files from the optional Bravais lattice step, and the final `merged.mtz` - exactly the same set of files you would have produced by running the commands shown in blue by hand.

![Output files](./images/gui-output-files.png)

Because the GUI records which steps have run, you can come back to this directory at any time, click **Load state from working dir**, and re-run any single step with different parameters - everything downstream of it will simply need running again.
