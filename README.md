# Using MIT's Darwin Model as a testbed for statistical learning models

This package contains a series of analytical tools to extract and data from output from MIT's Darwin marine ecosystem 
model, embedded in MITgcm. It trains statistical learning models (GAMs) on a subset of historical Darwin ocean data, 
sampled to mimic real-world observational data, and also on randomly-sampled datasets of various sizes. It quantifies 
the effect of spatial bias and of training set sample size on the resulting predictions.
Altogether, the program allows us to assess GAMs model skill in predicting the virtual ocean's plankton biogeography, 
both in present-day spatial extrapolations, and by the end of the 21st century, as a response to climate change.

### STEP 1

- Extracts and cleans surface data (Z=0) from Darwin output files (1987-2008, 2079-2100)
- Builds a binary sampling matrix (BSM) using a publicly-available ocean measurements dataset
- Uses the BSM to sample Darwin model at real-life ocean-measurement locations
- Builds an identically-sized BSM to sample the Darwin model at random locations
- Plots a 3D matrix (Lat, Lon, Month) to visualise spatiotemporal distributions (pdf)
- Plots histogram of measurements per month (pdf)
- Builds a further 54 randomly-sampled training sets spanning 18 size classes (N=63 to N=11,557)

### STEP 2

- The samples are used as training datasets for Generalised Additive Models (GAMs)
- Plankton species are combined into functional groups (pro, pico cocco, diaz, diatom, dino, zoo)
- Biomass is selected as target variable for GAMs
- Physical variables (SST, SSS, PAR) and nutrients (NO3, PO4, Fe, Si) set as predictors
- GAMs are trained, and partial dependency plots are outputted (pdf)
- GAMs are used to predict plankton biogeography across whole-ocean in 1987-2008, and 2079-2100

### STEP 3

- Global biomass maps are plotted for qualitative comparison between target and GAMs predictions
- Relative difference (%) maps between Darwin 'truth' and GAMs predictions are plotted for 1987-2008 and 2079-2100
- Target and predictions are quantitatively compared with a series of descriptive statistics
- The above analyses are repeated for each plankton functional group
- Correlations using the Distance Correlation method, Pearson's, and Spearman's are calculated
- Correlation heatmaps are produced


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for dev. or testing.

### Prerequisites

First, please ensure that you have a copy of the conda package manager installed locally (miniconda is recommended).

Fork and clone the project repository onto your local machine.


### Create Environment

From the root of the cloned project, run:

```
make create_environment
```

This will create a virtual environment for the project, to install project dependencies, and minimise the possibility
of conflicts with other elements of your system. You will be prompted to activate - go ahead and do so :)

Next, inform your python interpreter of the structure of the project, so it understands which internal components should
be treated as callable modules:

```
make setup
```

Finally, install the project dependencies:

```
make requirements
```

## Authors

- **Lee Bardon** - _Initial work_ - [teatauri](https://github.com/teatauri)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
