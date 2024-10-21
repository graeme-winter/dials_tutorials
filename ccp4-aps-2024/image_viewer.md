# Image Viewer

The DIALS image viewer can show a lot of useful diagnostic information: if you run with just the data i.e. `dials.image_viewer imported.expt` then you can walk through the steps of spot finding or look at the data / mask. If, however, you include the reflection data you can also look at the pixel classification from spot finding or the integration shoeboxes.

## From Spot Finding

If you run `dials.image_viewer imported.expt strong.refl` after `dials.find_spots` you can see:

- the reflection bounding boxes (blue)
- the "signal" pixels - marked with a green dot
- the centre of mass of the spot (red cross)

If you enable "show mask" you can also see those pixels which are excluded because (i) insensitive or (ii) already masked as they are known to be bad.

## From Indexing

If you have data from indexing then the bounding box will depend on the lattice number: for a multi-sweep experiment, or if you have multiple lattices on a single image set, you will see different colour boxes. You can also select "show HKL" to indicate the Miller indices, or "indexed only" to include only those spots which have been indexed. Looking at the results from refinement is essentially the same.

## From Integration

With the integration data you instead see the integration bounding boxes on the images, which are much larger as these include the background region. Frequently these will overlap with one another slightly if the spots become close together. If they overlap substantially there may be problems with these data e.g. a mosaic crystal or detector too close to the sample.

[Return to main tutorial](./README.md)
