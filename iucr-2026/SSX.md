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

Where each of the "runs" are treated independently until they are merged - even if they are run as an ensemble.
