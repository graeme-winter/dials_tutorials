# Data processing tutorial

## Summary

We will start by looking at a data set recorded from crystals of the enzyme tetrahydroalstonine synthase (THAS1). The images were collected at Diamond Light Source on a PILATUS 6M pixel array detector at an X-ray wavelength of 1.282 Å, at the Zinc _K_ edge. There is sufficient anomalous signal to solve the structure by experimental phasing (SAD). The data set is located on your PC in the directory `C:\CourseFiles\ccp4\ADH4_data` and there are some more details provided in the file `ADH4_data_info.pdf`.

First we will set up a xia2 processing job, running remotely on the CCP4 Cloud at Harwell. This will keep the local PCs free to simultaneously try out DIALS data processing using the command line. Use of the command line is not always so natural on Windows compared to Linux, or even Mac. Nevertheless, hopefully the tutorial will demonstrate that command line processing with DIALS can be reasonably straightforward, and offers a lot of power and choice to the user.

Once you have completed the "manual" processing, you can compare results with the xia2 job. Are there any differences? Which job has better statistics?

Optionally, if you have time at the end, you may look at xia2 processing results for a thermolysin data set, recorded on an EIGER X 16M detector at 1.2824 Å - again at the Zn edge. However, the autoprocessing did not quite go to plan this time. Can you work out what is wrong?

## Processing with xia2 on CCP4 Cloud

On the Windows desktop you should see a folder named something like "CCP4-9 Shortcuts". Open this and then double click on the icon named "CCP4Cloud Remote". This will open a web browser allowing you to log in to the CCP4 Cloud at Harwell. Here we assume you already have an account, and know how to create a new project.

Within your Cloud project, add a new "Automatic Image Processing with Xia-2" task. Under "Input Data" make sure sure the task will "Look for X-ray images in cloud storage". :file_folder: Browse for the image directory, selecting _Tutorials/Data/1_from_images/ADH4/ADH4_diffraction_data_. Set a sensible project and crystal name, and don't forget to add "Zn" as the heavy atom type!

There's no need to set any advanced options, just select "Run". Make sure the job starts, but after that you can leave it to process while you look at the images locally with DIALS.

> [!WARNING]
> You are more likely to encounter xia2 from Diamond autoprocessing, or by running xia2 locally through ccp4i2 or at the command line. Processing using CCP4 Cloud requires you first to upload the images to Cloud. Recently this was made easier if you (or your lab) using the Globus file transfer platform, where CCP4 Cloud has an endpoint. However, image data is large and will eventually be deleted from Cloud to save space. So don't consider CCP4 Cloud as a backup solution for your diffraction data!

## Starting the CCP4 console

On the Windows desktop you should see a folder named something like "CCP4-9 Shortcuts". Open this and then double click on the icon named "CCP4Console". This will bring up a Windows Terminal with the CCP4 environment correctly set up. The first thing you should do is change to a suitable directory in which to perform data processing, for example by entering the following commands:

```console
cd %homepath%
mkdir ADH4-dials
cd ADH4-dials
```

## Importing the images

The first task in data processing with DIALS is to import the images. The program used to do this is unimaginatively named `dials.import`. In common with other `dials.something` commands, running the program without options will print a help message with some usage examples:

```console
dials.import
```

You may have to scroll up to read the full output. If you add the option `-h` to this command you will not only see the help message, but also the structured definitions of the command line parameters that can be passed to the program.

> [!NOTE]
> What happens if you pass multiple `h` and `v` characters? Try this out later with other DIALS programs too.

Now we are ready to import the images. You can do this by entering the following command (adjust if the path to the files differs on your computer):

```console
dials.import C:\CourseFiles\ccp4\ADH4_data\ADH4_diffraction_data\ADH4_M7S9_6_*.cbf
```

Note the use of the wildcard `*` character in this command. This is not DIALS syntax, but is expanded by the Windows shell to match every image file in that directory, from `ADH4_M7S9_6_0001.cbf` to `ADH4_M7S9_6_0800.cbf`. What `dials.import` does is read the header of each of these files, checks the diffraction geometry, and determines the relationship between the files. All going well you will see output containing

