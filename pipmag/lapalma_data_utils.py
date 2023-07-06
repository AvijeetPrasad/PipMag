import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import pandas as pd


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