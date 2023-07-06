# PipMag

Development of pipeline for magnetic field reconstruction based on spectro-polarimetric observations of the solar atmosphere.

## Online version

Run the following [notebook](https://github.com/AvijeetPrasad/PipMag/blob/main/notebooks/quicklook.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github.com/AvijeetPrasad/PipMag/blob/main/notebooks/quicklook.ipynb)



## Setting up conda environment

    mamba create --name pipmag
    mamba activate pipmag
    mamba install --file requirements.txt

## Installation

For development purposes, you may want to install the package in an editable mode. This will link the installed package directly to your source code so that any changes you make to the source code will be immediately reflected in the installed package.

To install `pipmag` in editable mode:

1. Navigate to the directory containing `setup.py`:

    ```bash
    cd /path/to/pipmag
    ```

2. Activate your conda environment:

    ```bash
    mamba activate pipmag
    ```

3. Install the package in editable mode:

    ```bash
    pip install -e .
    ```

## Creating the SST observations database

- Open the file `quicklook.ipynb`
- Go to the section marked `Start here: Loading the existing dataframe`
- Load the latest pickle file and run the block containing the widget.
- Enter a `Year, Month, Day, Time` combination and click on Show to see the quicklook movie options.
- Any predefined info will be loaded in the boxes which can now be updated.

## Setting up the `config.ini` file

- Open the file `config.ini.example` file and save it as `config.ini`
- Add the `ADS_DEV_KEY` to the `config.ini` file. To obtain the `ADS_DEV_KEY` follow the instructions [here](https://ui.adsabs.harvard.edu/help/api/)

## Commit messages

Use following tags for commit messages:

       [DEV] : Code development (including additions and deletions)
       [ADD] : Adding new feature
       [DEL] : Removing files, routines
       [FIX] : Fixes that occur during development, but which have essentially no impact on previous work
       [BUG] : Bug with significant impact on previous work -- `grep`-ing should give restricted list
       [OPT] : Optimisation
       [DBG] : Debugging
       [ORG] : Organisational, no changes to functionality
       [SYN] : Typos and misspellings (including simple syntax error fixes)
       [DOC] : Documentation only
       [REP] : Repository related changes (e.g., changes in the ignore list, remove files)
       [UTL] : Changes in utils
