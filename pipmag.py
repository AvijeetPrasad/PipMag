import requests
from bs4 import BeautifulSoup
import re
import pickle
from datetime import datetime
import glob
import os
import pandas as pd
from IPython.display import display, clear_output, Video, HTML
import ipywidgets as widgets


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


def get_obs_years(la_palma_url='http://tsih3.uio.no/lapalma/', verbose=False):
    # recursively get all the subdirectories in the parent url directory
    r = requests.get(la_palma_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    obs_years = [a['href'] for a in soup.find_all(
        'a', href=True) if a['href'].endswith('/')]
    # choose the subdirs that are of the form 20?? and ignore the rest
    obs_years = [s for s in obs_years if s.startswith('20')]
    # print the observation years withouth the trailing slash
    # for year in obs_years:
    # 	print(year[:-1])
    # print enumerated list of the observation years
    if verbose:
        print('The La Palma Observatory has data at UiO for the following years:')
        for i, year in enumerate(obs_years):
            print(f'{i+1:02d}. {year[:-1]}')
    return obs_years


def get_obs_dates(obs_years, lapalma_url='http://tsih3.uio.no/lapalma/', verbose=False):
    # recursively get all the subdirectories in the obs_years list
    obs_dates = []
    for subdir in obs_years:
        r = requests.get(lapalma_url + subdir)
        soup = BeautifulSoup(r.text, 'html.parser')
        obs_dates.extend([subdir + a['href']
                         for a in soup.find_all('a', href=True) if a['href'].endswith('/')])
    # select the directories that are of the form 20??/20??-??-??/ and ignore the rest
    obs_dates = [s for s in obs_dates if s.startswith(
        '20') and s.count('/') == 2]
    # print the first, last and total number of directories
    first_entry = obs_dates[0][:-1]
    last_entry = obs_dates[-1][:-1]
    # total_observing_dates = len(obs_dates)
    # split the first and last entry to remove the year in the front
    first_entry = first_entry.split('/', 1)[1]
    last_entry = last_entry.split('/', 1)[1]
    if verbose:
        print(
            f'first entry: {first_entry}\nlast entry : {last_entry}\ntotal observing dates: {len(obs_dates)}')
    return obs_dates


def get_obs_dates_list(obs_dates):
    # write a function that takes obs_dates as input a returns a list of dates in the format 20??-??-??
    # remove the trailing slash and the year in the front, and return the list in the form 20??-??-??
    obs_dates = [s[5:-1] for s in obs_dates]
    # if the sepatator is not a dash, replace it with a dash
    obs_dates_list = [s.replace('.', '-') for s in obs_dates]
    # remove the repeating dates from obs_dates_list by using set
    obs_dates_list = list(set(obs_dates_list))
    # sort the list again, as set does not preserve the ordering
    obs_dates_list = sorted(obs_dates_list)
    return obs_dates_list


def get_files(url, file_extension):
    # define a function that takes a url and a file extension as input and
    # returns a list of files with the given extension,
    # if the files are not founds it searches the subdirectories
    # get the list of files with the given extension
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    files = [url + a['href']
             for a in soup.find_all('a', href=True) if a['href'].endswith(file_extension)]
    # if the list is empty, recursively search the subdirectories
    if not files:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        subdirs = [url + a['href']
                   for a in soup.find_all('a', href=True) if a['href'].endswith('/')]
        for subdir in subdirs:
            files.extend(get_files(subdir, file_extension))
    return files


def get_video_liks(obs_dates, lapalma_url='http://tsih3.uio.no/lapalma/'):
    # for the obs_dates list, get the list of files with either .mp4 or .mov
    # extension and save it as a dictionary wih the key being the observing date
    #  if the files are not founds then add a None value to the dictionary
    video_links = {}
    # i = 0
    for obs_date in obs_dates:
        # get the list of files with either .mp4 or .mov extension
        files = get_files(lapalma_url + obs_date + '/', '.mp4') + \
            get_files(lapalma_url + obs_date + '/', '.mov')
        # if the list is not empty, save it as a dictionary wih the key being the observing date
        key = obs_date[5:-1]
        # replace the dots with dashes
        key = key.replace('.', '-')
        if files:
            video_links[key] = files
        # if the list is empty, add a None value to the dictionary
        else:
            video_links[key] = ''
    return video_links


def get_image_links(obs_dates, lapalma_url='http://tsih3.uio.no/lapalma/'):
    image_links = {}
    # i = 0
    for obs_date in obs_dates:
        # get the list of files with either .mp4 or .mov extension
        files = get_files(lapalma_url + obs_date + '/', '.jpg')
        # if the list is not empty, save it as a dictionary wih the key being the observing date
        key = obs_date[5:-1]
        # replace the dots with dashes
        key = key.replace('.', '-')
        if files:
            image_links[key] = files
        # if the list is empty, add a None value to the dictionary
        else:
            image_links[key] = ''
    return image_links


def get_all_links(links):
    # define a function that takes image_links as input
    # and returns a single list of all the image links sorted alphabetically
    all_links = []
    for key, value in links.items():
        # if the value is not None, extend the list with the value
        if value != '':
            all_links.extend(value)
    # sort the list alphabetically
    all_links_sorted = sorted(all_links)
    print(f'total number of links: {len(all_links_sorted)}')
    return all_links_sorted


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


def get_date_time_from_link(link,
                            pattern=r'(\d{4}-\d{2}-\d{2})_(\d{2}:\d{2}:\d{2})'):
    # write a function that takes a string as input and a regex pattern which captures the date and time as groups 1
    # and 2 and returns a list of tuples with the date and time as the first and second element of the tuple
    # get the date and time from the image link
    date_time = re.search(pattern, link)
    # if the date and time is found, return a list of tuples with the date
    # and time as the first and second element of the tuple
    if date_time:
        date = date_time.group(1)
        # replace the dots with dashes usig the re.sub function
        # date = re.sub(r'(\d{4}).(\d{2}).(\d{2})', r'\1-\2-\3', date)
        time = date_time.group(2)
        # caputre entries for time like '075627' and replace the with '07:56:27'
        time = re.sub(r'(\d{2})(\d{2})(\d{2})', r'\1:\2:\3', time)
        # combine the date and time into a string
        date_time = date + '_' + time
        return date_time
    # if the date and time is not found, return None
    else:
        return None


def get_date_time_from_link_list(links_list,
                                 date_pattern_list=[r'(\d{4}-\d{2}-\d{2})_(\d{2}:\d{2}:\d{2})',
                                                    r'(\d{4}-\d{2}-\d{2})_(\d{6})(?!\d)',
                                                    r'(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})',
                                                    r'(\d{2}[a-zA-Z]{3}\d{2})_(\d{6})(?!\d)',
                                                    r'(\d{2}[a-zA-Z]{3}\d{4})_(\d{6})(?!\d)',
                                                    r'(\d{4}\.\d{2}\.\d{2})_(\d{6})(?!\d)',
                                                    r'(\d{8})_(\d{6})(?!\d)']
                                 ):
    # define a function that takes date_pattern_list as input
    # and sequentially tries to get the date and time from the image link and
    date_time_list = []
    date_time_not_found_list = []
    for link in links_list:
        for date_pattern in date_pattern_list:
            date_time = get_date_time_from_link(link, date_pattern)
            if date_time:
                date_time_list.append(date_time)
                break
        if not date_time:
            date_time_not_found_list.append(link)
    return date_time_list, date_time_not_found_list


def check_date_format(date_string, date_format_list):
    # check if the format of the  string '2013-06-30_09:15:50' matches the any of the formats in the date_format_list:
    #  if it does, return the format if it does not, return None
    for date_format in date_format_list:
        try:
            datetime.strptime(date_string, date_format)
            pass
        except ValueError:
            print(date_string)
            pass
    return None


def get_invalid_dates(
    date_time_list,
    date_format_list=[
        '%Y-%m-%d_%H:%M:%S',
        '%d%b%Y_%H:%M:%S',
        '%Y.%m.%d_%H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y%m%d_%H%M%S',
        '%Y%m%d_%H:%M:%S'
    ]
):
    # define a function to take a list of date
    # and times compare it against a list of date and time formats and return the invalid dates
    invalid_dates = []
    for date in date_time_list:
        for date_format in date_format_list:
            try:
                pd.to_datetime(date, format=date_format)
                break
            except ValueError:
                if date_format == date_format_list[-1]:
                    invalid_dates.append(date)
    if len(invalid_dates) == 0:
        print('All dates in date_time_list are valid')
    else:
        print(f"Invalid dates: {invalid_dates}")
    return invalid_dates


def convert_to_datetime(
    date_time_list,
    date_format_list=[
        '%Y-%m-%d_%H:%M:%S',
        '%d%b%Y_%H:%M:%S',
        '%Y.%m.%d_%H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y%m%d_%H%M%S',
        '%Y%m%d_%H:%M:%S'
    ]
):
    # define a function that takes a list of datetime strings,
    # uses the date_format_list to convert them to datetime objects and returns a list of datetime objects
    date_time_obj_list = []
    for date_time in date_time_list:
        for date_format in date_format_list:
            try:
                date_time_obj = datetime.strptime(date_time, date_format)
                date_time_obj_list.append(date_time_obj)
            except ValueError:
                pass
    return date_time_obj_list


def search_string_in_list(string_list, pattern):
    # define a function that searches for a string pattern in a list of strings if the pattern is found,
    # return the string, if the pattern is not found, return None
    # test_string = search_string_in_list(all_media_links_with_date_time, '0160904')
    # print(test_string)
    matched_string = []
    for string in string_list:
        if re.search(pattern, string):
            matched_string.append(string)
    if len(matched_string) == 0:
        return None
    else:
        return matched_string


def get_instrument_info(link_list, instrument_keywords):
    # define a function that takes a list of links and a dictionary of instrument keywords
    # and returns a list of instruments
    result = set()
    for string in link_list:
        for instrument, keywords in instrument_keywords.items():
            for keyword in keywords:
                if keyword in string:
                    result.add(instrument)
                    break
    # if no instrument is found, return None
    if len(result) == 0:
        return None
    return list(result)


def get_links_with_string(link_list, string_list):
    # define function that takes a list of links, searches for string patterns
    # and returns a list of the links that matrch the patterns
    result = []
    for link in link_list:
        for string in string_list:
            if string in link:
                result.append(link)
    return result


def print_obs_dates(year, obs_dates):
    # define a function to print all the observing dates for a given year in the obs_dates list
    obs_dates_year = [s for s in obs_dates if s.startswith(year)]
    print(
        f'first: {obs_dates_year[0][:-1]}, last: {obs_dates_year[-1][:-1]}, total: {len(obs_dates_year)}')
    # remove the trailing slash and the year in the front, and return the list in the form 20??-??-??
    obs_dates_year = [s[5:-1] for s in obs_dates_year]
    formatted_obs_dates_year = []
    # print an enumerated list of the observing dates
    for i, obs_date in enumerate(obs_dates_year):
        # obs_date = [s.replace('.', '-') for s in obs_date.split('/')]
        # print i with 2 digits and the observing date
        print(f'{i+1:02d}: {obs_date}')
        formatted_obs_dates_year.append(obs_date)
    return None


def find_obs_dates(partial_string, obs_dates):
    # define a function that takes a partial string and returns all the strings that match it from the obs_dates list
    obs_dates_partial = [s for s in obs_dates if partial_string in s]
    # remove the trailing slash and the year in the front, and return the list in the form 20??-??-??
    obs_dates_partial = [s[5:-1] for s in obs_dates_partial]
    formatted_obs_dates_partial = []
    # print an enumerated list of the observing dates
    for i, obs_date in enumerate(obs_dates_partial):
        # print i with 2 digits and the observing date
        print(f'{i+1:02d}: {obs_date}')
        formatted_obs_dates_partial.append(obs_date)
    # if no match is found, print a message
    if len(obs_dates_partial) == 0:
        print('No observation dates found')
    return None


class MovieSelector:
    '''Class to create a widget to select a movie from a list of movies'''

    def __init__(self, df):
        self.df = df

    def get_links(self, date_time):
        return self.df[self.df['date_time'] == date_time]['video_links'].values[0]

    def create_widget(self):
        # Create a dropdown widget for the date_time column
        self.date_time_dropdown = widgets.Dropdown(
            options=self.df['date_time'], description='Date Time:')

        # Create a dropdown widget for the movie links column
        self.links_dropdown = widgets.Dropdown(
            options=[], description='Movie Links:')

        # Create a variable to store the selected link
        self.selected_link = ''

        # Create an output widget to display the selected link
        self.output = widgets.Output()

        # Function to update the links dropdown based on the selected date_time
        def update_links(change):
            date_time = change.new
            links = self.get_links(date_time)
            self.links_dropdown.options = links

        # Function to update the selected link when the links dropdown value changes
        def links_value_changed(change):
            self.selected_link = change.new

        # Register the function to be called when the date_time dropdown value changes
        self.date_time_dropdown.observe(update_links, names='value')

        # Register the function to be called when the links dropdown value changes
        self.links_dropdown.observe(links_value_changed, names='value')

        # Display the dropdown widgets and the output widget
        display(self.date_time_dropdown)
        display(self.links_dropdown)

        def display_selected_link_button(b):
            with self.output:
                clear_output()
                display(Video(self.selected_link))

        display_button = widgets.Button(description='Show')
        display_button.on_click(display_selected_link_button)
        display(display_button)
        display(self.output)


class VideoSelector:
    def __init__(self, df):
        self.df = df

    def create_widget(self):
        # Create a dropdown widget for the year column
        self.year_dropdown = widgets.Dropdown(
            options=self.df['year'].unique(), description='Year:')

        # Create a dropdown widget for the month column
        self.month_dropdown = widgets.Dropdown(
            options=[], description='Month:')

        # Create a dropdown widget for the day column
        self.day_dropdown = widgets.Dropdown(options=[], description='Day:')

        # Create a dropdown widget for the time column
        self.time_dropdown = widgets.Dropdown(options=[], description='Time:')

        # Create a dropdown widget for the links column
        self.links_dropdown = widgets.Dropdown(
            options=[], description='Links:')

        # Create a variable to store the selected link
        self.selected_link = ''

        # Create an output widget to display the selected link
        self.output = widgets.Output()

        # Function to update the month dropdown based on the selected year
        def update_months(change):
            year = change.new
            months = self.df[self.df['year'] == year]['month'].unique()
            self.month_dropdown.options = months

        # Function to update the day dropdown based on the selected month and year
        def update_days(change):
            year = self.year_dropdown.value
            month = change.new
            days = self.df[(self.df['year'] == year) & (
                self.df['month'] == month)]['day'].unique()
            self.day_dropdown.options = days

        # Function to update the time dropdown based on the selected day, month, and year
        def update_time(change):
            year = self.year_dropdown.value
            month = self.month_dropdown.value
            day = change.new
            time = self.df[(self.df['year'] == year) & (
                self.df['month'] == month) & (self.df['day'] == day)]['time'].unique()
            self.time_dropdown.options = time

        # Function to update the links dropdown based on the selected time
        def update_links(change):
            time = change.new
            links = list(self.df[self.df['time'] == time]
                         ['video_links'].values[0])
            self.links_dropdown.options = links

        # Function to update the selected link when the links dropdown value changes
        def links_value_changed(change):
            self.selected_link = change.new
            self.matches = self.df[self.df['video_links'].apply(
                lambda x: self.selected_link in x)]
            self.selected_index = self.matches.index[0]

        # Function to display the selected link when the display button is pressed
        def display_selected_link(b):
            with self.output:
                clear_output()
                display(Video(self.selected_link,
                        html_attributes='controls autoplay loop'))
                # print("Selected link index:", self.selected_index)
                display(widgets.HTML(
                    f"<h3><b>Index:</b> {self.selected_index}</h3>"))

        # Register the functions to be called when the year, month, and day dropdown values change
        self.year_dropdown.observe(update_months, names='value')
        self.month_dropdown.observe(update_days, names='value')
        self.day_dropdown.observe(update_time, names='value')

        # Register the function to be called when the time dropdown value changes
        self.time_dropdown.observe(update_links, names='value')

        # Register the function to be called when the links dropdown value changes
        self.links_dropdown.observe(links_value_changed, names='value')

        # Create a button widget to display the selected link
        self.display_button = widgets.Button(description='Show')
        self.display_button.on_click(display_selected_link)

        # Register the function to be called when the links dropdown value changes
        self.links_dropdown.observe(links_value_changed, names='value')
        # Display the dropdown widgets, the button, and the output widget
        display(self.year_dropdown)
        display(self.month_dropdown)
        display(self.day_dropdown)
        display(self.time_dropdown)
        display(self.links_dropdown)
        display(self.display_button)
        display(self.output)


class DataUpdater:
    def __init__(self, df, column_names):
        self.df = df
        self.column_names = column_names
        self.index_text = widgets.Text(description='Index:')
        self.value_texts = {}
        for column_name in self.column_names:
            self.value_texts[column_name] = widgets.Text(
                description=f'{column_name}:')
        self.update_button = widgets.Button(description='Update')
        self.output = widgets.Output()

        self.update_button.on_click(self.update_values)
        self.index_text.observe(self.display_existing_values, names='value')

    def update_values(self, b):
        index = int(self.index_text.value)
        for column_name in self.column_names:
            value = self.value_texts[column_name].value
            if isinstance(self.df.at[index, column_name], list):
                self.df.at[index, column_name] = value.split(',')
            else:
                self.df.at[index, column_name] = value
        with self.output:
            clear_output()
            display(widgets.HTML(
                f"<b>{', '.join(self.column_names)} updated for index {index}</b>"))

    def display_existing_values(self, change):
        if self.index_text.value:
            index = int(self.index_text.value)
            for column_name in self.column_names:
                existing_value = self.df.at[index, column_name]
                if isinstance(existing_value, list):
                    self.value_texts[column_name].value = ', '.join(
                        existing_value)
                else:
                    self.value_texts[column_name].value = existing_value if pd.notna(
                        existing_value) else ""

    def display(self):
        display(self.index_text)
        for column_name in self.column_names:
            display(self.value_texts[column_name])
        display(self.update_button)
        display(self.output)


class VideoSelector2:
    def __init__(self, df, column_names):
        self.df = df
        self.column_names = column_names

    def create_widget(self):
        # Create a dropdown widget for the year column
        self.year_dropdown = widgets.Dropdown(
            options=self.df['year'].unique(), description='Year:')

        # Create a dropdown widget for the month column
        self.month_dropdown = widgets.Dropdown(
            options=[], description='Month:')

        # Create a dropdown widget for the day column
        self.day_dropdown = widgets.Dropdown(options=[], description='Day:')

        # Create a dropdown widget for the time column
        self.time_dropdown = widgets.Dropdown(options=[], description='Time:')

        # Create a dropdown widget for the links column
        self.links_dropdown = widgets.Dropdown(
            options=[], description='Links:')

        # Create a variable to store the selected link
        self.selected_link = ''

        # Create an output widget to display the selected link
        self.output = widgets.Output()

        self.value_texts = {}
        for column_name in self.column_names:
            self.value_texts[column_name] = widgets.Text(
                description=f'{column_name}:')
        self.update_button = widgets.Button(description='Update')

        # Function to update the month dropdown based on the selected year
        def update_months(change):
            year = change.new
            months = self.df[self.df['year'] == year]['month'].unique()
            self.month_dropdown.options = months

        # Function to update the day dropdown based on the selected month and year
        def update_days(change):
            year = self.year_dropdown.value
            month = change.new
            days = self.df[(self.df['year'] == year) & (
                self.df['month'] == month)]['day'].unique()
            self.day_dropdown.options = days

        # Function to update the time dropdown based on the selected day, month, and year
        def update_time(change):
            year = self.year_dropdown.value
            month = self.month_dropdown.value
            day = change.new
            time = self.df[(self.df['year'] == year) & (
                self.df['month'] == month) & (self.df['day'] == day)]['time'].unique()
            self.time_dropdown.options = time

        # Function to update the links dropdown based on the selected time
        def update_links(change):
            time = change.new
            links = list(self.df[self.df['time'] == time]
                         ['video_links'].values[0])
            self.links_dropdown.options = links

        # Function to update the selected link when the links dropdown value changes
        def links_value_changed(change):
            self.selected_link = change.new
            self.matches = self.df[self.df['video_links'].apply(
                lambda x: self.selected_link in x)]
            self.selected_index = self.matches.index[0]

        # Function to display the selected link when the display button is pressed
        def display_selected_link(b):
            with self.output:
                clear_output()
                display(Video(self.selected_link,
                        html_attributes='controls autoplay loop'))
                # print("Selected link index:", self.selected_index)
                display(widgets.HTML(
                    f"<h3><b>Index:</b> {self.selected_index}</h3>"))

        # Function to update the index dropdown based on the selected time

        def update_values(b):
            index = int(self.selected_index)
            for column_name in self.column_names:
                value = self.value_texts[column_name].value
                if isinstance(self.df.at[index, column_name], list):
                    self.df.at[index, column_name] = value.split(',')
                else:
                    self.df.at[index, column_name] = value
            with self.output:
                clear_output()
                display(widgets.HTML(
                    f"<b>{', '.join(self.column_names)} updated for index {index}</b>"))

        def display_existing_values(change):
            if self.selected_index:
                index = int(self.selected_index)
                for column_name in self.column_names:
                    existing_value = self.df.at[index, column_name]
                    if isinstance(existing_value, list):
                        self.value_texts[column_name].value = ', '.join(
                            existing_value)
                    else:
                        self.value_texts[column_name].value = existing_value if pd.notna(
                            existing_value) else ""

        # Register the functions to be called when the year, month, and day dropdown values change
        self.year_dropdown.observe(update_months, names='value')
        self.month_dropdown.observe(update_days, names='value')
        self.day_dropdown.observe(update_time, names='value')

        # Register the function to be called when the time dropdown value changes
        self.time_dropdown.observe(update_links, names='value')

        # Register the function to be called when the links dropdown value changes
        self.links_dropdown.observe(links_value_changed, names='value')

        # Create a button widget to display the selected link
        self.display_button = widgets.Button(description='Show')
        self.display_button.on_click(display_selected_link)

        # Register the function to be called when the links dropdown value changes
        self.links_dropdown.observe(links_value_changed, names='value')
        self.links_dropdown.observe(display_existing_values, names='value')

        # Display the dropdown widgets, the button, and the output widget
        display(self.year_dropdown)
        display(self.month_dropdown)
        display(self.day_dropdown)
        display(self.time_dropdown)
        display(self.links_dropdown)
        display(self.display_button)

        display(self.output)

        # Details at the bottom of the video
        for column_name in self.column_names:
            display(self.value_texts[column_name])
        display(self.update_button)


class ADSSearch:
    '''Class to search the ADS API
    example usage:
    ads = ADSSearch()
    results = ads.search(["SST", "CRISP", "25 May 2017"])
    '''

    def __init__(self):
        self.api_token = os.environ.get("ADS_DEV_KEY")
        if not self.api_token:
            raise ValueError(
                "ADS API key not found. Please set the ADS_DEV_KEY environmental variable.")

    def search(self, search_terms):
        headers = {"Authorization": f"Bearer {self.api_token}"}

        # Construct the query string
        query_terms = " AND ".join(f"full:\"{term}\"" for term in search_terms)
        query = f"{query_terms}"

        # Set up the query parameters
        params = {
            "q": query,
            "fl": "id,title,bibcode,author,year",
            "rows": 100,
            "sort": "date desc"
        }

        # Make the API request
        response = requests.get(
            "https://api.adsabs.harvard.edu/v1/search/query", headers=headers, params=params)
        response_json = response.json()

        # Process the response and return the results
        results = []
        for paper in response_json["response"]["docs"]:
            result = {
                "title": paper["title"][0],
                "bibcode": paper["bibcode"],
                "first_author": paper["author"][0],
                "year": paper["year"],
                "url": f"https://ui.adsabs.harvard.edu/abs/{paper['bibcode']}"
            }
            results.append(result)
        return results


def datetime_to_string(dt):
    # convert datetime to string in the format 25 May 2017 if the date is two digits, otherwise 6 June 2019
    if dt.day < 10:
        return f"{dt.day} {dt.strftime('%B')} {dt.year}"
    else:
        return f"{dt.day} {dt.strftime('%B')} {dt.year}"


def get_search_terms(df, index):
    # function that take dataframe index, reads the datetime, converts into string,
    # and appends in to the instruments list to search ADS
    date_string = datetime_to_string(df.at[index, 'date_time'])
    instruments = df.at[index, 'instruments']
    # append date string to instruments list
    search_terms = ['SST'] + instruments + [date_string]
    return search_terms


def get_ads_results(search_terms):
    # function that takes a list of search terms and returns the ADS results
    ads = ADSSearch()
    results = ads.search(search_terms)
    return results


class ADS_Search(ADSSearch):
    '''Class to search the ADS API based on data in a Pandas DataFrame
    example usage:
    search = ADS_Search(dataframe)
    search.get_results(0)
    '''

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def get_results(self, index, pretty_print=False):
        search_terms = get_search_terms(self.dataframe, index)
        results = get_ads_results(search_terms)

        if pretty_print:
            headers = ["#", "Title", "First author", "Bibcode", "URL"]
            rows = [[i+1, result["title"], result["first_author"],
                     result["bibcode"], result["url"]] for i, result in enumerate(results)]
            df = pd.DataFrame(rows, columns=headers)
            if len(rows) > 0:
                # Generate the HTML table with links and disable HTML escaping
                html_table = df.to_html(
                    render_links=True, escape=False, index=False)

                # Define CSS style rules for the table cells and header cells
                cell_style = "td { text-align: left; }"
                header_style = "th { text-align: center; }"

                # Use the HTML module to display the table with the style rules
                display(
                    HTML(f'<style>{cell_style} {header_style}</style>{html_table}'))

        else:
            print(f"Search terms: {search_terms}")
            for i, result in enumerate(results):
                print(f"Result {i+1}:")
                print(f"Title: {result['title']}")
                print(f"Bibcode: {result['bibcode']}")
                print(result["first_author"])
                print(f"URL: {result['url']}")


class VideoSelector3:
    def __init__(self, df, column_names):
        self.df = df
        self.column_names = column_names

        # Adds a search of papers according to the selected day
        self.ads = ADS_Search(df)

    def create_widget(self):
        # Create a dropdown widget for the year column
        self.year_dropdown = widgets.Dropdown(
            options=self.df['year'].unique(), description='Year:')

        # Create a dropdown widget for the month column
        self.month_dropdown = widgets.Dropdown(
            options=[], description='Month:')

        # Create a dropdown widget for the day column
        self.day_dropdown = widgets.Dropdown(options=[], description='Day:')

        # Create a dropdown widget for the time column
        self.time_dropdown = widgets.Dropdown(options=[], description='Time:')

        # Create a dropdown widget for the links column
        self.links_dropdown = widgets.Dropdown(
            options=[], description='Links:')

        # Create a variable to store the selected link
        self.selected_link = ''

        # Create an output widget to display the selected link
        self.output = widgets.Output()

        # Create a text field to display the properties of the selected observations
        self.value_texts = {}
        for column_name in self.column_names:
            self.value_texts[column_name] = widgets.Text(
                description=f'{column_name}:')
        self.update_button = widgets.Button(description='Update')

        # Function to update the month dropdown based on the selected year
        def update_months(change):
            year = change.new
            months = self.df[self.df['year'] == year]['month'].unique()
            self.month_dropdown.options = months

        # Function to update the day dropdown based on the selected month and year
        def update_days(change):
            year = self.year_dropdown.value
            month = change.new
            days = self.df[(self.df['year'] == year) & (
                self.df['month'] == month)]['day'].unique()
            self.day_dropdown.options = days

        # Function to update the time dropdown based on the selected day, month, and year
        def update_time(change):
            year = self.year_dropdown.value
            month = self.month_dropdown.value
            day = change.new
            time = self.df[(self.df['year'] == year) & (
                self.df['month'] == month) & (self.df['day'] == day)]['time'].unique()
            self.time_dropdown.options = time

        # Function to update the links dropdown based on the selected time
        def update_links(change):
            time = change.new
            links = list(self.df[self.df['time'] == time]
                         ['video_links'].values[0])
            self.links_dropdown.options = links

        # Function to update the selected link when the links dropdown value changes
        def links_value_changed(change):
            self.selected_link = change.new
            self.matches = self.df[self.df['video_links'].apply(
                lambda x: self.selected_link in x)]
            self.selected_index = self.matches.index[0]

        # Function to display the selected link when the display button is pressed

        def display_selected_link(b):
            with self.output:
                clear_output()
                display(Video(self.selected_link,
                        html_attributes='controls autoplay loop'))
                # print("Selected link index:", self.selected_index)

                # Display the ADS results
                self.ads.get_results(self.selected_index, pretty_print=True)

                display(widgets.HTML(
                    f"<h3><b>Index:</b> {self.selected_index}</h3>"))

        # Function to update the index dropdown based on the selected time
        def update_values(b):
            index = int(self.selected_index)
            for column_name in self.column_names:
                value = self.value_texts[column_name].value
                if isinstance(self.df.at[index, column_name], list):
                    self.df.at[index, column_name] = value.split(',')
                else:
                    self.df.at[index, column_name] = value
            with self.output:
                clear_output()
                display(widgets.HTML(
                    f"<b>{', '.join(self.column_names)} updated for index {index}</b>"))

        def display_existing_values(change):

            if self.selected_index:
                index = int(self.selected_index)
                for column_name in self.column_names:
                    existing_value = self.df.at[index, column_name]
                    if isinstance(existing_value, list):
                        self.value_texts[column_name].value = ', '.join(
                            existing_value)
                    else:
                        self.value_texts[column_name].value = existing_value if pd.notna(
                            existing_value) else ""

        # Register the functions to be called when the year, month, and day dropdown values change
        self.year_dropdown.observe(update_months, names='value')
        self.month_dropdown.observe(update_days, names='value')
        self.day_dropdown.observe(update_time, names='value')

        # Register the function to be called when the time dropdown value changes
        self.time_dropdown.observe(update_links, names='value')

        # Register the function to be called when the links dropdown value changes
        self.links_dropdown.observe(links_value_changed, names='value')

        # Create a button widget to display the selected link
        self.display_button = widgets.Button(description='Show')
        self.display_button.on_click(display_selected_link)

        # Register the function to be called when the links dropdown value changes
        self.links_dropdown.observe(links_value_changed, names='value')
        self.links_dropdown.observe(display_existing_values, names='value')

        # Display the dropdown widgets, the button, and the output widget
        display(self.year_dropdown)
        display(self.month_dropdown)
        display(self.day_dropdown)
        display(self.time_dropdown)
        display(self.links_dropdown)
        display(self.display_button)

        # Display the video
        display(self.output)

        # Details at the bottom of the video
        for column_name in self.column_names:
            display(self.value_texts[column_name])
        display(self.update_button)
