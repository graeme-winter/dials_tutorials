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

