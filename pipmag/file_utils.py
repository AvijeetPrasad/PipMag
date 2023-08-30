import pickle
from datetime import datetime
import glob
import os
import pandas as pd

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

def read_and_format_csv(file_path, expected_columns=None):
    """
    Reads a CSV file into a DataFrame and formats specified columns.
    The function includes both error handling and type checking.

    Parameters
    ----------
    file_path : str
        The path to the CSV file that is to be read.
    expected_columns : list, optional
        A list of column names that are expected to be in the DataFrame.
        The default is None, which skips the column check.

    Returns
    -------
    pd.DataFrame or str
        Returns a formatted DataFrame if the file reading and formatting are successful.
        Otherwise, returns an error message.

    Dependencies
    ------------
    pandas as pd

    Notes
    -----
    Function Name: read_and_format_csv
    The function reads a CSV file into a DataFrame and applies several formatting operations.
    These include converting the 'date_time' column to datetime format,
    converting specified columns from strings to lists, replacing NaN values with None in specified columns,
    and converting the 'polarimetry' column to a string.

    The function expects the CSV file to have the following format:
    ```
    date_time,year,month,day,time,instruments,target,comments,video_links,image_links,links,num_links,polarimetry
    2013-06-30 09:15:50,2013,6,30,09:15:50,CRISP; IRIS,Spicules,
    ,http://example.com/video,http://example.com/image,http://example.com/links,3,False
    ```

    Examples
    --------
    >>> read_and_format_csv('sample.csv', expected_columns=['date_time', 'year', 'month'])
    Returns a DataFrame with the specified formatting if the file and columns are valid.
    """

    try:
        # Read the DataFrame from the CSV file
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        return "Error: The specified file was not found."
    except pd.errors.EmptyDataError:
        return "Error: The file is empty."
    except pd.errors.ParserError:
        return "Error: The file could not be parsed."

    # Check if the DataFrame has the expected columns
    if expected_columns:
        if not set(expected_columns).issubset(set(df.columns)):
            return f"Error: Missing expected columns. Expected: {expected_columns}, Found: {list(df.columns)}"

    # Convert the 'date_time' column to datetime format
    df['date_time'] = pd.to_datetime(df['date_time'])

    # Columns to convert from strings to lists
    list_columns = ['links', 'video_links', 'image_links', 'instruments']

    # Convert the strings in each column to lists
    for col in list_columns:
        df[col] = df[col].apply(lambda x: x.split(';') if isinstance(x, str) else [])

    # Columns to convert from NaN to None
    nan_to_none_columns = ['comments', 'polarimetry', 'target']

    # Convert the NaNs in each column to None
    for col in nan_to_none_columns:
        df[col] = df[col].apply(lambda x: None if pd.isna(x) else x)

    # Convert the 'polarimetry' column to string format
    df['polarimetry'] = df['polarimetry'].apply(lambda x: str(x))

    return df


def preprocess_and_save_dataframe(df, la_palma_obs_data_file):
    """
    Preprocesses the input DataFrame and saves it as a .csv file.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing observational data columns such as 'target', 'links', 'video_links', 'image_links',
        and 'instruments'.
    la_palma_obs_data_file : str
        File path where the preprocessed DataFrame will be saved as a .csv file.

    Returns
    -------
    None
        The function saves the preprocessed DataFrame as a .csv file and does not return any value.

    Dependencies
    ------------
    pandas as pd

    Notes
    -----
    Function Name: preprocess_and_save_dataframe
    This function performs the following preprocessing steps:
    1. Rewrites specific keywords in the 'target' column to a standardized format.
    2. Converts lists in certain columns to semi-colon separated strings.
    3. Saves the preprocessed DataFrame to a .csv file.

    Examples
    --------
    >>> preprocess_and_save_dataframe(df, "path/to/save/file.csv")
    The DataFrame `df` will be preprocessed and saved at "path/to/save/file.csv".
    """

    def rewrite_keywords(text, target_keywords, replace_with):
        for keyword in target_keywords:
            if keyword in text:
                text = text.replace(keyword, replace_with)
        return text

    ACTIVE_REGION_KEYWORDS = {'active region', 'Active region', 'AR'}
    QUIET_SUN_KEYWORDS = {'quiet Sun', 'quiet sun', 'QS', 'Quiet sun'}
    SUNSPOT_KEYWORDS = {'sunspot', 'Sunspot', 'SS', 'ss', 'SUnspot'}

    df['target'] = df['target'].apply(lambda x: None if pd.isna(
        x) else rewrite_keywords(x, ACTIVE_REGION_KEYWORDS, "Active Region"))
    df['target'] = df['target'].apply(lambda x: None if pd.isna(
        x) else rewrite_keywords(x, QUIET_SUN_KEYWORDS, "Quiet Sun"))
    df['target'] = df['target'].apply(lambda x: None if pd.isna(
        x) else rewrite_keywords(x, SUNSPOT_KEYWORDS, "Sunspot"))

    df_copy = df.copy()

    columns_to_convert = ['links', 'video_links', 'image_links', 'instruments']
    for col in columns_to_convert:
        df_copy[col] = df_copy[col].apply(lambda x: ';'.join(x))

    df_copy.to_csv(la_palma_obs_data_file, index=False)


def read_and_format_csv_for_query(file_path):
    """
    Reads a CSV file into a pandas DataFrame and converts specific columns' NaN values to 'None'.

    Parameters
    ----------
    file_path : str
        The path to the CSV file to be read.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with NaN values in specified columns replaced with 'None'.

    Dependencies
    ------------
    pandas

    Notes
    -----
    Function Name: read_and_format_csv_for_query
    This function is specifically designed to prepare DataFrames for querying,
    by replacing NaN values in selected columns with 'None'.

    Examples
    --------
    >>> read_and_format_csv_for_query("path/to/csv/file.csv")
    DataFrame with NaNs in 'comments', 'polarimetry', and 'target' columns replaced by 'None'.
    """

    df = pd.read_csv(file_path)

    # List of columns to convert from NaN to None
    columns_to_convert = ['comments', 'polarimetry', 'target']

    # Convert the NaNs in each column back to None
    for col in columns_to_convert:
        df[col] = df[col].apply(lambda x: 'None' if pd.isna(x) else x)

    return df