```
--------------------------------------------------------------------------------
  format: <class 'dxtbx.format.FormatCBFMiniPilatusDLS6MSN100.FormatCBFMiniPilatusDLS6MSN100'>
  template: C:\Users\fcx32934\data\ADH4_data_for_summer_school\ADH4_diffraction_data\ADH4_M7S9_6_####.cbf:1:800
  num images: 800
  sequences:
    still:    0
    sweep:    1
  num stills: 0
--------------------------------------------------------------------------------
Writing experiments to imported.expt
```

This tells you that DIALS interprets the 800 images as a single rotation sweep, and writes the diffraction geometry and associated metadata into a new file, `imported.expt`. To get human-readable information from that file try

```console
dials.show imported.expt
```

## Viewing the images

Although we are doing command-line data processing, we should still look at the images! DIALS contains a feature-rich image viewer for this purpose:

```console
dials.image_viewer imported.expt
```

> [!NOTE]
> Take a moment to explore the controls in the image viewer. Can you drag the image around and zoom using the mouse? Can you see the intensity and resolution information for a single pixel? What is your preferred colour scheme and brightness? Can you scroll through and see how the diffraction images change as data collection proceeds? Don't be afraid to play with the controls - nothing you can do here will affect processing of the data set.

There is a horizontal backstop shadow across the images. We could mask this out if we wanted, however looking at the rotation axis orientation using `dials.image_viewer`, we see that this is aligned with the backstop shadow. Spots close to the rotation axis are less reliable and will not be integrated anyway (can you figure out why?). So we will not bother to mask the shadow here.

## Finding spots

With the image viewer open, select the "Threshold pixels" checkbox. This shows you which pixels the spot-finding algorithm considers to be "strong".

> [!NOTE]
> Do the strong pixels match the diffraction spots? What happens if you modify parameters of the threshold algorithm (like kernel size and gain)? What happens if you select different threshold algorithms?

The default parameters seem pretty good for this data set, so exit the image viewer and run a default spot-finding job:

```console
dials.find_spots imported.expt
```

DIALS finds spots throughout the entire rotation scan, whereas some other programs default to finding spots on just enough images to perform indexing. This means spot-finding takes longer with DIALS, but the information determined from the entire scan can be reused multiple times. In fact, now DIALS will not need to read the image data again until integration. At the end of the spot-finding procedure you will see an ASCII-art histogram indicating the number of spots found on each image. In this case it is pretty boring because the crystal diffracts equally well throughout the scan:

```
Histogram of per-image spot count for imageset 0:
307302 spots found on 800 images (max 5525 / bin)
*                                * **** ** * * **  ** *    *
************************************************************
************************************************************
************************************************************
************************************************************
************************************************************
************************************************************
************************************************************
************************************************************
************************************************************
1                         image                          800

--------------------------------------------------------------------------------
Saved 307302 reflections to strong.refl
```

## Viewing the reciprocal lattice

Now we can pass both the metadata `imported.expt`, and spot file `strong.refl` to `dials.reciprocal_lattice_viewer`:

```console
dials.reciprocal_lattice_viewer imported.expt strong.refl
```

> [!TIP]
> The Windows terminal appears not to allow tab-completion on DIALS command names. Why?! To avoid having to type out the whole of `dials.reciprocal_lattice_viewer` you can use its alias `dials.rlv` instead.

Take some time to explore the controls in the `dials.reciprocal_lattice_viewer`

> [!NOTE]
> What does middle-button drag do? Try setting "Max Z" to something small, like 5. What does this show you? Align the view down the rotation axis and then click to increase the Max Z value (Use Alt-click to jump in blocks of 100). Can you see how data collection sweeps out a volume of reciprocal space? Can you align the view in a direction that clearly shows the crystal lattice?

The main purpose of the `dials.reciprocal_lattice_viewer` prior to indexing is to look for pathologies that might cause indexing to fail, such as poor diffraction geometry, noisy spots, split spots, ice rings, and so on. In this case the reciprocal space lattice looks very clean, so we would not expect indexing to have any problems.

## Indexing
