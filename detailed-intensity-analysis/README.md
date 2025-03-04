# Intensity Analysis using DIALS

One of the joys of DIALS is the ability to do custom things with intermediate processing results, for example looking for trends in the scaled but unmerged data across a number of data sets. As an example, wanting to see e.g. how the signal to noise of the data (I/σ(I)) varies across a number of nominally equivalent data sets.

To do this, start with the processed results of the [🐮🐷🧓 data](../ccp4-aps-2024/COWS_PIGS_PEOPLE.md)...

## DIALS Python Scripts

Assuming you have a relatively recent DIALS install you should be able to run everything with _either_ a vanilla `python3` shell _or_ `dials.python` - if the latter exists, it will work, otherwise in the former if you have any problems, check that you have your DIALS environment configured.

The main intermediate results in DIALS are the reflection (`.refl`) and experiment (`.expt`) files. These are discussed extensively [elsewhere](../ccp4-aps-2024/README.md). Here we will peer into the results of some processing to do some lightweight analysis: you can do far more advanced things than I am showing here, but the intention is that this is introductory.

## DIALS Command Line Tools

Before getting too stuck into the Python API, it is worth looking at the data with some of the command line tools notably `dials.show`: this will tell you many useful things like the unit cell of your crystals, the experimental geometry etc.

```console
dials.show scaled.refl
```

will show _a lot_ of output - this is just the tail end:

```console
Experiment 11:
Experiment identifier: f6a74085-64ac-b9aa-9b77-70ab0b9a6e72
Image template: /Users/graeme/data/cows-pigs-people/data/CIX15_1_#####.cbf.gz
Detector:
Panel:
  name: Panel
  type: SENSOR_PAD
  identifier: PILATUS3 6M, S/N 60-0119
  pixel_size:{0.172,0.172}
  image_size: {2463,2527}
  trusted_range: {0,91798}
  thickness: 0.45
  material: Si
  mu: 4.20638
  gain: 1
  pedestal: 0
  fast_axis: {0.999917,0.0128412,0.000502715}
  slow_axis: {0.0128436,-0.999904,-0.00511264}
  origin: {-225.3,222.967,-198.598}
  distance: 199.639
  pixel to millimeter strategy: ParallaxCorrectedPxMmStrategy
    mu: 4.20638
    t0: 0.45


Max resolution (at corners): 1.033440
Max resolution (inscribed):  1.300337

Beam:
    probe: x-ray
    wavelength: 0.99987
    sample to source direction : {-0,-0.00135723,0.999999}
    divergence: 0
    sigma divergence: 0
    polarization normal: {0,0.999999,0.00135723}
    polarization fraction: 0.999
    flux: 0
    transmission: 1
    sample to source distance: 0

Beam centre: 
    mm: (222.42,225.57)
    px: (1293.14,1311.48)

Scan:
    number of images:   100
    image range:   {1,100}
    epoch:    1.71534e+09
    exposure time:    0.009
    oscillation:   {0,0.1}

Goniometer:
    Rotation axis:   {0,1,0}
    Fixed rotation:  {1,0,0,0,1,0,0,0,1}
    Setting rotation:{1,0,0,0,1,0,0,0,1}
    Axis #0 (GON_OMEGA):  {0,1,0}
    Angles: 0
    scan axis: #0 (GON_OMEGA)

Crystal:
    Unit cell: 77.858, 77.858, 77.858, 90.000, 90.000, 90.000
    Space group: I 2 3
    U matrix:  {{-0.5537,  0.1131, -0.8250},
                {-0.2210,  0.9352,  0.2765},
                { 0.8029,  0.3354, -0.4928}}
    B matrix:  {{ 0.0128,  0.0000,  0.0000},
                {-0.0000,  0.0128,  0.0000},
                { 0.0000,  0.0000,  0.0128}}
    A = UB:    {{-0.0071,  0.0015, -0.0106},
                {-0.0028,  0.0120,  0.0036},
                { 0.0103,  0.0043, -0.0063}}
    A sampled at 101 scan points
  Average unit cell: 
Profile model:
    type: gaussian_rs
    delta_b (sigma_b): 0.133894 (0.044631)
    delta_m (sigma_m): 0.141251 (0.047084)
Scaling model:
  type : physical
  Scale component:
    parameters (sigma)
     1.1016   (0.0143)
     1.0247   (0.0079)
     1.0194   (0.0073)
     0.9800   (0.0075)
     0.9585   (0.0152)
  Decay component:
    parameters (sigma)
     0.1208   (0.0450)
     0.2751   (0.0425)
     0.2043   (0.0462)
```

If you want to work with the data, showing the content of the _reflections_ is super helpful as this reminds you of all the data column names too:

```console
dials.show scaled.refl
```

Gives:

