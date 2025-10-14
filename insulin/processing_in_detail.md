# Processing in Detail (Diamond / CCP4 2022)

## Introduction

DIALS processing may be performed by either running the individual tools (spot finding, indexing, refinement, integration, symmetry, scaling, exporting to MTZ) or you can run `xia2`, which makes informed choices for you at each stage. In this tutorial we will run through each of the steps in turn, taking a look at the output as we go. We will also look at enforcing the correct lattice symmetry.

The aim of this tutorial is to introduce you to the tools, not teach about data processing - it is assumed you have some idea of the overall process from e.g. associated lectures. With the graphical tools, I am not making so much effort to explain the options as simply "playing" will give you a chance to learn your way around and also find the settings which work for you. Particularly with looking at diffraction images, the "best" settings are very personal.

## DIALS version

This tutorial assumes you are using [DIALS version 3.12](https://dials.github.io/installation.html) and that you have this set up (i.e. you've run `module load ccp4-workshop`).

If you type `dials.version` you should see something like:

        DIALS 3.12.0-g13ced8fbc-release
        Python 3.9.13
        Installed in: /dls_sw/apps/dials/dials-v3-12-0/modules/dials/src/dials

If you are running this at home with a different version of DIALS, details may change but the general flow should be the same.

## Tutorial data

The data for this tutorial were collected with a deliberately wide rotation angle (i.e. going against my advice in the lectures) to allow quick processing... they are in

        /dls/i03/data/2022/mx33300-1/TestInsulin/ins_11/

and we will look at `ins_11_1.nxs` - there are other data sets in surrounding areas which are more carefully measured. The same data are available [here](https://zenodo.org/record/7277713) to allow following through the tutorials remotely.

## Files

DIALS creates two principal file types:

- experiment files called `something.expt`
- reflection files called `something.refl`

"Experiment" in DIALS has a very specific meaning - the capturing of data from one set of detector, beam, goniometer and crystal - so if you have two scans from one crystal this is two experiments, if you have two lattices on one data set this is two experiments. In most cases you can ignore this distinction though.

Usually the output filenames will correspond to the name of the DIALS program that created them e.g. `indexed.refl` and `indexed.expt` from `dials.index`. The only deviations from this are on import (see below) where we are only reading experiment models and spot finding where we find _strong_ reflections so write these to `strong.refl` - and we create no models so (by default) there is no output experiment file.

At any time you can _look_ at these files with `dials.show` which will summarise the content of the files to the terminal.

[If you're impatient...](./tldr.md) - the truth is this is pretty much how I start processing any data set these days.

## Parameters

All DIALS programs accept parameters in the form of `parameter=value` - in most cases this will be sufficient though some less frequently used options may require "name space" clarification e.g. `index_assignment.method=local`. All of the DIALS programs support the option

        dials.program -c -e2

which will show you all possible configuration options - if you are looking for an option this is the simplest way to search so e.g.

        dials.index -c -e2 | less

will allow you to scroll through the extensive list of options you can adjust. In most cases the defaults are relatively sensible for synchrotron data from a pixel array detector, as we are using in this tutorial.

## Output

In the majority of cases the `dials` programs write their output to `dials.program.log` e.g. `dials.find_spots.log` etc. - everything which is printed to the terminal is also saved in this file, so you can review the processing later. In the case where you are reporting an issue to the developers including these log files in the error report (particularly for the step which failed) is very helpful.

From most stages you can generate a more verbose _report_ of the current state of processing with:

        dials.report step.expt step.refl

which will generate a detailed report as HTML describing the current
state of the processing.

## Import

The starting point for any processing with DIALS is to _import_ the data - here the metadata are read and a description of the data to be processed saved to a file named `imported.expt`. This is "human readable" in that the file is JSON format (roughly readable text with brackets around to structure for computers). While you can edit this file if you know what you are doing, usually this is not necessary.

        dials.import /dls/i03/data/2022/mx33300-1/TestInsulin/ins_11/ins_11_1_master.h5

will read the metadata from this `nexus` file and write `imported.expt` from this.

It is important to note that for well-behaved data (i.e. anything which is well-collected from a well-behaved sample) the commands below will often be identical after importing.

At this point you can actually look at the images with the `dials.image_viewer` tool -

        dials.image_viewer imported.expt

in this tool there are many settings you can adjust, which could depend on the source of the data and - most importantly - your preferences.

To get a sense of how the diffraction spots are spread, stacking images can help - for example in this case setting the stack to 5 gives a good idea of the real separation between reflections. If the data are not stacked the spot finding process can also be explored - the controls at the bottom of the "Settings" window allow you to step through these and can be very useful for getting a "computer's eye view" of how the data look (particularly for establishing where the diffraction is visible to.)

[Here](./import_detail.md) is a short discussion on some more details of importing data.

## Find Spots

The first "real" task in any processing using DIALS is the spot finding. Since this is looking for spots on every image in the dataset, this process can take some time so by default will use all of the processors available in your machine - if you would like to control this adjust with e.g. `nproc=4` - however the default is usually sensible unless you are sharing the computer with many others.

        dials.find_spots imported.expt

This is one of the two steps where every image in the data set is read and processed and hence can be moderately time-consuming. This contains a reflection file `strong.refl` which contains both the positions of the strong spots and also "images" of the spot pixels which we will use later. You can view these spots on top of the images with

        dials.image_viewer imported.expt strong.refl

to get a sense of what spots were found. You will see that the spots are surrounded by little blue boxes - these are the _bounding boxes_ of the reflections i.e. the outer extent of the connected regions of the signal pixels. The signal pixels are highlighted with green blobs giving a sense of what is and is not "strong."

![Image viewer](./images/viewer.png)

The default parameters for spot finding usually do a good job for Pilatus images, such as these. However they may not be optimal for data from other detector types, such as CCDs or image plates. Issues with incorrectly set gain might, for example, lead to background noise being extracted as spots. You can use the image mode buttons to preview how the parameters affect the spot finding algorithm. The final button 'threshold’ is the one on which spots were found, so ensuring this produces peaks at real diffraction spot positions will give the best chance of success.

The second tool for visualisation of the found spots is the reciprocal lattice viewer - which presents a view of the spot positions mapped to reciprocal space.

        dials.reciprocal_lattice_viewer imported.expt strong.refl

No matter the sample orientation you should be able to rotate the space to "look down" the lines of reflections. If you cannot, or the lines are not straight, it is likely that there are some errors in the experiment parameters e.g. detector distance or beam centre. If these are not too large they will likely be corrected in the subsequent analysis.

![Reciprocal viewer](./images/reciprocal-lattice.png)

Have a play with the settings - you can change the beam centre in the viewer to see how nicely aligned spots move out of alignment. Some of the options will only work after you have indexed the data. If the geometry is not accurately recorded you may find it useful to run:

        dials.search_beam_position imported.expt strong.refl

to determine an updated position for the beam centre - ideally the shift that this calculates should be small if the beamline is well-calibrated - if it is a couple of mm or more it may be worth discussing this with the beamline staff! Running the reciprocal lattice viewer with the optimised experiment output:

        dials.reciprocal_lattice_viewer optimised.expt strong.refl

should show straight lines, provided everything has worked correctly. Further discussion of the output can be found [here](./find_spots_detail.md).

## Indexing

The next step will be indexing of the found spots with `dials.index` - by default this uses a 3D FFT algorithm to identify periodicity in the reciprocal space mapped spot positions, though there are other algorithms available which can be better suited to e.g. narrow data sets.

        dials.index imported.expt strong.refl

or

        dials.index optimised.expt strong.refl

are the ways to trigger the program, and the most common parameters to set are the `space_group` and `unit_cell` if these are known in advance. While this does index the data it will also perform some refinement with a static crystal model, and indicate in the output the fraction of reflections which have been indexed - ideally this should be close to 100%:

{% raw %}
```
Refined crystal models:
model 1 (22031 reflections):
Crystal:
    Unit cell: 67.0787(15), 67.0881(18), 67.1497(16), 109.4286(6), 109.4379(5), 109.4057(5)
    Space group: P 1
    U matrix:  {{ 0.1983,  0.4141,  0.8883},
                {-0.5954, -0.6690,  0.4448},
                { 0.7785, -0.6172,  0.1139}}
    B matrix:  {{ 0.0149,  0.0000,  0.0000},
                { 0.0053,  0.0158,  0.0000},
                { 0.0091,  0.0091,  0.0182}}
    A = UB:    {{ 0.0132,  0.0146,  0.0162},
                {-0.0083, -0.0065,  0.0081},
                { 0.0094, -0.0087,  0.0021}}
+------------+-------------+---------------+-------------+
|   Imageset |   # indexed |   # unindexed | % indexed   |
|------------+-------------+---------------+-------------|
|          0 |       22031 |         14143 | 60.9%       |
+------------+-------------+---------------+-------------+
```
{% endraw %}

If it is significantly less than 100% it is possible you have a second lattice - adding `max_lattices=2` (say) to the command-line will indicate to the program that you would like to consider attempting to separately index the unindexed reflections after the first lattice has been identified. In this case there was a clear second lattice which can be indexed well:

{% raw %}
```
Refined crystal models:
model 1 (21933 reflections):
Crystal:
    Unit cell: 67.1002(11), 67.1161(14), 67.1713(12), 109.4317(6), 109.4414(5), 109.4017(5)
    Space group: P 1
    U matrix:  {{ 0.1982,  0.4141,  0.8884},
                {-0.5955, -0.6690,  0.4448},
                { 0.7785, -0.6172,  0.1140}}
    B matrix:  {{ 0.0149,  0.0000,  0.0000},
                { 0.0052,  0.0158,  0.0000},
                { 0.0091,  0.0091,  0.0182}}
    A = UB:    {{ 0.0132,  0.0146,  0.0162},
                {-0.0083, -0.0065,  0.0081},
                { 0.0094, -0.0087,  0.0021}}
model 2 (11577 reflections):
Crystal:
    Unit cell: 67.0129(15), 67.0339(12), 67.1879(13), 109.4653(6), 109.4389(7), 109.3508(6)
    Space group: P 1
    U matrix:  {{-0.3130, -0.3469, -0.8841},
                { 0.3928,  0.8003, -0.4531},
                { 0.8647, -0.4891, -0.1142}}
    B matrix:  {{ 0.0149,  0.0000,  0.0000},
                { 0.0052,  0.0158,  0.0000},
                { 0.0091,  0.0091,  0.0182}}
    A = UB:    {{-0.0145, -0.0135, -0.0161},
                { 0.0059,  0.0085, -0.0082},
                { 0.0093, -0.0088, -0.0021}}
+------------+-------------+---------------+-------------+
|   Imageset |   # indexed |   # unindexed | % indexed   |
|------------+-------------+---------------+-------------|
|          0 |       33510 |          2661 | 92.6%       |
+------------+-------------+---------------+-------------+
Change of basis op: a,b,c
Rotation matrix to transform crystal 1 to crystal 2:
{{-0.991, 0.025, -0.130},
 {0.007, -0.971, -0.240},
 {-0.133, -0.239, 0.962}}
Rotation of -179.465 degrees about axis (-0.066, -0.121, 0.990)
```
{% endraw %}

Here we see that there is a second lattice which is almost 180° separated: this is a very common outcome, resulting from the crystal splitting when cooled. In this case a reasonable data set can be obtained ignoring the second lattice, so we can just go ahead with the single lattice results. By default the triclinic lattice i.e. with `P1` no additional symmetry is assumed - for the majority of data there are no differences in the quality of the results from assigning the Bravais lattice at this stage, even if as here it is perfectly obvious what the correct answer is.

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

        dials.refine_bravais_settings indexed.expt indexed.refl

you will see a table of possible unit cell / Bravais lattice / R.M.S. deviations printed in the output - in the case of this tutorial data they will all match, as the true symmetry is tetragonal.

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
|   *     22 |       0.1746 |  0.076 | 0.765/0.846  |     9000 | cI        | 77.88  77.88  77.88  90.00  90.00  90.00  |   472354 | b+c,a+c,a+b       |
|   *     21 |       0.1746 |  0.076 | 0.592/0.814  |     9000 | tI        | 77.88  77.88  77.84  90.00  90.00  90.00  |   472111 | b+c,a+c,a+b       |
|   *     20 |       0.1746 |  0.076 | 0.583/0.841  |     9000 | tI        | 77.87  77.87  77.91  90.00  90.00  90.00  |   472390 | a+b,b+c,a+c       |
|   *     19 |       0.1746 |  0.076 | 0.603/0.807  |     9000 | tI        | 77.89  77.89  77.89  90.00  90.00  90.00  |   472487 | a+c,a+b,b+c       |
|   *     18 |       0.1746 |  0.076 | 0.807/0.841  |     9000 | oI        | 77.84  77.91  77.87  90.00  90.00  90.00  |   472201 | a+b,a+c,-b-c      |
|   *     17 |       0.1697 |  0.053 | 0.616/0.841  |     9000 | oF        | 77.72 109.79 110.10  90.00  90.00  90.00  |   939381 | -a-c,-a+c,a+2*b+c |
|   *     16 |       0.1576 |  0.049 | 0.843/0.846  |     9000 | hR        | 110.06 110.06  67.23  90.00  90.00 120.00 |   705259 | a+2*b+c,-b+c,a    |
|   *     15 |       0.1655 |  0.073 | 0.772/0.789  |     9000 | hR        | 110.09 110.09  67.32  90.00  90.00 120.00 |   706590 | a+b+2*c,a-c,b     |
|   *     14 |       0.1655 |  0.076 | 0.765/0.843  |     9000 | hR        | 110.15 110.15  67.44  90.00  90.00 120.00 |   708624 | 2*a+b+c,-a+b,c    |
|   *     13 |       0.1746 |  0.073 | 0.598/0.807  |     9000 | oF        | 77.80 109.87 110.04  90.00  90.00  90.00  |   940646 | b+c,-b+c,2*a+b+c  |
|   *     12 |       0.1697 |  0.052 | 0.841/0.841  |     9000 | mI        | 77.73  77.72  77.74  90.00  90.16  90.00  |   469672 | a+b,a+c,-b-c      |
|   *     11 |       0.1746 |  0.073 | 0.807/0.807  |     9000 | mI        | 77.72  77.78  77.77  90.00  90.08  90.00  |   470151 | -a-b,-b-c,a+c     |
|   *     10 |       0.1576 |  0.042 | 0.638/0.638  |     9000 | mI        | 67.21 110.06  67.31  90.00 109.39  90.00  |   469695 | -a,a+2*b+c,-c     |
|   *      9 |       0.1655 |  0.071 | 0.598/0.598  |     9000 | mI        | 67.25 110.01  67.31  90.00 109.39  90.00  |   469732 | -b,-2*a-b-c,-c    |
|   *      8 |       0.1018 |  0.042 | 0.602/0.814  |     9000 | oF        | 77.60 109.58 109.95  90.00  90.00  90.00  |   934984 | a+b,-a+b,a+b+2*c  |
|   *      7 |       0.1016 |  0.039 | 0.814/0.814  |     9000 | mI        | 77.66  77.60  77.60  90.00  90.19  90.00  |   467582 | -a-c,-a-b,b+c     |
|   *      6 |       0.1018 |  0.041 | 0.602/0.602  |     9000 | mI        | 67.14 109.96  67.17  90.00 109.39  90.00  |   467769 | -a,-a-b-2*c,-b    |
|   *      5 |       0.0658 |  0.033 | 0.806/0.815  |     9000 | hR        | 109.60 109.60  67.29  90.00  90.00 120.00 |   699973 | b-c,-a+c,a+b+c    |
|   *      4 |       0.0658 |  0.032 | 0.616/0.616  |     9000 | mI        | 67.10 109.58  67.28  90.00 109.54  90.00  |   466187 | b,a-c,-a-b-c      |
|   *      3 |       0.0559 |  0.026 | 0.656/0.656  |     9000 | mI        | 67.11 109.64  67.29  90.00 109.48  90.00  |   466761 | a,-b+c,-a-b-c     |
|   *      2 |       0.0135 |  0.023 | 0.615/0.615  |     9000 | mI        | 67.16 109.51  67.26  90.00 109.56  90.00  |   466089 | c,-a+b,-a-b-c     |
|   *      1 |       0      |  0.023 | -/-          |     9000 | aP        | 67.08  67.09  67.15 109.43 109.44 109.41  |   233036 | a,b,c             |
+------------+--------------+--------+--------------+----------+-----------+-------------------------------------------+----------+-------------------+
* = recommended solution
```

If you wish to use one of the output experiments from this process e.g. `bravais_setting_22.expt` you will need to reindex the reflection data from indexing to match this - we do not output every option of reindexed data as these files can be large. In most cases it is simpler to re-run `dials.index` setting the chosen space group.

The reader is reminded here - in most cases it is absolutely fine to proceed without worrying about the crystal symmetry at this stage 🙂.

## Refinement

The model is already refined during indexing, but this is assuming that a single crystal model is appropriate for every image in the data set - in reality there are usually small changes in the unit cell and crystal orientation throughout the experiment as the sample is rotated. `dials.refine` will first re-run refinement with a fixed unit cell and then perform scan-varying refinement. If you have indexed multiple sweeps earlier in processing (not covered in this tutorial) then the crystal models will be copied and split at this stage to allow per-crystal-per-scan models to be refined.

By and large one may run:

        dials.refine indexed.expt indexed.refl

without any options and the program will do something sensible - if you compare the R.M.S. deviations from the end of indexing with the end of refinement you should see a small improvement e.g.

```
RMSDs by experiment:
+-------+--------+----------+----------+------------+
|   Exp |   Nref |   RMSD_X |   RMSD_Y |     RMSD_Z |
|    id |        |     (px) |     (px) |   (images) |
|-------+--------+----------+----------+------------|
|     0 |   9000 |  0.22756 |  0.20807 |     0.1411 |
+-------+--------+----------+----------+------------+
```

to:

```
RMSDs by experiment:
+-------+--------+----------+----------+------------+
|   Exp |   Nref |   RMSD_X |   RMSD_Y |     RMSD_Z |
|    id |        |     (px) |     (px) |   (images) |
|-------+--------+----------+----------+------------|
|     0 |  17478 |  0.19828 |   0.1788 |    0.11457 |
+-------+--------+----------+----------+------------+
```

If you look at the output of `dials.report` at this stage you should see small variations in the unit cell and sample orientation as the crystal is rotated - if these do not appear small then it is likely that something has happened during data collection e.g. severe radiation damage.

## Integration

Once you have refined the model the next step is to integrate the data - in effect this is using the refined model to calculate the positions where all of the reflections in the data set will be found and measure the background-subtracted intensities:

        dials.integrate refined.expt refined.refl

By default this will pass through the data twice, first looking at the shapes of the predicted spots to form a reference profile model then passing through a second time to use this profile model to integrate the data, by being fit to the transformed pixel values. This is by far the most computationally expensive step in the processing of the data!

by default all the processors in your computer are used, unless we think this will exceed the memory available in the machine. At times, however, if you have a large unit cell and / or a large data set you may find that processing on a desktop workstation is more appropriate than e.g. a laptop.

If you know in advance that the data do not diffract to anything close to the edges of the detector you can assign a resolution limit at this stage by adding `prediction.d_min=1.8` (say) to define a 1.8 Å resolution limit - this should in general not be necessary. At the end of integration two new files are created - `integrated.refl` and `integrated.expt` - looking at these in the image viewer e.g.

        dials.image_viewer integrated.expt integrated.refl

can be very enlightening as you should see little red boxes around every reflection - if you select "integrated only" you can see what was and was not integrated. You may see a selection of reflections close to the rotation axis are missed - these are not well modelled or predicted in any program so typically excluded from processing.

## Symmetry analysis

Before the data may be scaled it is necessary that the crystal symmetry is known - if this was assigned correctly at indexing e.g. `space_group=I213` then you can proceed directly to scaling. In the majority of cases however it will be unknown or not set at this point, so needs to be assigned between integration and scaling. Even if the Bravais lattice was assigned earlier, the correct symmetry _within_ that lattice is needed.

The symmetry analysis in DIALS takes the information from the spot positions and also the spot intensities. The former are used to effectively re-run `dials.refine_bravais_settings` to identify possible lattices and hence candidate symmetry operations, and the latter are used to assess the presence or absence of these symmetry operations. Once the operations are found, the crystal rotational symmetry is assigned by composing these operations into a putative space group. In addition, systematically absent reflections are also assessed to assign a best guess to translational elements of the symmetry - though these are not needed for scaling, they may help with downstream analysis rather than you having to manually identify them.

        dials.symmetry integrated.expt integrated.refl

is how this step is run. At this point it is important to note that
the program is trying to identify all symmetry elements, and does not
know that e.g. inversion centres are not possible - so for an oP
lattice it will be testing for P/mmm symmetry which corresponds to
P2?2?2? in standard MX.

The data in this tutorial give interesting output for this:

```
+--------------+--------+------+-------+-----+---------------+
|   likelihood |   Z-CC |   CC |     N |     | Operator      |
|--------------+--------+------+-------+-----+---------------|
|        0.943 |   9.92 | 0.99 | 24130 | *** | 1 |(0, 0, 0)  |
|        0.177 |   4.75 | 0.48 | 34990 |     | 4 |(1, 1, 0)  |
|        0.161 |   4.47 | 0.45 | 34730 |     | 4 |(1, 0, 1)  |
|        0.16  |   4.45 | 0.44 | 34902 |     | 4 |(0, 1, 1)  |
|        0.939 |   9.81 | 0.98 | 50328 | *** | 3 |(1, 0, 0)  |
|        0.936 |   9.75 | 0.97 | 43702 | *** | 3 |(0, 1, 0)  |
|        0.937 |   9.77 | 0.98 | 30082 | *** | 3 |(0, 0, 1)  |
|        0.936 |   9.75 | 0.98 | 28854 | *** | 3 |(1, 1, 1)  |
|        0.942 |   9.87 | 0.99 | 15282 | *** | 2 |(1, 1, 0)  |
|        0.182 |   4.83 | 0.48 | 11226 |     | 2 |(-1, 1, 0) |
|        0.942 |   9.87 | 0.99 | 19976 | *** | 2 |(1, 0, 1)  |
|        0.15  |   4.25 | 0.43 | 19170 |     | 2 |(-1, 0, 1) |
|        0.943 |   9.9  | 0.99 | 19334 | *** | 2 |(0, 1, 1)  |
|        0.161 |   4.46 | 0.45 | 32878 |     | 2 |(0, -1, 1) |
|        0.163 |   4.49 | 0.45 | 24440 |     | 2 |(1, 1, 2)  |
|        0.164 |   4.52 | 0.45 | 26138 |     | 2 |(1, 2, 1)  |
|        0.136 |   3.93 | 0.39 | 20246 |     | 2 |(2, 1, 1)  |
+--------------+--------+------+-------+-----+---------------+
```

Here it is clear that there are some operations that have close to 100% CC, others that are much lower - in particular the 4-fold rotations in the middle of the faces are not present which means the crystal has a _polar_ space group so care needs to be taken when combining data from multiple samples.

## Scaling and Merging

During the experiment there are effects which alter the measured intensity of the reflections, not least radiation damage, changes to beam intensity or illuminated volume or absorption within the sample. The purpose of `dials.scale`, like all scaling programs, is to attempt to correct for these effects by using the fact that symmetry related reflections should share a common intensity. By default no attempt is made to merge the reflections - this may be done independently in `dials.merge` - but a table of merging statistics is printed at the end along with resolution recommendations.

        dials.scale symmetrized.expt symmetrized.refl

or

        dials.scale symmetrized.expt symmetrized.refl anomalous=True

runs everything with the defaults which allows for:

- modest radiation damage
- changes in overall intensity
- modest sample absorption

with the latter being the parameter most likely changed. If you have a data set recorded from a sample containing a large amount of metal (not common in MX) or recorded at long wavelength e.g, for sulphur SAD it may be necessary to adjust the extent to which the absorption correction is constrained with one of these options:

- `absorption_level=low`
- `absorption_level=medium`
- `absorption_level=high`

where setting low, the default, corresponds to ~ 1% absorption, medium to ~5% and high to ~ 25% - these are not absolute, more a sense of what you may expect. Testing has indicated that setting it too high is unlikely to do any harm, but setting it too low can have a measurable impact on the quality of the data for phasing experiments. `dials.scale` generates a HTML report `dials.scale.html` which includes a lot of information about how the models look, as well as regions of the data which agree well and poorly - from a practical perspective this is the point where you really _know_ about the final quality of the data.

## Estimating resolution

After scaling you can estimate the resolution limit of the scaled data with `dials.estimate_resolution` - this performs a fit and reads off where CC-half is 0.3 by default

        dials.estimate_resolution scaled.*

This will also write out a HTML file with a graph to inspect. You can take the output of this and re-scale the data to this limit with `d_min=1.71` (in this case.)

## Merging or Exporting

Most downstream software depends on a scaled _and merged_ data set e.g. for molecular replacement, so at the end of processing you can run

        dials.export scaled.expt scaled.refl

to simply export the scaled reflections in MTZ format or

        dials.merge scaled.expt scaled.refl

which will output a scaled and merged MTZ file.
