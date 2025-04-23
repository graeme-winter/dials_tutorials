# NE-CAT Staff and User Tutorial

This is a tutorial on what shape the data are and how to manage them, from 24ID-E at the APS: the idea here is to also highlight some of the things to look at during data collection or beamline set-up as well as for _actually_ processing your data.

 There are a couple of tutorials here:

 - processing a simple data set
 - combining a couple of data sets, in the presence of indexing ambiguity
 - diagnosing multiple lattices, processing such data

 The intent is that the instructions allow you to follow along at your own pace. In the general sense the instructions are _not_ beamline specific however as you work through other tutorials you may find that the focus will vary slightly from one tutorial to another, depending on the questions which have been raised.

 TODO: upload the example data to Zenodo. For this the data are _small_ as they are recorded as CBF, and can be bzip2 compressed to ~2GB / run. All the data were taken by Kay Perry with "standard beamline protocols" so show minimal signs of radiation damage and consist of 360° of rotation at 0.2° / image.

## Too Long, Didn't read

To be honest most of the time I run this little script then pick through the bones of what was there: if the data are good or OK, this will probably just work:

```bash
dials.import ## THE DATA e.g. LIST OF CBF or foo_master.h5
dials.find_spots imported.expt
dials.index imported.expt strong.refl
dials.refine indexed.expt indexed.refl
dials.integrate refined.expt refined.refl
dials.symmetry integrated.expt integrated.refl
dials.scale symmetrized.expt symmetrized.refl anomalous=true absorption_level=medium
```

so in this case we will want:

```bash
dials.import ../*cbf.bz2
dials.find_spots imported.expt
dials.index imported.expt strong.refl
dials.refine indexed.expt indexed.refl
dials.integrate refined.expt refined.refl
dials.symmetry integrated.expt integrated.refl
dials.scale symmetrized.expt symmetrized.refl anomalous=true absorption_level=medium
```

This will:

- import the data (discussed below)
- find spots on _every_ frame
- index those spots
- refine the model from indexing
- integrate the spots
- derive the symmetry
- scale the data

There are alternative tracks you can adopt which will be discussed in the longer form narratives below.

## Importing Data, Viewing

To keep things simple first look at a _boring_ data set: `insulin_042225_15_1_00####.cbf.bz2`. With any processing with DIALS the first thing you do is _import_ the data: this reads the headers to make sense of the data set & also explains to _you_ what it found so you can make sense of it. Usually I make a subdirectory of the data area to process a data set, e.g. `work`, but you can process it from anywhere. I would usually recommend _not_ processing in the same folder as the data are. Assuming you have done `mkdir work` or similar, then run:

```bash
dials.import ../insulin_042225_15_1_00*cbf.bz2
```

In this case it will show:

```console
DIALS (2018) Acta Cryst. D74, 85-97. https://doi.org/10.1107/S2059798317017235
DIALS 3.dev.1291-ge4527ba53
The following parameters have been modified:

input {
  experiments = <image files>
}

--------------------------------------------------------------------------------
  format: <class 'dxtbx.format.FormatCBFMiniEiger.FormatCBFMiniEiger'>
  template: /home/graeme/data/necat-e/insulin-2025-04-22/insulin_042225_15/insulin_042225_15_1_######.cbf.bz2:1:1800
  num images: 1800
  sequences:
    still:    0
    sweep:    1
  num stills: 0
--------------------------------------------------------------------------------
Writing experiments to imported.expt
```

This is printed to the screen but also written to `dials.import.log` - this is helpful when trying to work out what happened later on. Here we see we found 1,800 images forming a single sweep - consistent and therefore reassuring. The most useful things to do now are (i) look at the images and (ii) find spots. Looking at the images is easy enough:

```bash
dials.image_viewer imported.expt
```

Which pops up a window with the image in, and gives you a lot of options to play. The basic view is pretty basic, but there are some useful options to view finely sliced diffraction data. The viewer:

![Basic image viewer](./basic-viewer.png)

has a "stack" option which allows multiple images to be stacked to make up e.g. a 1° image:

![One degree stack](./degree.png)

Here I also tweaked the "brightness" in the controls widget:

![Controls widget](./controls.png)

At this point simply playing will be useful, but you can learn some more by reducing stack to 1 then selecting "threshold" at the bottom of the controls - this is the "spot finder view" of the data and very useful for interpreting weak data:

![Spot finder view](./spot-finder-view.png)

we will come back to this in a minute. Right now, take a few minutes to play with the settings and decide how best _you_ like to look at the images. Also play with the mouse wheel: you can zoom and pan, which is great for looking at itty bitty little spots.

## An Aside: Files

DIALS creates two principal file types:

- experiment files called `something.expt`
- reflection files called `something.refl`

