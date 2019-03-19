# R-cubed riser data

This repository contains experiment data from the R-cubed riser in the NREL TCPDU system. Code for analyzing the data is also provided. The data is for model development and validation of a riser unit for upgrading biomass pyrolysis vapors.

#### original-hydro

CSV files of the original hydrodynamics experiment data are in the `original-hydro` directory. The CSV data was exported from the `R3 CCPC Hydrodynamics Data Summary 20190225` Excel spreadsheet provided by NREL. Before exporting from the spreadsheet, the columns had to be formatted as "Number" with 6 decimal places.

#### processed-hydro

The `processed-hydro` folder contains CSV files created from the original data located in the `original-hydro` directory. The processed files are named according to the experiment number, date, and sheet; these files are used for model development and validation. The processed files were created by the `process_hydro.py` script.

#### results-hydro

Statistics about the processed data are written to `results-hydro` after running the various Python programs (e.g. `dp_cat.py`) in the root directory.

#### spreadsheets

The `hydro-data` spreadsheet contains all the hydrodynamics experiment data provided by NREL. This file's original name was `R3 CCPC Hydrodynamics Data Summary 20190225`. The `hydro-exp-matrix` spreadsheet is an overview of the hydrodynamics experiments conducted in the riser.

## Usage

Terminal commands for running each program are given below. See the comments in each Python file for more information.

```bash
# plot pressures and save stats to csv file
# 1st argument low, mid, or high
# 2nd argument pdit700, pdit704, pdit705, pdit706, or pdit707
$ python dp_cat.py low pdit700

# plot different pressure for max catalyst flow
$ python dp_cat_max.py

# compare diff. pressure for different process gas flows
$ python dp_gas.py

# plot atmospheric pressure
$ python p_atm.py

# process the original experimental data and save to file
$ python process_hydro.py

# plot temperatures from thermocouples
# 1st argument low, mid, or high
# 2nd argument te709c, te709b, te709a, te707c, te707b, te707a, te705, or te701
$ python temp_cat.py mid te709c
$ python temp_cat.py high te705
```

## License

Code and data in this repository is available under the MIT License - see the [LICENSE](LICENSE) file for more information.