```console
DIALS (2018) Acta Cryst. D74, 85-97. https://doi.org/10.1107/S2059798317017235
The following parameters have been modified:

input {
  reflections = scaled.refl
}


Reflection list contains 412223 reflections
+-------------------------------+------------------------------------+---------------------------------------+------------------------------------+
| Column                        | min                                | max                                   | mean                               |
|-------------------------------+------------------------------------+---------------------------------------+------------------------------------|
| background.mean               | 0.0                                | 11.1                                  | 1.2                                |
| background.sum.value          | 4.2                                | 9016.0                                | 369.3                              |
| background.sum.variance       | 4.7                                | 11720.8                               | 436.2                              |
| d                             | 1.04                               | 55.14                                 | 1.77                               |
| flags                         | 8389377                            | 68190465                              | 58840062                           |
| id                            | 0                                  | 11                                    | 5                                  |
| imageset_id                   | 0                                  | 11                                    | 5                                  |
| intensity.prf.value           | -2885.8                            | 783585.1                              | 491.5                              |
| intensity.prf.variance        | -1.0                               | 784656.7                              | 816.0                              |
| intensity.scale.value         | -392825628198780224.0              | 381946923149443200.0                  | 1483707444518.7                    |
| intensity.scale.variance      | 0.4                                | 89120290316131689036578140582838272.0 | 33733286673738519231003652784128.0 |
| intensity.sum.value           | -159.6                             | 781766.6                              | 491.8                              |
| intensity.sum.variance        | 5.6                                | 783026.2                              | 955.5                              |
| inverse_scale_factor          | 0.193                              | 2.330                                 | 0.986                              |
| inverse_scale_factor_variance | 0.000                              | 0.001                                 | 0.000                              |
| lp                            | 0.008                              | 1.661                                 | 0.657                              |
| miller_index                  | -72, -69, -71                      | 72, 70, 68                            | -1, 1, -2                          |
| num_pixels.background         | 65                                 | 23280                                 | 2658                               |
| num_pixels.background_used    | 65                                 | 23280                                 | 2658                               |
| num_pixels.foreground         | 25                                 | 3536                                  | 423                                |
| num_pixels.valid              | 99                                 | 25932                                 | 3081                               |
| original_index                | 0.0                                | 37324.0                               | 17489.85864447156                  |
| panel                         | 0                                  | 0                                     | 0                                  |
| partial_id                    | 0                                  | 459227                                | 229077                             |
| partiality                    | 0.0000                             | 1.0000                                | 0.8214                             |
| profile.correlation           | -0.011                             | 0.993                                 | 0.605                              |
| qe                            | 0.849                              | 0.971                                 | 0.910                              |
| s1                            | -0.7437, -0.7234, -1.0000          | 0.7094, 0.7489, -0.5358               | -0.0352, 0.0114, -0.7821           |
| xyzcal.mm                     | 0.55, 0.62, -0.02                  | 423.14, 434.09, 0.19                  | 211.56, 221.43, 0.09               |
| xyzcal.px                     | 2.39, 2.83, -10.00                 | 2460.83, 2524.51, 110.00              | 1229.96, 1287.37, 50.11            |
| xyzobs.mm.value               | 0.66, 0.76, 0.00                   | 423.00, 433.93, 0.17                  | 211.56, 221.43, 0.09               |
| xyzobs.mm.variance            | 0.0000e+00, 0.0000e+00, 0.0000e+00 | 9.4165e-01, 6.4161e-01, 8.5676e-07    | 4.9412e-03, 4.5721e-03, 3.0571e-07 |
| xyzobs.px.value               | 3.07, 3.62, 0.50                   | 2460.00, 2523.63, 99.50               | 1229.96, 1287.38, 50.02            |
| xyzobs.px.variance            | 0.0000, 0.0000, 0.0000             | 31.8299, 21.6878, 0.2813              | 0.1670, 0.1545, 0.1004             |
| zeta                          | -1.000                             | 1.000                                 | -0.046                             |
+-------------------------------+------------------------------------+---------------------------------------+------------------------------------+
```

Critically this also gives hints about the data types, e.g, scalar columns or vector ones.

## Python Script

A useful Python script is:

