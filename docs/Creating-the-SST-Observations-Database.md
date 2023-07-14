# Creating the SST Observations Database

This page will guide you on how to create the SST observations database using the PipMag package. This database forms the backbone of your data analysis and is essential for the effective use of the PipMag functionalities.

Follow the steps below to create your SST observations database:

1. **Import the necessary module:** You will need to import the `gen_la_palma_df.py` module from the `pipmag` package. This module contains the functions necessary for creating the database.

2. **Run the module:** Execute the `gen_la_palma_df.py` module to generate the SST observations database. The module will parse through the SST data and structure it into a data frame.

3. **Save the data frame:** The resulting data frame will be saved as a CSV file in the `data` directory of the project repository. This CSV file forms the SST observations database.

Now that you have created the SST observations database, you can view the quicklook movies of the observations:

1. **Open the Jupyter notebook:** Navigate to the `notebooks` directory in the project repository and open the `la_palma_quicklook.ipynb` notebook.

2. **Load the database:** In the notebook, load the `la_palma_obs_data.csv` file from the `data` directory. 

3. **Run the IPython widget:** Run the block in the notebook containing the IPython widget. 

4. **Input the date and time:** Provide a `Year, Month, Day, Time` combination and click on "Show" to see the quicklook movie options. Any predefined information will be loaded into the boxes and can be updated as needed.

With these steps, you've successfully created the SST observations database and are ready to explore the quicklook movies of the observations!

In the next section, we will guide you on how to [Set Up the Configuration File](./Setting-up-configuration-file).

If you encounter any issues during the database creation process, feel free to raise an issue on the project's GitHub page. We are here to help!