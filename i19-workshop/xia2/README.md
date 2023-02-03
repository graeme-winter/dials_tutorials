# xia2

`xia2` as a command line tool is there to process your data when you have other things to do: it will in general make sensible decisions for you but it _won't_ tell you how your data are interesting, nor give you any real insight into what is going on. If your data are OK, it can be very effective in getting you from the diffraction images to `hkl` files in a compact period of time.

## Basic xia2 usage

In the simplest case (for small molecule data) you just run

```bash
xia2.small_molecule /dls/i19-2/data/2023/cy12345-6/foo/
```

(say) for data collected into a directory `/dls/i19-2/data/2023/cy12345-6/foo/`. This will do all the spot finding, indexing, refinement, integration, symmetry determination and scaling for you, and just give you a very light weight summary of the processing.

For the tutorial data this gives several blocks of output - spot finding from each of the four scans:

```
-------------------- Spotfinding SWEEP1 --------------------
1388 spots found on 900 images (max 39 / bin)
                      *                                *    
                      *                                *    
                      *    *  **    *          *       *    
*         *           * *  * ***  ***  ** ***  ***  * **    
* **   *  *     *     * * ****** ******************** ** *  
* **   * *****  * *** **************************************
**** *********  * ******************************************
**** ********* *********************************************
************************************************************
************************************************************
1                         image                          900
-------------------- Spotfinding SWEEP2 --------------------
1170 spots found on 849 images (max 29 / bin)
        *       *                                *          
        *       *     *  * **  * *    *    *  *  *          
    **  *** *   ** *  * ** *** * *   **   **  *  **   *     
    **  *** * * ** * ** ** ***** ****** * *** *  ** ***     
  * ** ****** **** * ************************ *  ** *** * **
  * ** *********** ************************** * *** *** * **
 ********************************************** ******* ****
******************************************************* ****
************************************************************
************************************************************
2                         image                          850
-------------------- Spotfinding SWEEP3 --------------------
1108 spots found on 848 images (max 28 / bin)
                   *       *                  *  *          
                   *    *  * *     *      * * *  *          
 *   *   *        **    *  *** **  *      * *** ***         
** * *   * * *    **    *  *** **  *    * * *** *** *  *   *
** ***** ******* *** ** *  *** ****** * * ********* * ***  *
**************** *** ***** ************ * ******************
************************** *********************************
************************** *********************************
************************** *********************************
************************************************************
1                         image                          848
-------------------- Spotfinding SWEEP4 --------------------
1060 spots found on 850 images (max 31 / bin)
                                                           *
     *                                                     *
*    *    * *       *     *    *                           *
*   ***   * *  ** * *   * *    *   *   *             *     *
*   *** *** *  ** * *  ** *    *  ***  *        *    ** ****
***************** * ***** ****** **** ** ** *** * *  ** ****
******************* ***** ****** ******* ************** ****
******************* ******************** *******************
************************************************************
************************************************************
1                         image                          850
```

If you see any gaps in here then it may be worth looking at the images. The indexing takes all four scans worth of spots, maps the data to reciprocal space then determines an orientation matrix which best explains them all. This is then asssessed for likely symmetry based on refinement against compatible Bravais lattice constraints (which I note is _different_ from the default `dials` route.) - the output here is very sparse:

```
---------------- Autoindexing SWEEPS 1 to 4 ----------------
All possible indexing solutions:
mP   4.09  11.23   9.86  90.00 100.68  90.00
aP   4.09   9.86  11.23  89.99  90.02  79.32
Indexing solution:
mP   4.09  11.23   9.86  90.00 100.68  90.00
```

All of the compatible lattices are outputted, and by default the highest symmetry one tested - this may later be eliminated by analysis of the intensities (but in this case turns out to be correct). Next the models are refined (which shows no output) and the data integrated. Modern data sets consist of hundreds or thousands of images, so `xia2` summarises the output of integration as one character per image e.g.