```python
# flex arrays are like numpy arrays
from dials.array_family import flex

# ExperimentList represents all the standard dials "models" - stuff like
# crystals, beams, ...
from dxtbx.model.experiment_list import ExperimentList

# some useful tools from scaling which will help our analysis here
from dials.algorithms.scaling.Ih_table import map_indices_to_asu

# here we are just reading the files from typical dials processing
expts = ExperimentList.from_file("scaled.expt")
refls = flex.reflection_table.from_file("scaled.refl")

# here we are selecting the _good_ reflections - these are the ones
# which are flagged as (i) having been scaled and (ii) _not_ flagged as
# having been bad for scaling - the flags are packed into a bit array
# - then we _invert_ the selection of bad for scaling reflections with ~
refls = refls.select(refls.get_flags(refls.flags.scaled))
refls = refls.select(~refls.get_flags(refls.flags.bad_for_scaling, all=False))

# map the reflections to the asymmetric unit, make a new column with
# the unique Miller index as asu_miller_index
space_group = expts[0].crystal.get_space_group()
refls["asu_miller_index"] = map_indices_to_asu(refls["miller_index"], space_group)

# now we can iterate through the experiments
for j, expt in enumerate(expts):
    
    # if we want properties of the crystal like the unit cell or space group, 
    # we can get them (but we are not using them here)
    xtal = expt.crystal
    cell = xtal.get_unit_cell().parameters()
    space_group = expt.crystal.get_space_group()

    # now we can select the reflections which belong to _this_ experiment
    data = refls.select(refls["id"] == j)

    # print some commentary (not functional)
    print(f"For experiment {j} there are {data.size()} reflections")

    # now we can gather the _unique_ reflections by looking at the unique set
    # of Miller indices: created by making this into a Python set
    uniq = set(data["asu_miller_index"])

    # now extract the _scaled_ I and σ(I) values from the data - in DIALS we 
    # store the variance not the standard deviation, so need to sqrt() the values
    i = data["intensity.scale.value"] / data["inverse_scale_factor"]
    s = flex.sqrt(data["intensity.scale.variance"]) / data["inverse_scale_factor"]

    # compute the mean I/σ(I)
    i_s = flex.mean(i / s)
    
    print(f" of which {len(uniq)} are unique with average I/σ(I) of {i_s}")
```

This is commented and can run as it is, to tell you a few things about each of the 12 data sets, but here I will break it down some more to discuss what's what.

### Imports

The imports at the top of the file.

```python
from dials.array_family import flex
from dxtbx.model.experiment_list import ExperimentList
from dials.algorithms.scaling.Ih_table import map_indices_to_asu
```

These are importing:

- fundamental data types for working with DIALS data: `flex` arrays and experiment models
- an example algorithm (there are a great many) pulled from part of the scaling code

As a warning: sometimes these things don't seem immediately obvious, because _they are not_ - there is much which is weird and idiosyncratic in the DIALS code base. For the record, `flex` arrays fit in the same spot as e.g. `numpy` arrays and you can cheaply map from one to another with `flumpy` (a document for another day.)

### Reading and Filtering Data

The reading of the data files happens in:

```python
expts = ExperimentList.from_file("scaled.expt")
refls = flex.reflection_table.from_file("scaled.refl")
```

You can work straight from here, but this will include some data we probably don't want so we filter out the good stuff with:

```python
refls = refls.select(refls.get_flags(refls.flags.scaled))
refls = refls.select(~refls.get_flags(refls.flags.bad_for_scaling, all=False))
```

This selects the data that are flagged as _scaled_ then removes the ones which are bad for scaling by selecting only those which are _not_ bad for scaling (`~` is a negation.) At this point, we have:

- all our experiments from the data set
- all the reflections which belong to those experiments

So, let's do something useful.

### Something Useful 1: Adding New Columns

One of the great things about reflection tables is being able to add new columns with derived information. Here, we want to e.g. compute the I/σ(I) for data sets for each experiment, and work out the average multiplicity of the data: this involves working out the reduced Miller index for all the reflections:

```python
space_group = expts[0].crystal.get_space_group()
refls["asu_miller_index"] = map_indices_to_asu(refls["miller_index"], space_group)
```

Of course, this assumes that all the data have the same space group... but we can assume that for now. This creates a new column in our reflection table called `asu_miller_index` that we can treat the same way as any other column (even though, in this case, the column is a column of _vectors_.)

### Looking at Experiments

One of the things we may want to do is printing all the unit cells, even though we could do that with `dials.show` as above. In that case we would only need the experiments, and would iterate through them with e.g.:

```python
for j, expt in enumerate(expts):
    xtal = expt.crystal
    cell = xtal.get_unit_cell().parameters()
    space_group = expt.crystal.get_space_group()

    print(f"For experiment {j} the cell is {cell} with space group {space_group}")
```

This is not interesting, but starts to show how you could explore: putting a `help(expt)` or `help(xtal)` in here will allow you to probe the models in a friendly environment. More usefully though we are supposed to be working with the intenities...

### Working with Intensities

To access the intensities for each experiment involves selecting the ones with the correct `id` value in the column:

```python
for j, expt in enumerate(expts):
    data = refls.select(refls["id"] == j)

    uniq = set(data["asu_miller_index"])

    i = data["intensity.scale.value"] / data["inverse_scale_factor"]
    s = flex.sqrt(data["intensity.scale.variance"]) / data["inverse_scale_factor"]
    i_s = i / s
    
    print(f"For experiment {j} there are {data.size()} reflections")
    print(f" of which {len(uniq)} are unique with average I/σ(I) of {flex.mean(i_s)}")
```

Here we are iterating through the experiments and selecting the reflections which belong to each. We can then take the intensities and variances and correct them as done in the scaling, taking the `sqrt` to get the standard deviation - the `flex` array `i_s` contains the I/σ(I) value for each observation, so printing the mean is simple.

## Moving On

There is far more you can do from here, but this shows the essence of working with the data files in DIALS. For convenience the [full script is included](./rachel_example.py).
