# PipMag

Development of pipeline for magnetic field reconstruction based on spectro-polarimetric observations of the solar atmosphere.

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

Sure, here's a draft section for your README to instruct users on how to use Git Large File Storage (LFS) to track changes in CSV files:

## Using Git Large File Storage (LFS) for CSV files

If you're contributing large CSV files to this project, we recommend using Git Large File Storage (LFS), an open-source Git extension for versioning large files. Git LFS replaces large files such as CSV files with text pointers inside Git, while storing the file contents on a remote server. This results in reduced repository size and faster clone and fetch operations.

Follow the steps below to install Git LFS and start tracking CSV files:

1. **Install Git LFS:** If you haven't installed Git LFS yet, you can do so using Homebrew if you're on a macOS:

    ```bash
    brew install git-lfs
    ```

   For other operating systems, please follow the [official Git LFS installation instructions](https://git-lfs.github.com/).

2. **Set up Git LFS:** After installing Git LFS, you need to set it up once per repository on your machine. Navigate to the root directory of your local clone of the Git repository and run:

    ```bash
    git lfs install
    ```

3. **Track CSV files:** To start tracking CSV files with Git LFS, run:

    ```bash
    git lfs track "*.csv"
    ```

   This command tells Git LFS to track all CSV files. You can adjust the "*.csv" pattern to match the specific files you want to track.

4. **Commit and push changes:** Now, you can commit and push your changes as usual:

    ```bash
    git add .
    git commit -m "Add large file"
    git push
    ```

   Git LFS is now set up and will automatically intercept the CSV files you specified and store them efficiently.

Please note that each user who wants to interact with the large files will need to have Git LFS installed on their machine. Otherwise, they'll only see the text pointers in their local repository.

For more information about Git LFS, please refer to the [official Git LFS documentation](https://github.com/git-lfs/git-lfs/wiki).
---

Remember to replace the repository path and file types according to your project's specifics.

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
