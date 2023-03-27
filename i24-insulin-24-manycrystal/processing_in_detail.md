# Many Crystal Data Processing

In the earlier tutorials where we process one data set at a time. DIALS will however let you carry through a collection of data sets as an _ensemble_. This could be multiple data sets from a single sample at different orientations (for example with a multi-axis goniometer) or multiple nominally similar samples which you may wish to merge.

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

## Processing: Spot Finding

Ths works the same as we used for the `tl;dr` pipeline - import data and find spots, but this time _import many data sets_:

```
dials.import ../downloads/*nxs
```

This will take a couple of seconds then print out:

```
Ethics-Gradient demo :( $ dials.import ../*nxs
DIALS (2018) Acta Cryst. D74, 85-97. https://doi.org/10.1107/S2059798317017235
DIALS 3.dev.947-gd83b87046
The following parameters have been modified:

input {
  experiments = <image files>
}

--------------------------------------------------------------------------------
  format: <class 'dxtbx.format.FormatNXmxDLS.FormatNXmxDLS'>
  num images: 1200
  sequences:
    still:    0
    sweep:    24
  num stills: 0
--------------------------------------------------------------------------------
Writing experiments to imported.expt
```

(or something very similar). You can see we have 24 data sets in here each with 50 images, or 5°, so we have a total of 120° of data - but we have no idea how complete this is right now. Find some spots:

```
dials.find_spots imported.expt
```

In general this is pretty quick since every data set is tiny... you should not need to go back and redo this step, but susequent steps we may revisit.

## Processing: Indexing

Here is the first time we may consider running a step twice, but we can use the flexibility of the dials tool chain to make this relatively painless. Indexing first as before:

```
dials.index imported.expt strong.refl joint=false
```

Here we set `joint=false` to tell `dials.index` that the data sets don't share an orientation matrix - by default it will assume all the data come from one crystal with different goniometer settings (say). Usual indexing output follows about 24 times, which I won't copy here because it is very long. Because we are indexing in P1 you may not recognise the lattice shape, but if you watch carefully while processing you may see that one cell appears a lot. You don't need to pay attention however, because we can inspect the output very easily:

```
dials.show indexed.expt | grep "Unit cell"
```

Gives

```
Ethics-Gradient demo :) $ dials.show indexed.expt | grep "Unit cell"
    Unit cell: 67.79(3), 67.71(3), 67.759(19), 109.429(8), 109.532(9), 109.416(15)
    Unit cell: 67.692(13), 67.723(8), 67.760(7), 109.438(3), 109.511(6), 109.456(6)
    Unit cell: 67.692(4), 67.808(7), 67.734(3), 109.631(7), 109.400(6), 109.394(3)
    Unit cell: 67.717(8), 67.688(5), 67.700(12), 109.528(6), 109.371(9), 109.459(7)
    Unit cell: 67.66(6), 67.80(3), 67.70(3), 109.545(5), 109.373(15), 109.500(14)
    Unit cell: 67.70(3), 67.801(19), 67.769(18), 109.4989(19), 109.457(6), 109.476(10)
    Unit cell: 67.62(3), 67.64(3), 67.736(18), 109.482(7), 109.542(9), 109.354(13)
    Unit cell: 67.688(11), 67.667(15), 67.772(7), 109.476(11), 109.519(17), 109.366(11)
    Unit cell: 67.68(3), 67.75(2), 67.69(4), 109.539(9), 109.326(14), 109.500(8)
    Unit cell: 67.65(3), 67.736(17), 67.749(17), 109.4611(18), 109.470(7), 109.443(8)
    Unit cell: 67.666(4), 67.706(3), 67.751(3), 109.5027(12), 109.505(5), 109.454(3)
    Unit cell: 67.68(3), 67.71(3), 67.708(19), 109.421(11), 109.435(7), 109.485(13)
    Unit cell: 67.69(2), 67.727(18), 67.753(17), 109.449(4), 109.456(6), 109.524(11)
    Unit cell: 67.74(3), 67.75(2), 67.72(2), 109.455(7), 109.418(10), 109.529(13)
    Unit cell: 67.848(18), 67.80(3), 67.787(17), 109.460(7), 109.4822(19), 109.474(8)
    Unit cell: 67.859(12), 67.884(9), 67.845(9), 109.455(3), 109.424(16), 109.437(8)
    Unit cell: 67.658(6), 67.649(5), 67.672(5), 109.4692(15), 109.404(6), 109.580(4)
    Unit cell: 67.631(3), 67.655(3), 67.599(6), 109.578(2), 109.3383(16), 109.4352(14)
    Unit cell: 67.747(16), 67.78(3), 67.72(3), 109.645(13), 109.339(6), 109.449(9)
    Unit cell: 67.776(4), 67.770(4), 67.839(5), 109.4885(18), 109.527(4), 109.466(2)
    Unit cell: 67.80(3), 67.80(3), 67.844(18), 109.455(6), 109.442(9), 109.473(14)
    Unit cell: 67.76(4), 67.83(2), 110.69(3), 89.961(3), 89.943(9), 70.518(14)
    Unit cell: 67.61(2), 67.67(2), 67.722(14), 109.501(6), 109.467(6), 109.385(12)
```