```
-------------------- Integrating SWEEP1 --------------------
Processed batches 2 to 901
Standard Deviation in pixel range: 0.03 1.39
Integration status per image (60/record):
ooooooooo.o.ooooooo.o.o.ooo..ooooooooooooooooooooooooooooo.o
oo.o.ooooo.o..oo.o.ooo.oooooo..o.oo.ooo.oooooooooooo.ooooo..
oooooo..ooooooooooooooo.oooooo..oo..ooo..oooooooooooooooo.oo
oooooooooooooooooooo.oooooooooooooo.o.ooooo.oooooooooooooo.o
oooooo.oooooooo.o.oo.ooooooo.oooooooooooooooooo.oooo.oooooo.
ooooo.o.ooooooooooooooooooooooooooooooooooooo.ooo.ooo.oo.ooo
oooo..o.oooo.ooooo.ooooo.oooo..oooooooooooo.oooooooo..oooooo
oooo.oooooooooo.o.ooooooo.oooo.o.oo.oooooooooooo..oooooooooo
oooooo.oo.%oo.ooo.ooo.ooooo.ooooooo.oo.oooooooooo%oooooooooo
oo.oo.ooooooo.oo..oooooooo.oooooooo..oooo.ooo.oo..oooooooooo
o.oooooooooo.oooo.oooooooooo.ooooo.o.oooooooooooooo.oooooooo
o.o.ooooooooooo.o..oooo.ooooooooooooo.ooooooooooooooooo%oooo
oooo..oo%oooooooooooooo.ooooooo.ooooooo.ooo.ooooo.ooooooo.oo
oooooooo.ooooooo.oooooooooo.ooooooo.oo.ooo.ooooooooooo.%oooo
o.oooo.ooooo..oooo.oo.o.oooooooooo.ooo.o.oo.ooo..ooooo.ooooo
"o" => good        "%" => ok        "!" => bad rmsd
"O" => overloaded  "#" => many bad  "." => weak
"@" => abandoned
Mosaic spread: 0.214 < 0.214 < 0.214
-------------------- Integrating SWEEP2 --------------------
Processed batches 2 to 851
Standard Deviation in pixel range: 0.03 1.07
Integration status per image (60/record):
o.ooo.oo..o...o....ooo.oooooooo.ooo%oo..ooooo....oo.o.oo.ooo
oooooo..oooooooooo..ooooo.oo..ooooo.ooooooooooooooo.o.oooooo
oo.ooo.ooo.oooooooo.o.ooooo.o.ooooooooooo..o..o.oooo.ooooooo
oooooooo....oooooo..ooooooooo.oooooo..o.ooooo..oo.oooo.ooo..
oooooooooo.oo%.oooo..o....o.o.ooooooooooooo.o.oooo..oooooooo
ooo.ooo.oo.oooo.oooo.ooo.ooooooo..o.oo.ooooooo.ooooooooooooo
oo.oooooooooooo.ooooo.ooo.oooooo.ooo..oooo.ooooo.ooooooooooo
ooo.oo.o.o.oo.oooooooooooo..ooo.oooooo.oo%.oo.oooooooo.ooooo
.ooooooooooooooooooooo.ooooooo.ooooooo..ooooooo.ooooo.ooooo.
ooo.oooooooo.oo.ooooo.ooooo..oooo.ooooooo.oooooo.o.oooo.o.oo
o.ooooooooooooo.ooo.o.oo.ooooooooooooooooo.oo.ooooooooo.oooo
ooooooo.ooo.oo.o.ooo.ooooo.ooooooo..ooooo.oooooooo%ooooo.ooo
ooooo.ooooooooooooo.oooo..ooooo.ooo.o.o.o%.ooooooo.o.%oooooo
.oo.o.o.oo.ooooo.oooooooo.oo..o.ooooooo.ooooo.ooo.oooo..ooo.
oooooo.ooo
"o" => good        "%" => ok        "!" => bad rmsd
"O" => overloaded  "#" => many bad  "." => weak
"@" => abandoned
Mosaic spread: 0.179 < 0.179 < 0.179
-------------------- Integrating SWEEP3 --------------------
Processed batches 2 to 851
Standard Deviation in pixel range: 0.03 1.18
Integration status per image (60/record):
ooo..o.oo.ooooooooo.oo.ooooo..oooo.ooo...o..ooooo..o.ooooooo
..ooooo.oooo.oooooooooooo..ooo.o..ooooo...ooooo.o.oooo.oo...
oooooo.oooooooooooooo.ooo.oooooooo..ooooo.oo%oo.ooo..oo.oooo
o.o..ooooo.ooo.o.oo.oooooo...ooooo.ooo.o.oooooooo.oo....oo.o
oo.oo.ooooo.o..o.ooooooo..oooooo.ooooooo.o.o.ooo.oo.oo.ooo.o
.oooooo..oooooooooooooooooooo%oooo.o.o.oooooooo..ooo.ooo..o.
oo.o.o.o.oooo..o...oo.ooo.oooooo%ooooo.ooooooo.ooooooooo.oo.
ooooooooooooooooooooooooooooo.ooo.oooooo.oo%oooooooooooooooo
o..ooo.ooo..ooo.oooooooooooooooooo.oo.ooo..oooo.ooooo.ooooo.
oooo..ooooooo.oooooooo.o..oooooo.o.ooooooooo.ooooooo.oooo.oo
oooo.ooooo..oooooooo.oooooooo.oooo.ooo.ooooo.oooooo.oooo.oo%
o.ooooooooooooooooo..ooooo...oooo.oo...ooooooo.oo.oooooo.o.o
.oo.ooooooo.o.o.oo.ooooo..oooooooooo.oo..oo.ooo.ooo.o.o.o..o
o..oooooooo...oooo.o.oooo.o.o.ooo.o.oo.oo..oooo.oo.oo.o...oo
oooooo..o.
"o" => good        "%" => ok        "!" => bad rmsd
"O" => overloaded  "#" => many bad  "." => weak
"@" => abandoned
Mosaic spread: 0.197 < 0.197 < 0.197
-------------------- Integrating SWEEP4 --------------------
Processed batches 2 to 851
Standard Deviation in pixel range: 0.01 1.24
Integration status per image (60/record):
ooooooo.ooo..oo.o.ooooo.ooo.o%oo.oooo..oo%o.o.o.ooooooo..ooo
.oo.o.oooooooooooooo..oooooo.ooooooo.ooo.oo..oooo.ooo.oooo.o
oooo.oo..oo.oooooo.ooooooo.ooooooooooo.ooooo.o.ooo.oooooo.oo
oooooo.ooo.o.oooo.ooo.o.oo.oo.o.ooooooooooo.ooo.ooooo.o.oooo
ooooooooooo.ooo.ooo.oooooo.ooo..ooo.....o.oooooooooo.o.ooooo
o.o.ooo..oo.o...o.ooooooooo..ooooo.o.oooooooooooo%o..o.ooo.o
o..oo....oooooooooooooo.oo.ooooo.oooo.ooooo..oooooooo.ooooo.
.oo..oooo.o.oo.oooooo.oooooo.o.ooooo.ooo...o.ooo..oooooo.ooo
o.oooo..ooo.oo..oo%oo..oooooo%o.o.ooooo.ooo..oooooo.ooooo.oo
o.ooo...oooooo.oo.ooooooo.o.oo..ooo.o.o..ooo..o..o.o.oo.o.oo
o.oooo.oo..oooooo..o...o.oooooo....ooooooo.oooo.oo.oooooo.o.
oo.ooooooooooo.o.o.o.oooo.oo.ooooo..ooooo..o.oooooooooo.ooo.
oooo.ooooo.oooooooo.oooo.oo.ooooo.o..ooooooo.oo..ooooooooooo
o..ooooooo.oo...oo.oooooooooooooooooooo.o..ooo.oo.oooooooooo
ooooooooo.
"o" => good        "%" => ok        "!" => bad rmsd
"O" => overloaded  "#" => many bad  "." => weak
"@" => abandoned
Mosaic spread: 0.284 < 0.284 < 0.284
```

