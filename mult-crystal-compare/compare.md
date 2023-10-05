# Multi-crystal Comparison with DIALS

While there are tutorials on combining multiple data sets with DIALS and multiplex, I have not got one yet which can be used for _comparing_ data sets i.e. if you record a load of data sets from a sample which has (say) indexing ambiguity and you don't want to mess around too much. In this case you may also want to scale the data to make them as similar as possible, but merge them separately. Happily, this is easy.

## Script

Essentially the same as the usual `tl;dr` script - process data by importing, indexing etc. except here we are importing a number of data sets and indexing them separately, before being back to a common orientation for scaling.

```
dials.import \
/dls/i04/data/2023/cm33903-4/gw/20230922/ins6/ins6_1.nxs \
/dls/i04/data/2023/cm33903-4/gw/20230922/ins7/ins7_1.nxs \
/dls/i04/data/2023/cm33903-4/gw/20230922/ins8/ins8_1.nxs
dials.find_spots imported.expt
dials.index imported.expt strong.refl joint=false
dials.refine indexed.expt indexed.refl
dials.integrate refined.expt refined.refl
dials.cosym integrated.expt integrated.refl
dials.scale symmetrized.expt symmetrized.refl \
  anomalous=true absorption_level=medium
dials.split_experiments scaled.expt scaled.refl
for n in 0 1 2; do
  dials.merge split_${n}.expt split_${n}.refl output.mtz=split_${n}.mtz
done
```

(you do not need to process the data together, this is just for convenience) - the key point is bringing the data from integration (here; in P1, but that is not mandatory) together and resolving the symmetry across the population and any indexing ambiguity. After this, the data are suitable for scaling together (which works fine with the defaults). After this the data are then separated out into the original data sets and merged to give MTZ files which are then suitable for `dimple` analysis - after this the maps can be loaded into `coot` for direct comparison.