Almost all of these are about 67,67,67,109,109,109 but some of them did not work quite right. Also, you may notice that there are only 23 rows, because one failed to index. However we now have some expectation omn what is the "right" answer, so let's use that information:

```
dials.index imported.expt strong.refl joint=false unit_cell=67,67,67,109,109,109
```

This is used as a starting point for the processing and will be subsequently refined. If you watch the output you will see that some of the sets are ~ 90% indexed, others about 60% and so on. Let's not worry too much here but there are probably multiple lattices in some of these sets. An exercise for the reader could be investigating this. Check output again with `dials.show` -

```
Ethics-Gradient demo :) $ dials.show indexed.expt | grep "Unit cell" 
    Unit cell: 67.824(6), 67.782(4), 67.817(4), 109.4474(11), 109.486(5), 109.529(4)
    Unit cell: 67.692(13), 67.723(8), 67.760(7), 109.438(3), 109.511(6), 109.456(6)
    Unit cell: 67.692(4), 67.808(7), 67.734(3), 109.631(7), 109.400(6), 109.394(3)
    Unit cell: 67.717(8), 67.688(5), 67.700(12), 109.528(6), 109.371(9), 109.459(7)
    Unit cell: 67.66(6), 67.80(3), 67.70(3), 109.545(5), 109.373(15), 109.500(14)
    Unit cell: 67.70(3), 67.801(19), 67.769(18), 109.4989(19), 109.457(6), 109.476(10)
    Unit cell: 67.62(3), 67.64(3), 67.736(18), 109.482(7), 109.542(9), 109.354(13)
    Unit cell: 67.686(11), 67.771(6), 67.767(7), 109.478(4), 109.486(14), 109.516(10)
    Unit cell: 67.67(3), 67.74(2), 67.75(2), 109.413(4), 109.538(9), 109.504(8)
    Unit cell: 67.62(3), 67.73(2), 67.718(16), 109.522(6), 109.452(8), 109.404(13)
    Unit cell: 67.666(4), 67.706(3), 67.751(3), 109.5027(12), 109.505(5), 109.454(3)
    Unit cell: 67.68(3), 67.71(3), 67.708(19), 109.421(11), 109.435(7), 109.485(13)
    Unit cell: 67.64(2), 67.686(18), 67.714(17), 109.446(4), 109.450(6), 109.545(11)
    Unit cell: 67.72(2), 67.76(2), 67.74(3), 109.528(14), 109.419(10), 109.456(7)
    Unit cell: 67.824(7), 67.864(6), 67.803(6), 109.4814(14), 109.457(5), 109.467(3)
    Unit cell: 67.859(12), 67.884(9), 67.845(9), 109.455(3), 109.424(16), 109.437(8)
    Unit cell: 67.644(5), 67.606(7), 67.654(9), 109.438(4), 109.588(3), 109.3586(17)
    Unit cell: 67.62(3), 67.59(5), 67.65(3), 109.589(17), 109.433(6), 109.333(13)
    Unit cell: 67.82(3), 67.754(16), 67.773(16), 109.6307(17), 109.434(8), 109.362(6)
    Unit cell: 67.772(4), 67.780(5), 67.842(6), 109.527(4), 109.4895(19), 109.4657(19)
    Unit cell: 67.80(3), 67.80(3), 67.844(18), 109.455(6), 109.442(9), 109.473(14)
    Unit cell: 67.68(3), 67.64(3), 67.73(2), 109.511(12), 109.473(7), 109.359(13)
    Unit cell: 67.83(4), 67.84(3), 67.90(2), 109.464(7), 109.514(9), 109.439(13)
    Unit cell: 67.62(2), 67.735(14), 67.723(14), 109.4923(8), 109.467(6), 109.477(6)
```