Usually would expect to get mostly `oooo` and `.....` for small molecule data sets - with `%%%` if the spots are less than perfect. What we see above is good. After this the data have the correct symmetry (as in point group) identified and then scaled, after which a "sensible" resolution limit is determined -

```
-------------------- Preparing DEFAULT ---------------------
Reindexing all datasets to common reference
--------------------- Scaling DEFAULT ----------------------
Resolution limit for NATIVE/SWEEP1:  0.81 ( 0.82 suggested)
Resolution limit for NATIVE/SWEEP2:  0.58 ( 0.59 suggested)
Resolution limit for NATIVE/SWEEP3:  0.58 ( 0.66 suggested)
Resolution limit for NATIVE/SWEEP4:  0.58 ( 0.59 suggested)
```

(in this case, using all the data). By default all of the intensity measurements are kept in the output, with the merging stats reporting all data and the lower limit if necessary. After this stage the strong reflections are used to re-refine the unit cell post integration, to get a best estimate of the "global" unit cell for subsequent analysis along with uncertainties to pass on to `shelx`:

```
------------------- Unit cell refinement -------------------
Overall:   4.08  11.21   9.84  90.00 100.67  90.00
```

Finally the overall merging stats are reported for the data set -

```
For AUTOMATIC/DEFAULT/NATIVE                Suggested   Low    High  Overall
High resolution limit                           0.59    1.60    0.59    0.58
Low resolution limit                            9.67    9.67    0.60    9.67
Completeness                                   95.6   100.0    38.9    93.9
Multiplicity                                    4.4     7.7     1.1     4.4
I/sigma                                         9.0    44.1     0.0     8.9
Rmerge(I)                                     0.049   0.041   0.558   0.049
Rmeas(I)                                      0.053   0.044   0.789   0.053
Rpim(I)                                       0.020   0.016   0.558   0.020
CC half                                       0.999   0.999   0.666   0.999
Total observations                             9769     994      48    9777
Total unique                                   2235     129      44    2243
Assuming spacegroup: P 1 2/m 1
Unit cell (with estimated std devs):
 4.0770(2)  11.2084(7)  9.8377(5)
90.0       100.670(4)  90.0   
```

It is important to note here that the space group assignment is based on the systematic absences and therefore somewhat unreliable, but the point group determination (which is really all we care about at this stage) is robust.

The details of how this works can be followed through by going through the [_much more interesting_ `dials` tutorial](../dials/README.md).

## Controlling xia2

The intention of `xia2` is that the defaults "just work" but sometimes you will know better and wish to enforce your will over the computer. This is very straightforward e.g. assigning the known unit cell, space group and resolution limit (which are the key choices) as:

```bash
xia2 space_group=P2 unit_cell=4.1,11.2,9.8,90,100.7,90 d_min=0.84 /dls/i19-2/data/2023/cy12345-6/foo/
```

You can also process specific "runs" with e.g.

```bash
xia2 image=/dls/i19-2/data/2023/cy12345-6/foo/foo_2_0001.cbf image=/dls/i19-2/data/2023/cy12345-6/foo/foo_2_0001.cbf
```

which will only take the runs which belong to those images. You can also process a subset of the images in a run with

```
xia2 image=/dls/i19-2/data/2023/cy12345-6/foo/foo_2_0001.cbf:1:900
```

which will only process images 1...900 inclusive. This can be useful if you did a long scan and the sample decayed.
