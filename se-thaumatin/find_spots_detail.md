# Find Spots (detail)

## Input


## Output

The output of spot finding shows the number of strong _pixels_ found on every image and then at the end shows an overall summary:

```
Extracted 405471 spots
Removed 123788 spots with size < 3 pixels
Removed 34 spots with size > 1000 pixels
Calculated 281649 spot centroids
Calculated 281649 spot intensities
Filtered 234130 of 281649 spots by peak-centroid distance

Histogram of per-image spot count for imageset 0:
234130 spots found on 1800 images (max 4530 / bin)
*     ******                                                
********************              **********             ***
*************************** ************************ *******
************************************************************
************************************************************
************************************************************
************************************************************
************************************************************
************************************************************
************************************************************
1                         image                         1800

--------------------------------------------------------------------------------
Saved 234130 reflections to strong.refl
```

This "ascii-art" graph can be useful to give you an overall indication
of how the data look. If, as here, the graph is approximately constant
you may assume that the sample has not suffered substantial radiation
damage and was reasonably well centred. If there are sinusoidal
variations this may indicate either a variation in diffraction
strength (e.g. anisotropy) or a significant variation in the unit cell
lengths (i.e. when a long axis is perpendicular to the beam there are
more spots.)

This summary also shows how many reflections were excluded for being
too small or too large - usually the defaults are sensible however,
but you can adjust these with `min_spot_size` and `max_spot_size`.

This is also interesting:

```
Filtered 234130 of 281649 spots by peak-centroid distance
```

If you look at the images you will see in the default spot finding that there are quite a few "missed" reflections - spots wihich were not found. By default the spot finding in DIALS also filters on the distance between the highest pixel and the centre of mass (with the `max_separation` parameter). In this case a lot of spots have _failed_ this test, as in fact the crystal was split: this is visible in the reciprical lattice viewer, by looking at the unindexed reflections which appear to fall along lines of indexed reflections.

If we relax the `max_separation` parameter then many more spots are found but the number of indexed reflections will not increase that much: allowing a second lattice to be indexed increases the number of indexed reflections but - importantly - _not usefully_. The crystal lattice is still essentially "single" with more complex reflection profiles which are actually handled correctly in integration (i.e. all of the intensity is measured) hence it is probably better at this stage to ignore the details and continue.
