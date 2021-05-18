

How to use?

1. write_thickness.py calculates how thick the range shifter material is for a given setup. This is done by first fitting cubic splines to simulated data, where LET vs range shifter thickness has been plotted, and then use these splines as a lookup table for the desired LET we want to calculate.

2. This data is then added to the config.cfg-file under src

3. Now, we can create our shieldhit-directories using mcscripter config.cfg, which will use the files from src/template, and modify them accorging to the config.cfg-file

```
cd 2015_Guan/sim-files
mscripter config_H.cfg
mscripter config_He.cfg
mscripter config_C.cfg
```

4. Perform the MC-simulations in all the created subfolders

```
./prepare.sh
find workspace_2021_05_18_15_49_12/ -name beam.dat -execdir sbatch run.sh \; # or similar
```

5. Now we can use collect_data_mult.py under src/, to collect all generated data from the output of the MC-sims. 

(The final fit of the data is done elsewhere)
