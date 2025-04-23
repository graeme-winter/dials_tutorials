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

To keep things simple first look at a _boring_ data set: `insulin_042225_15_1_00####.cbf.bz2`. With any processing with DIALS the first thing you do is _import_ the data: this reads the headers to make sense of the data set & also explains to _you_ what it found so you can make sense of it.
