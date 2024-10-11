# Processing 🐮🐷🧑‍🦳 with DIALS (CCP4 / APS 2024)

## Introduction

DIALS data processing may be run by automated tools such as `xia2` or interactively on the command line. For a tutorial it is more useful to use the latter, to explain the opportunities afforded by the software. In any data processing package the workflow requires reading data, finding spots, indexing to get an orientation matrix, refinement, integration and then scaling / correction: DIALS is no different.

This tutorial deviates slightly from the mainstream by _starting_ with data from a number of crystals, first from a single sample type and then from a mixture, which will show you how to classify data with subtle differences (e.g. presence or absence of a ligand.)

## The Data

[The data](https://zenodo.org/records/13890874) were taken on i24 at Diamond Light Source as part of routine commissioning work, with a number of data sets recorded from micro-crystals mounted on meshes. Crystals were prepared of the protein insulin from cows, pigs and people (as described on the Zenodo deposition; bovine, porcine and human insulin, of course all grown in e-coli anyway).

## The Workflow

The [workflow](../se-thaumatin/processing_in_detail.md) is the same with one data set as with many, with some small deviations - data from multiple crystals will not in general share an orientation matrix so the indexing will need to _not_ join all the lattices.

As mentioned above the flow is to read the data, find spots, index, refine, integrate and then derive some corrections from symmetry related reflections, which involves assigning the symmetry. In DIALS we use the following tools:

- `dials.import` - read all the image headers to make sense of the metadata
- `dials.find_spots` - find the spots - with DIALS we find spots across the whole data set and one spot across multiple images is "found" in 3D
- `dials.index` - assign indices to the spots and derive unit cell, symmetry
- `dials.refine` - improve the models from indexing (separate as allows "wobbles")
- `dials.integrate` - measure the background subtracted spot intensity
- `dials.symmetry` - derive the Patterson symmetry of the crystal from the data
- `dials.scale` - correct the data for sample decay, overall scale from beam or illuminated volume and absorption
- `dials.export` - output processed data for e.g. use in CCP4 or PHENIX



