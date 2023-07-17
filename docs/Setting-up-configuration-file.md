# Configuring PipMag

This page provides detailed instructions on how to configure PipMag by setting up the `config.ini` file. This file is important for the proper functioning of certain features in PipMag, such as the Astrophysics Data System (ADS) search feature.

## Preparing the `config.ini` File

The repository includes an example configuration file named `config.ini.example`. To set up your own configuration:

1. Open the `config.ini.example` file.
2. Save it as `config.ini`.

This `config.ini` file will be your personal configuration file for PipMag.

## Configuring ADS Search

To run ADS searches within the notebooks, you'll need to add your `ADS_DEV_KEY` to the `config.ini` file. Follow the steps below to do this:

1. Obtain your `ADS_DEV_KEY` by following the instructions provided [here](https://ui.adsabs.harvard.edu/help/api/).
2. Open your `config.ini` file.
3. Add your `ADS_DEV_KEY` to the `config.ini` file and save the changes.

With these steps, you have successfully set up the `config.ini` file and configured PipMag for ADS searches.

## Note

Remember to keep your `config.ini` file safe and not to share it publicly, as it contains your personal `ADS_DEV_KEY`. Treat it like a password.

In the next section, we will guide you on how to use Git Large File Storage (LFS) for handling large CSV files in the [Using Git Large File Storage (LFS) for CSV Files](./Working-with-Git-Large-File-Storage.md).

If you encounter any issues during the configuration process, feel free to raise an issue on the project's GitHub page. We are here to help!