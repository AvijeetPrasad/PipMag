import pickle
from datetime import datetime
import glob
import os

def add_timestamp(file_name):
    # update the add_timestamp function to detect the extension of the file
    # name and add the timestamp before the extension
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
    # define a function that takes data and filename as input and saves the data as a pickle file
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def load_pickle(filename):
    # define a function that takes filename as input and loads the data from the pickle file
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    print(f'loaded {filename} successfully')
    return data
