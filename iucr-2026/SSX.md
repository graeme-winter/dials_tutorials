# Synchrotron Serial Crystallography

## Introduction

Synchrotron serial crystallography (SSX) data may be processed with DIALS _either_ through running through the command sequence in a similar way to the [more prosaic tutorials](./WORKFLOW.md) or through [xia2](https://gist.github.com/jbeilstenedmands/34c99139a64efa10e956d26f0a4483e7). Both offer advantages: in this tutorial the former will be explored first, to understand the _process_ of data analysis, before introducing the latter which largely automates many of the key steps.

## Workflow

For reference, the workflow for processing a simple rotation data set is:

```console
import → find spots → index → refine → integrate → symmetry → scale
```

For a many crystal data set we have:

```console
import → find spots → index → refine → integrate ↘
import → find spots → index → refine → integrate ↘
import → find spots → index → refine → integrate ↘
import → find spots → index → refine → integrate → symmetry → scale
import → find spots → index → refine → integrate ↗
import → find spots → index → refine → integrate ↗
import → find spots → index → refine → integrate ↗
```

Where each of the "runs" are treated independently until they are merged - even if they are run as an ensemble. Obviously if they are run independently then it is possible that inconsistent unit cells will appear in indexing so it is more truthful to present the latter as:

```console
import → find spots → index ↘        ↗ re-index → refine → integrate ↘
import → find spots → index ↘        ↗ re-index → refine → integrate ↘
import → find spots → index ↘        ↗ re-index → refine → integrate ↘
import → find spots → index → review → re-index → refine → integrate → symmetry → scale
import → find spots → index ↗        ↘ re-index → refine → integrate ↗
import → find spots → index ↗        ↘ re-index → refine → integrate ↗
import → find spots → index ↗        ↘ re-index → refine → integrate ↗
```

Here, the `review` step is where the unit cells for each run are inspected and a "guess" made as to the most likely set of parameters, whch are then provided as input to the `re-index` step. The `symmetry` determination step here is implemented with `cosym`, which simultaneously resolves the determination of the crystal symmetry and the potential indexing ambiguity between sweeps.

An assumption going into this analysis however is that the unit cells and experimental geometry can be well refined for each sweep, so can be treated as effectively independent: the radius of convergence is typically also generous, so we don't need to worry too much about re-cycling the geometrical parameters. For SSX data these are both false.

## SSX Workflow

The workflow for SSX essentially assumes that the experimental geometry encoded in the headers is good enough to get started, but will need some optimisation: the first "phase" of the analysis is therefore a bootstrap process, where we learn a little about the data set from a subset of the measurements and tune some of the parameters. As an example, of (say) 19,200 frames it may be typical to use 1,000 for this. The start of the workflow looks similar to the simple case above:

```console
import → find spots → index
```

A nuance here, however, is that we use `dials.ssx_index` which is optimised for the problem of indexing unique patterns on each image independently. The start of the workflow is therefore:

```console
import → find spots → ssx_index → review
```

The `review` step here is made easier by `ssx_index` providing a summary of the frequency of the most common unit cell parameter clusters:

```console
Cluster_id       N_xtals  Med_a         Med_b         Med_c         Med_alpha    Med_beta     Med_gamma   Delta(deg)
357 in P 1.
cluster_01       357      96.80 (0.30 ) 96.68 (0.24 ) 96.68 (0.31 ) 90.00 (0.27) 89.94 (0.34) 89.99 (0.30)
      P m -3 m (No. 221)  96.72         96.72         96.72         90.00        90.00        90.00         0.086 
80 in P 1.
cluster_02       80       96.62 (0.37 ) 136.85(0.52 ) 136.84(0.71 ) 89.90 (0.34) 90.00 (0.37) 90.08 (0.35)
     P 4/m m m (No. 123)  136.85        136.85        96.62         90.00        90.00        90.00         0.13  
51 in P 1.
cluster_03       51       96.81 (0.38 ) 96.68 (0.33 ) 193.19(0.74 ) 89.98 (0.32) 89.98 (0.37) 89.89 (0.26)
     P 4/m m m (No. 123)  96.75         96.75         193.19        90.00        90.00        90.00         0.11  
46 in P 1.
cluster_04       46       136.88(0.47 ) 136.71(0.48 ) 136.79(0.43 ) 75.18 (24.54) 89.63 (24.47) 77.76 (28.42)
      I 1 2/m 1 (No. 12)  136.71        192.88        197.18        90.00        111.64       90.00         1.9   
```

Here we can see that the most common cluster contains a cubic-looking unit cell with multiples of those same parameters appearing later. We can therefore take a guess that the correct unit cell is cubic with ⍺⩬96.7Å. Re-running the index step (without even constraining the unit cell to _be_ cubic, just giving that cell as an initial guess) nearly doubles the number of indexed crystals.