We now have 24 rows, all with the right cells, so we can now pick up the usual workflow (refine, integrate) though having a look at the reciprocal lattice viewer is fun. Select "crystal frame".

## Processing: Refine and Integrate

Precisely the same as the usual flow:

```
dials.refine indexed.refl indexed.expt
dials.integrate refined.refl refined.expt
```

With a _lot_ of text written.

I note at the end of refinement output:

```
RMSDs by experiment:
+-------+--------+----------+----------+------------+
|   Exp |   Nref |   RMSD_X |   RMSD_Y |     RMSD_Z |
|    id |        |     (px) |     (px) |   (images) |
|-------+--------+----------+----------+------------|
|     0 |   1097 |  0.32693 |  0.21546 |   0.11621  |
|     1 |   1745 |  0.28606 |  0.23142 |   0.16296  |
|     2 |    852 |  0.33914 |  0.22277 |   0.095315 |
|     3 |    414 |  0.2984  |  0.24746 |   0.19368  |
|     4 |    616 |  0.38176 |  0.21949 |   0.087365 |
|     5 |   1075 |  0.2712  |  0.23097 |   0.11563  |
|     6 |   1173 |  0.25273 |  0.22517 |   0.11882  |
|     7 |    394 |  0.29569 |  0.2544  |   0.21929  |
|     8 |   1311 |  0.36547 |  0.24697 |   0.16955  |
|     9 |   1396 |  0.28428 |  0.20668 |   0.089166 |
|    10 |    848 |  0.26028 |  0.25227 |   0.1787   |
|    11 |   1326 |  0.2702  |  0.23254 |   0.13247  |
|    12 |   1457 |  0.25631 |  0.21543 |   0.098179 |
|    13 |   1546 |  0.27731 |  0.23287 |   0.15222  |
|    14 |   1195 |  0.27129 |  0.22806 |   0.097633 |
|    15 |    189 |  0.21021 |  0.26237 |   0.21419  | <- this may not be so good
|    16 |   1141 |  0.29631 |  0.22824 |   0.11738  |
|    17 |   1220 |  0.42937 |  0.25279 |   0.17958  |
|    18 |   1415 |  0.28069 |  0.22886 |   0.09891  |
|    19 |    559 |  0.30719 |  0.28369 |   0.1695   |
|    20 |   1087 |  0.25108 |  0.23645 |   0.13212  |
|    21 |   1541 |  0.29062 |  0.24738 |   0.16129  |
|    22 |   1213 |  0.2702  |  0.23749 |   0.15287  |
|    23 |   1703 |  0.26258 |  0.21416 |   0.11408  |
+-------+--------+----------+----------+------------+
```

There are a couple with not-so-many reflections, these may not be as good as the neighbours. Remember we are looking for isomorphism, so we want them to all be similar.

## Procesing: Symmetry Determination

Each of these sets is 5° of data: if we look at each in isolation we won't have many symmetry related observations to combine, which makes it hard to assess symmetry. Instead we have a tool named [`dials.cosym`](http://scripts.iucr.org/cgi-bin/paper?S2059798318002978) which does something similar to the symmetry program but works on an ensemble of data sets. It also resolves any indexing ambiguity between various sets, and the paper linked gives details on how it does this.

```
dials.cosym integrated.refl integrated.expt
```

This is similar to the logic behind `dials.symmetry` but accounts for the fact that the crystals may be inconsistently indexed:

```
+--------------+--------+------+-----+-----------------+
|   likelihood |   Z-CC |   CC |     | Operator        |
|--------------+--------+------+-----+-----------------|
|        0.083 |   1.71 | 0.17 |     | 4 |(1, 1, 0)    |
|        0.083 |   1.71 | 0.17 |     | 4^-1 |(1, 1, 0) |
|        0.083 |   1.71 | 0.17 |     | 4 |(1, 0, 1)    |
|        0.083 |   1.71 | 0.17 |     | 4^-1 |(1, 0, 1) |
|        0.083 |   1.71 | 0.17 |     | 4 |(0, 1, 1)    |
|        0.083 |   1.71 | 0.17 |     | 4^-1 |(0, 1, 1) |
|        0.949 |  10    | 1    | *** | 3 |(1, 0, 0)    |
|        0.949 |  10    | 1    | *** | 3^-1 |(1, 0, 0) |
|        0.949 |  10    | 1    | *** | 3 |(0, 1, 0)    |
|        0.949 |  10    | 1    | *** | 3^-1 |(0, 1, 0) |
|        0.949 |  10    | 1    | *** | 3 |(0, 0, 1)    |
|        0.949 |  10    | 1    | *** | 3^-1 |(0, 0, 1) |
|        0.949 |  10    | 1    | *** | 3 |(1, 1, 1)    |
|        0.949 |  10    | 1    | *** | 3^-1 |(1, 1, 1) |
|        0.949 |  10    | 1    | *** | 2 |(1, 1, 0)    |
|        0.083 |   1.71 | 0.17 |     | 2 |(-1, 1, 0)   |
|        0.949 |  10    | 1    | *** | 2 |(1, 0, 1)    |
|        0.083 |   1.71 | 0.17 |     | 2 |(-1, 0, 1)   |
|        0.949 |  10    | 1    | *** | 2 |(0, 1, 1)    |
|        0.083 |   1.71 | 0.17 |     | 2 |(0, -1, 1)   |
|        0.083 |   1.71 | 0.17 |     | 2 |(1, 1, 2)    |
|        0.083 |   1.71 | 0.17 |     | 2 |(1, 2, 1)    |
|        0.083 |   1.71 | 0.17 |     | 2 |(2, 1, 1)    |
+--------------+--------+------+-----+-----------------+
```

