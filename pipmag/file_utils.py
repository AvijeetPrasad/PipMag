import pickle
from datetime import datetime
import glob
import os

def add_timestamp(file_name):
    """
    Add timestamp to a file name.

    Parameters
    ----------
    file_name : str
        The name of the file to which the timestamp should be added.

    Returns
    -------
    str
        The new file name with the added timestamp.

    Dependencies
    ------------
    - datetime: Required to retrieve the current date and time.
    - os: Required to get the extension of the file name.

    Notes
    -----
    Function Name: add_timestamp
    This function takes a file name as input and appends a timestamp to it before the file extension.
    The timestamp is in the format YYYYMMDD_HHMMSS and is obtained from the current date and time.
    The function replaces the original file extension with the timestamp and the extension.

    Examples
    --------
    >>> add_timestamp("example.txt")
    "example_20210706_121510.txt"

    >>> add_timestamp("document.docx")
    "document_20210706_121510.docx"
    """
    # get the current date and time
    now = datetime.now()
    # get the current date and time in the format YYYYMMDD_HHMMSS
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    # get the extension of the file name
    extension = os.path.splitext(file_name)[1]
    # add the timestamp to the file name
    new_file_name = file_name.replace(extension, '_' + timestamp + extension)
    return new_file_name

def get_latest_file(file_pattern):
    """
    Get the latest file from a given file pattern.

    Parameters
    ----------
    file_pattern : str
        The pattern to match the files (e.g., "path/to/files/*.txt").

    Returns
    -------
    str or None
        The file name with the latest timestamp, including the file path.
        If no files are found, None is returned.

    Dependencies
    ------------
    - glob: Required for pattern matching and retrieving file names.
    - os: Required for manipulating file paths and names.
    - datetime: Required for converting timestamps to datetime objects.

    Notes
    -----
    Function Name: get_latest_file
    This function takes a file pattern as input and returns the file name with the latest timestamp.
    It searches for files matching the specified pattern using glob.
    If no files are found, the function returns None.
    The function extracts the timestamp from the file names, compares them,
    and returns the file with the latest timestamp.
    The file path is included in the returned file name.

    Examples
    --------
    >>> get_latest_file("path/to/files/*.txt")
    "path/to/files/example_20210706_121510.txt"

    >>> get_latest_file("path/to/files/*.csv")
    "path/to/files/data_20210706_121510.csv"

    >>> get_latest_file("path/to/files/*.pdf")
    None
    """
    # define a function that extracts the timestamp from a list of file names
    # and returns the file name with the latest timestamp
    file_list = glob.glob(file_pattern)
    # if the file list is empty, return None
    if not file_list:
        print('No files found')
        return None
    # remove the file path from the file names
    file_list = [os.path.basename(file_name) for file_name in file_list]
    # get the timestamp from the file name and join the date and time
    timestamp_list = [file_name.split('_')[-2:] for file_name in file_list]
    # combine the date and time
    timestamp_list = ['_'.join(timestamp) for timestamp in timestamp_list]
    # remove the extension from the timestamp
    timestamp_list = [timestamp.split('.')[0] for timestamp in timestamp_list]
    # convert the timestamp to a datetime object
    timestamp_dt_list = [datetime.strptime(
        timestamp, "%Y%m%d_%H%M%S") for timestamp in timestamp_list]
    # get the index of the latest timestamp
    latest_index = timestamp_dt_list.index(max(timestamp_dt_list))
    # get the file name with the latest timestamp
    latest_file = file_list[latest_index]
    # add the file path to the file name
    latest_file = os.path.join(os.path.dirname(file_pattern), latest_file)
    if len(latest_file) > 0:
        print(f'Latest file: {latest_file}')
    else:
        print('No files found')
    return latest_file

def save_pickle(data, filename):
    """
    Save data as a pickle file.

    Parameters
    ----------
    data : object
        The data to be saved as a pickle file.
    filename : str
        The name of the file to which the data will be saved.

    Returns
    -------
    None

    Dependencies
    ------------
    - pickle: Required for pickling and saving data.

    Notes
    -----
    Function Name: save_pickle
    This function takes data and filename as input and saves the data as a pickle file.
    It opens the file in binary write mode and uses pickle.dump() to write the data into the file.
    Pickling is a way to convert Python objects into a serialized format that can be saved to a file
    and later retrieved.
    The saved file will have the same format and content as the original data.

    Examples
    --------
    >>> save_pickle(my_data, "data.pickle")
    (No output; data is saved as "data.pickle" file.)
    """
    # define a function that takes data and filename as input and saves the data as a pickle file
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def load_pickle(filename):
    """
    Load data from a pickle file.

    Parameters
    ----------
    filename : str
        The name of the pickle file from which the data will be loaded.

    Returns
    -------
    object
        The loaded data from the pickle file.

    Dependencies
    ------------
    - pickle: Required for unpickling and loading data.

    Notes
    -----
    Function Name: load_pickle
    This function takes a filename as input and loads the data from the specified pickle file.
    It opens the file in binary read mode and uses pickle.load() to read the data from the file.
    Unpickling is the process of deserializing the data stored in a pickle file back into Python objects.
    The function returns the loaded data.
    A success message is printed to indicate that the file was loaded successfully.

    Examples
    --------
    >>> loaded_data = load_pickle("data.pickle")
    loaded data.pickle successfully
    (The loaded data is returned and assigned to the variable "loaded_data".)
    """
    # define a function that takes filename as input and loads the data from the pickle file
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    print(f'loaded {filename} successfully')
    return data
