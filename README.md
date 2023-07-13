# PipMag

PipMag is a Python package designed for browsing and querying solar observations data gathered by the Swedish Solar Telescope (SST). 

## Installation

### Preparing the Environment

The package relies on a set of dependencies listed in the `requirements.txt` file. To ensure a clean and conflict-free setup, it's recommended to create a new environment using either conda or mamba.

For macOS and Linux users, you can create and activate the environment as follows:

```bash
mamba create --name pipmag
mamba activate pipmag
mamba install --file requirements.txt
```

### Installing PipMag

Once the environment is ready, navigate to the directory containing `setup.py` file, activate your environment, and install the package in an editable mode. This mode links the installed package directly to your source code, allowing any changes you make in the source code to be immediately reflected in the installed package.

```bash
cd /path/to/pipmag
mamba activate pipmag
pip install -e .
```

## Creating the SST Observations Database

The package includes a python file (`pipmag/gen_la_palma_df.py`) that creats the SST observations database.

To view the quicklook movies:
- Open `notebooks/la_palma_quicklook.ipynb`
- Load the `data/la_palma_obs_data.csv` file and run the block containing the IPython widget.
- Provide a `Year, Month, Day, Time` combination and click on "Show" to see the quicklook movie options.
- Any predefined information will be loaded into the boxes and can be updated as needed.

## Setting up the `config.ini` File

To setup the configuration:

- Open the `config.ini.example` file and save it as `config.ini`
- To run ADS searches within the notebooks, add your `ADS_DEV_KEY` to the `config.ini` file. To obtain this key, follow the instructions provided [here](https://ui.adsabs.harvard.edu/help/api/).

## Using Git Large

File Storage (LFS) for CSV Files

If you're planning to contribute large CSV files to this project, we recommend using Git Large File Storage (LFS), an open-source Git extension for versioning large files. Git LFS replaces large files such as CSVs with text pointers inside Git, while storing the file contents on a remote server. This results in a smaller repository size and faster operations.

### Installing and Setting Up Git LFS

For macOS users, you can install Git LFS using Homebrew:

```bash
brew install git-lfs
```

For Linux users, refer to the [official Git LFS installation instructions](https://git-lfs.github.com/).

After the installation, setup Git LFS for your repository:

```bash
git lfs install
```

### Tracking CSV Files

To start tracking CSV files with Git LFS:

```bash
git lfs track "*.csv"
```

This command tells Git LFS to track all CSV files. Adjust the "*.csv" pattern to match the specific files you want to track.

### Committing and Pushing Changes

You can now commit and push your changes as usual:

```bash
git add .
git commit -m "Add large file"
git push
```

Remember, users who interact with the large files will need Git LFS installed on their machines. Otherwise, they'll only see the text pointers in their local repository.

## Commit Message Guidelines

Use the following tags for commit messages:

- `[DEV]`: Code development (including additions and deletions)
- `[ADD]`: Adding new features
- `[DEL]`: Removing files, routines
- `[FIX]`: Fixes that occur during development, but which have essentially no impact on previous work
- `[BUG]`: Bug with significant impact on previous work
- `[OPT]`: Optimization
- `[DBG]`: Debugging
- `[ORG]`: Organizational changes, no changes to functionality
- `[SYN]`: Typos and misspellings (including simple syntax error fixes)
- `[DOC]`: Documentation only
- `[REP]`: Repository related changes (e.g., changes in the ignore list, remove files)
- `[UTL]`: Changes in utilities

## Repository Structure

The repository structure is organized as follows:

- `LICENSE`: Contains the license details for this project.
- `README.md`: This file, containing details about the project and instructions for setting it up.
- `config.ini.example`: An example configuration file to guide users in setting up their own `config.ini`.
- `data`: This directory contains the dataset files.
- `docs`: Contains the documentation files for the project.
- `notebooks`: Contains Jupyter notebooks for analyzing and visualizing the data.
- `pipmag`: The main package directory, containing all the Python scripts and modules for the project.
- `requirements.txt`: Lists all Python dependencies required by PipMag.
- `scripts`: Contains utility scripts for the project.
- `setup.py`: Python script for packaging and distributing the project.
- `tests`: Contains the test scripts for the PipMag package.
