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

we will come back to this in a minute. Right now, take a few minutes to play with the settings and decide how best _you_ like to look at the images.
