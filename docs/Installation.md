# Installation

This page provides detailed instructions for installing PipMag. The installation process involves setting up a new environment, handling dependencies, and installing the package itself.

## Preparing the Environment

PipMag relies on a set of dependencies that are listed in the `requirements.txt` file. To ensure a clean and conflict-free setup, we recommend creating a new environment using conda or mamba.

If you're using macOS or Linux, you can create and activate the environment as follows:

```bash
mamba create --name pipmag
mamba activate pipmag
mamba install --file requirements.txt
```

## Installing PipMag

Once the environment is prepared, navigate to the directory containing the `setup.py` file, activate your environment, and install the package in an editable mode. This mode links the installed package directly to your source code, so any changes you make in the source code will be immediately reflected in the installed package.

```bash
cd /path/to/pipmag
mamba activate pipmag
pip install -e .
```

You've now successfully installed PipMag! The package is ready for you to use or contribute to.

In the next section, we will guide you on [Creating the SST Observations Database](./Creating-the-SST-Observations-Database).

If you encounter any issues during the installation process, feel free to raise an issue on the project's GitHub page. We are here to help!