# Spot Finding

The DIALS spot finding has two algorithms which can be used: the basic dispersion spot finding and "dispersion extended" which is not documented anywhere. My intention here is to document both of these including the second, achieved by reverse-engineering the algorithm itself.

N.B. the documentation exlpains _what_ it does with my best understanding of _why_. I do not claim that what it does it correct. The basic spot finding algorithm is based on our understanding of what XDS does: the more advanced dispersion extended one was added in [this PR](https://github.com/dials/dials/pull/758) but I don't think the text describing the algorithm is actually 100% correct.

## Spot Finding

The essence of any spot finding in DIALS is to classify spots into either "background" or "signal" - background pixels are where nothing interesting is happening, signal pixels are statistically surprising i.e. the distribution of pixel values does not correspond to background. In the case of a photon counting detector (which this description exclusively considers) the variance in a region of background is closely related to the mean as the values should form a Poisson distribution. If the local mean and variance are similar, then the data are behaving as background. If the variance is significantly greater than the mean, then there is a non-Poissonian distribution and something interesting to explore.

In all cases the general flow of spot finding is:

- read data, assess whether pixel has a valid or invalid value (i.e. it is known _a priori_ to be reliable or otherwise) - typically this then results in a pixel value `p` and a mask value `m` where `m=0` indicates that the pixel is invalid, `m=1` is valid
- compute the pixels which are background, then derive the pixels which do not belong to this background giving a signal pixel list
- combine the signal pixels into spots, by finding the 4-connected regions i.e. pixels where one above or to the left on am image, or at the same postion on the previous image for rotation scans, are also signal
- filter the spot list based on criteria such as minimum number of pixels, spacing between the pixel centroid and the highest pixel in the spot etc. (I am not convinved that the scond of these is a good criterion)
- extract the spot centroids, ideally background subtracted, and the bounding pixels and pixel values into a spot list tobe stored in a reflection file

In the general sense the images are sparse i.e. the number of pixels wih signal in is relatively small. The objects themselves are also typically small i.e. we assume a few pixels to a side, such that objects are not considered as crossing module boundaries: spot finding on individual modules should give equivalent results to spot finding on full image.

The dispersion and dispersion extended spot finding differ only on the classification step i.e. which pixels are signal, which are background: the connected component analysis which follows is identical.

## Dispersion Spot Finding

In dispersion spot finding the mean and variance of a sliding window are calculated, then this is used to assess whether any pixels withinb this region have a surprising value, by exceeding some threshold in terms of deviation from the mean. Typically the CPU based implementation will use integral images (also known as summed area tables) of the pixel mask values, the pixel values and the squared pixel values to compute the local mean and variance of valid pixel values in a sliding window, typically 7x7 pixels. The mean and variance are then used to threshold the pixels as firstly _non background_ before tesing if they pass as a strong signal pixel: these have multipliers (`sigma_b` and `sigma_s`, with default values of 6 and 3 respectively.) 

### Background

The measure of the background threshold is essentially asking if the pixels in he kernel region follow a Poisson distribution i.e. the variance is similar to the mean. In the DIALS code this is re-arranged in terms of the sum of mask values (`m_sum`) the sum of pixels (`i_sum`) and the sum of squared pixel values (here `i2_sum`: note the DIALS source code confusingly calls these m, x and y respectively and also keeps them in a struct so they are near to one another.) The condition for the _pixel_ to be classed as not-background is that the surrounding region has the inequality `X > T` where

`X = m_sum * i2_sum - i_sum * i_sum - i_sum * (m_sum - 1)`

and

`T = i_sum * sigma_b * sqrt(2 * (m_sum - 1))`

If a pixel `p` is excluded from being background it can be tested whether it is _strong_ i.e. significantly above the mean and variance of the local population with another inequality: `Y > S` where

`Y = p * m_sum - i_sum`

and

`S = sigma_s * sqrt(i_sum * m_sum)`

If both of these conditions are satisfied the pixel is strong and will be recorded for later grouping.