"Experiment" in DIALS has a very specific meaning - the capturing of data from one set of detector, beam, goniometer and crystal - so if you have two scans from one crystal this is two experiments, if you have two lattices on one data set this is two experiments. In most cases you can ignore this distinction though.

Usually the output filenames will correspond to the name of the DIALS program that created them e.g. `indexed.refl` and `indexed.expt` from `dials.index`. The only deviations from this are on import (see below) where we are only reading experiment models and spot finding where we find _strong_ reflections so write these to `strong.refl` - and we create no models so (by default) there is no output experiment file.

At any time you can _look_ at these files with `dials.show` which will summarise the content of the files to the terminal.

## Spot Finding

Mostly the spot finding is automatic, assuming you do not have either very special beam characteristics or an experimental detector (neither apply for us here at NE-CAT): `dials.find_spots imported.expt`. Now you're computer's fans will spin up - this is one of the more computationally expensive steps.

After a little while you will see the spot finder summary which looks like this:

```console
Extracted 115807 spots
Removed 43692 spots with size < 3 pixels
Removed 3 spots with size > 1000 pixels
Calculated 72112 spot centroids
Calculated 72112 spot intensities
Filtered 71205 of 72112 spots by peak-centroid distance

Histogram of per-image spot count for imageset 0:
71205 spots found on 1800 images (max 1382 / bin)
              *****                         ******* *       
         ************                   ****************** *
************************ ****** **  ************************
************************************************************
************************************************************
************************************************************
************************************************************
************************************************************
************************************************************
************************************************************
1                         image                         1800

--------------------------------------------------------------------------------
Saved 71205 reflections to strong.refl
```

This shows an ASCII art histogram of the spots / rotation angle. If you have a full turn of data you should hopefully get back to where you started. Already a lot of pathologies can be spotted at this stage, but this is boring data so there is nothing fun to see. You can now also look at the spot finding results in the image viewer to get a sense of what it has done, with:

```bash
dials.image_viewer imported.expt strong.refl
```

Which should look like:

![Spots found view](./spots-found.png)

In the general sense you can look at _any_ `.expt` and `.refl` combo in the image viewer. There are other views to consider as well.

## The Reciprocal Lattice

While the image viewer is useful for individual or small numbers of frames, to look at the data set as a whole we can look at where these spots map to in reciprocal space - this is also an _excellent_ verification of your experimental geometry. Run: `dials.reciprocal_lattice_viewer imported.expt strong.refl` to see:

![Reciprocal lattice view](./reciprocal-lattice-0.png)

This shows where the spots are in reciprocal space: the further away from the centre of the view, the higher the resolution. If you have anisotropy it will be evident here, as will ice rings as they form spherical shells. For us here we have a fairly spherical fuzzy blob with a really obvious ring in - this is the inter-module gap on the detector. You can move this view around to get a feel for the lattice. With some fidding with the mouse you can see the lattice planes nicely:

![Reciprocal view 1](./reciprocal-lattice-1.png)

The lattice lines are still a little squiggly because we have not refined the geometry yet, but the single lattice is clear. For the record I usually use this as either an education tool or for diagnostics, either beamline / instrumentation or working out why the data are not processing well.

## Indexing

The next useful step in processing is indexing: in DIALS this only worries about assigning a triclinic model by default though you can enforce symmetry if you know it (though it does not make that much difference).

```bash
dials.index imported.expt strong.refl
```

and some time will pass and a lot of words and numbers will be printed. Only really the stuff at the end matters:

```console
RMSDs by experiment:
+-------+--------+----------+----------+------------+
|   Exp |   Nref |   RMSD_X |   RMSD_Y |     RMSD_Z |
|    id |        |     (px) |     (px) |   (images) |
|-------+--------+----------+----------+------------|
|     0 |  36000 |  0.27885 |  0.25813 |     0.2302 |
+-------+--------+----------+----------+------------+

Refined crystal models:
model 1 (68909 reflections):
Crystal:
    Unit cell: 67.1980(14), 67.1782(14), 67.1619(13), 109.4179(3), 109.4693(3), 109.4854(4)
    Space group: P 1
    U matrix:  {{-0.1560,  0.2049,  0.9663},
                {-0.1068, -0.9760,  0.1897},
                { 0.9820, -0.0736,  0.1742}}
    B matrix:  {{ 0.0149,  0.0000,  0.0000},
                { 0.0053,  0.0158,  0.0000},
                { 0.0091,  0.0091,  0.0182}}
    A = UB:    {{ 0.0076,  0.0120,  0.0176},
                {-0.0050, -0.0137,  0.0035},
                { 0.0158,  0.0004,  0.0032}}
+------------+-------------+---------------+-------------+
|   Imageset |   # indexed |   # unindexed |   % indexed |
|------------+-------------+---------------+-------------|
|          0 |       68909 |          2294 |        96.8 |
+------------+-------------+---------------+-------------+
```
