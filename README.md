# PipMag

Development of pipeline for magnetic field reconstruction based on spectro-polarimetric observations of the solar atmosphere.

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

## Setting up conda environment

    mamba create --name pipmag 
    mamba activate pipmag
    mamba install --file requirements.txt

## Creating the SST observations database

- Open the file `quicklook.ipynb`
- Go to the section marked `Start here: Loading the existing dataframe`
- Load the latest pickle file and run the block containing the widget.
- Enter a `Year, Month, Day, Time` combination and click on Show to see the quicklook movie options.
- Note the `Index` value and enter the number in the widget below.
- Any predefined info will be loaded in the boxes which can now be updated.
