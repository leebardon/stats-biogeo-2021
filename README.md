# Analysing Data from MIT's Darwin Model

**NOTE**: _This package is a work in progress (as of 22nd Mar 2021). This message will be removed when v.1.0 development is complete._

This package contains a series of analytical tools to extract and data from output from MIT's Darwin marine ecosystem model, powered by the MITgcm. It applies machine-leaning (ML) models to a subset of historical Darwin ocean data, and assesses how well the ML models can predict the simulated ocean's plankton biogeography in future, as a response to climate change.

### STEP 1
---

> - Extracts and cleans surface data (Z=0) from Darwin output files (1987-2008, 2079-2100)
> - Builds a binary sampling matrix (BSM) using a publically-available ocean measurement dataset
> - Uses the BSM to sample Darwin model at real-life ocean-measurement locations
> - Builds an identically-sized BSM to sample the Darwin model at random locations
> - Plots a 3D matrix (Lat, Lon, Month) to visualise spatiotemporal distributions (pdf)
> - Plots histogram of measurements per month (pdf)

### STEP 2
---

> - The samples are used as training datasets for Generalised Additive Models (GAMs)
> - Plankton species are combined into functional groups (pro, pico cocco, diaz, diatom, dino, zoo)
> - Biomass is selected as target variable for GAMs
> - Physical variables (SST, SSS, PAR) and nutrients (NO3, PO4, Fe, Si) set as predictors
> - GAMs are trained, and partial dependency plots are outputted (pdf)
> - GAMs are used to predict plankton biogeography across whole-ocean in 1987-2008, and 2079-2100

### STEP 3
---

> - Global time-averaged biomass maps generated for each functional group, 1987-2008, 2079-2100
> - Target and predictions are quantitatively compared with descriptive statistics
> - Hexplots of target vs predictions for each functional group are generated
> - Target-predictor correlations are evaluated using a range of techniques, and plotted as heatmaps
> - Strength of correlations are evaluated over time, to examine possible relationship changes
> - Partial dependance plots are generated from GAMs models fitted on 1987-2008, and 2079-2100 data

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

First ensure that you are running a copy of python3 on your local machine, with pip package manager. Install dependency management package:

```
pip install pipenv
```

### Project Setup

Clone the project down locally and install in editable state from the root folder (containing setup.py file) and run:

```
pip install -e .
```

Change directory into the main project folder (ML_Biogeography_2021) and install dependencies:

```
pipenv install
```

Activate the environment:

```
pipenv shell
```

## Running the tests

TBC

## Built With

- [Pipenv](https://pypi.org/project/pipenv/) - Dependency Management
- [PyGam](https://pygam.readthedocs.io/en/latest/) - building Generalized Additive Models in Python

<!-- ## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us. -->

## Authors

- **Lee Bardon** - _Initial work_ - [teatauri](https://github.com/teatauri)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