```
Best solution: I m -3
Unit cell: (78.1965, 78.1965, 78.1965, 90, 90, 90)
Reindex operator: b+c,a+c,a+b
Laue group probability: 1.000
Laue group confidence: 1.000
Reindexing operators:
x,x-y,x-z: [2, 3, 4, 5, 7, 11, 12, 18, 20, 23]
x,y,z: [0, 1, 6, 8, 9, 10, 13, 14, 15, 16, 17, 19, 21, 22]
```

We now have data we can scale, and assess isomorphism for. Also take a look at the html report in `dials.cosym.html`

## Processing: Scaling

As before, simple scaling recipe (default) is probably fine:\

```
dials.scale symmetrized.refl symmetrized.expt
```

This will try and scale everything together, and report on the outcomes. First we will filter, then worry about resolution limits. Filter by computing the ∂-CC-half statistic - i.e. those which really are not contributing much to the end result:

```
dials.compute_delta_cchalf scaled.refl scaled.expt
```

```
Dataset: 15, ΔCC½: -8.617
Dataset: 7, ΔCC½: -1.426
Dataset: 3, ΔCC½: -0.995
Dataset: 19, ΔCC½: -0.214
Dataset: 5, ΔCC½: -0.107
Dataset: 9, ΔCC½: -0.028
Dataset: 16, ΔCC½: 0.058
Dataset: 4, ΔCC½: 0.115
Dataset: 20, ΔCC½: 0.135
Dataset: 14, ΔCC½: 0.138
Dataset: 6, ΔCC½: 0.140
Dataset: 13, ΔCC½: 0.147
Dataset: 17, ΔCC½: 0.188
Dataset: 22, ΔCC½: 0.189
Dataset: 18, ΔCC½: 0.217
Dataset: 12, ΔCC½: 0.299
Dataset: 23, ΔCC½: 0.316
Dataset: 21, ΔCC½: 0.359
Dataset: 8, ΔCC½: 0.361
Dataset: 11, ΔCC½: 0.368
Dataset: 2, ΔCC½: 0.436
Dataset: 1, ΔCC½: 0.486
Dataset: 0, ΔCC½: 0.504
Dataset: 10, ΔCC½: 0.858

mean delta_cc_half: -0.253
stddev delta_cc_half: 1.803
cutoff value: -7.465 

Removing dataset 15
Writing table to delta_cchalf.dat
Saving 200688 reflections to filtered.refl
Saving the experiments to filtered.expt
Writing html report to: compute_delta_cchalf.html
```

We see one is really bad, and it has automatically been excluded: we can re-use this with

```
dials.scale filtered.refl filtered.expt
```

This will over-write the old scaling results, beware, but shows that there is some flexibility in how the workflow can be used. Now the program will also recommend a resolution limit, so let's apply that:

```
dials.scale filtered.refl filtered.expt d_min=1.54
```

This gives us a completed data set, but does not include _everything_ we could have done...

## Processing: Automate with Multiplex

There is a tool included in `dials` to automate this: [`xia2.multiplex`](https://onlinelibrary.wiley.com/iucr/doi/10.1107/S2059798322004399).

```
mkdir multiplex
cd multiplex
xia2.multiplex ../integrated.refl integrated.expt min_completeness=0.9
```

This will do everything we did above, but more, in assessing which data sets are isomorphous in terms of intensities, group data sets, merge all clusters which look good and generally make your life a lot easier.
