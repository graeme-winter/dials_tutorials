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
