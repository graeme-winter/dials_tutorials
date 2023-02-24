# Many Crystal Data Processing

In the earlier tutorials where we process one data set at a time. DIALS will however let you carry through a collection of data sets as an _ensemble_. This could be multiple data sets from a single sample at different orientations (for example with a multi-axis goniometer) or multiple nominally similar samples which you wish to merge.

To DIALS these are _the same_ as processing a single data set: there are only very minor deviations in the usual workflow, and a slightly greater requirement on the operator to pay attention to what is going on.

## Multi-sweep vs. multi-crystal

The only real distinction between multi-sweep and multi-crystal data sets from the point of view of DIALS is whether or not there is a common orientation matrix between the sweeps: the question of isomorphism, which data sets should be included and which should not etc. are down to the user (i.e. you) though there are dials tools to give you some useful hints along the way.

## Workflow

The basic workflow is the same for multiple data sets as it is for single ones, with two nuances. The first is that importing all the data at once and indexing each run separately may give inconsistent results, so you as a user may want to make some choices after indexing. Once the data have been scaled you may want to remove some of the input data sets, which is obviously impossible for a single scan data set.

## Data

The data for this tutorial are [on zenodo](https://zenodo.org/record/7085897) - as a convenience there is a tool for fetching data from zenodo:

```bash
Ethics-Gradient i24-ins :) $ pip install zenodo-get
Ethics-Gradient i24-ins :) $ zenodo_get -r 7085897
Title: Multi-crystal cubic insulin example data set recorded on i24
Keywords: x-ray diffraction, diamond light source, cubic insulin, multi-crystal data set
Publication date: 2022-09-16
DOI: 10.5281/zenodo.7085897
Total size: 6178.9 MB
```

... time passes ... the data appear in the working directory. As an alternative you can run this script:

```bash
curl -o fetch-7085897.sh https://gist.githubusercontent.com/graeme-winter/858487c87eed54e12f962870d3643f5a/raw/92e0ba6771a1a4e4fdf4915be64003054c573e06/fetch-7085897.sh
bash -x fetch-7085897.sh
```

This will download the data required to run the tutorial. The data themselves consist of 24 x 5° cubic insulin data sets recorded on i24 at Diamond Light Source with a CdTe Eiger 2X 9M: there are "metadata" files which contain the mask etc., then data files and finally NeXus files which contain the actual experiment metadata which will be the input for this tutorial.

This download could well take an hour or so, and requires abourt 6GB of space.
