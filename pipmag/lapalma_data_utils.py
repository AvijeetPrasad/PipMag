import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import pandas as pd


def get_obs_years(la_palma_url='http://tsih3.uio.no/lapalma/', verbose=False):
    """
    Get the observation years available at the La Palma Observatory.

    Parameters
    ----------
    la_palma_url : str, optional
        The URL of the parent directory containing the observation year subdirectories
        (default: 'http://tsih3.uio.no/lapalma/').
    verbose : bool, optional
        Flag indicating whether to print the observation years (default: False).

    Returns
    -------
    list
        A list of observation years available at the La Palma Observatory.

    Dependencies
    ------------
    - requests: Required for making HTTP requests to retrieve the webpage content.
    - BeautifulSoup: Required for parsing the HTML content of the webpage.

    Notes
    -----
    Function Name: get_obs_years
    This function retrieves the observation years available at the La Palma Observatory from the specified URL.
    It makes an HTTP GET request to the URL and uses BeautifulSoup to parse the HTML content of the webpage.
    It extracts the subdirectories (observation years) from the webpage links
    and filters them to include only those starting with '20'.
    If `verbose` is set to True, it prints the observation years in a formatted list.
    The function returns a list of observation years available at the La Palma Observatory.

    Examples
    --------
    >>> get_obs_years()
    (The `get_obs_years` function is called without any arguments, and a list of observation years is returned.)
    >>> get_obs_years(la_palma_url='http://tsih3.uio.no/lapalma/', verbose=True)
    (The `get_obs_years` function is called with the verbose flag set to True,
    and the observation years are printed in a formatted list.)
    """
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
    """
    Get the observation dates available at the La Palma Observatory for the specified observation years.

    Parameters
    ----------
    obs_years : list
        A list of observation years to retrieve the observation dates for.
    lapalma_url : str, optional
        The URL of the parent directory containing the observation date subdirectories
        (default: 'http://tsih3.uio.no/lapalma/').
    verbose : bool, optional
        Flag indicating whether to print additional information,
        such as the first entry, last entry, and total observing dates
        (default: False).

    Returns
    -------
    list
        A list of observation dates available at the La Palma Observatory for the specified observation years.

    Dependencies
    ------------
    - requests: Required for making HTTP requests to retrieve the webpage content.
    - BeautifulSoup: Required for parsing the HTML content of the webpage.

    Notes
    -----
    Function Name: get_obs_dates
    This function retrieves the observation dates available at the La Palma Observatory
    for the specified observation years.
    It iterates over each observation year in the `obs_years` list
    and makes an HTTP GET request to retrieve the webpage content of the corresponding directory.
    It uses BeautifulSoup to parse the HTML content
    and extract the subdirectories (observation dates) from the webpage links.
    It filters the subdirectories to include only those starting with '20'
    and containing two forward slashes ('/') to match the format '20??/20??-??-??/'.
    If `verbose` is set to True, it prints additional information, such as the first entry,
    last entry, and total number of observing dates.
    The function returns a list of observation dates available
    at the La Palma Observatory for the specified observation years.

    Examples
    --------
    >>> obs_years = ['2022', '2023']
    >>> get_obs_dates(obs_years)
    (The `get_obs_dates` function is called with the specified observation years,
    and a list of observation dates is returned.)
    >>> get_obs_dates(obs_years, lapalma_url='http://tsih3.uio.no/lapalma/', verbose=True)
    (The `get_obs_dates` function is called with the specified observation years
    and verbose flag set to True, and additional information is printed along with the observation dates.)
    """
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
    """
    Get a list of observation dates in the format '20??-??-??' from the provided observation dates.

    Parameters
    ----------
    obs_dates : list
        A list of observation dates to convert.

    Returns
    -------
    list
        A list of observation dates in the format '20??-??-??'.

    Dependencies
    ------------
    None

    Notes
    -----
    Function Name: get_obs_dates_list
    This function takes a list of observation dates in the format '20??/20??-??-??/'
    and extracts the date portion in the format '20??-??-??'.
    It removes the trailing slash and the year in the front to get the date portion of each observation date.
    If the separator between year, month, and day is not a dash ('-'), it replaces it with a dash.
    The function then removes any repeating dates using a set and converts the set back to a sorted list.
    The resulting list contains unique observation dates in the format '20??-??-??'.

    Examples
    --------
    >>> obs_dates = ['2022/2022-01-01/', '2022/2022-02-15/', '2022/2022-01-01/', '2022/2022-03-10/']
    >>> get_obs_dates_list(obs_dates)
    (The `get_obs_dates_list` function is called with the provided observation dates,
    and a list of unique observation dates in the format '20??-??-??' is returned.)
    """
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
    """
    Get a list of files with the specified file extension from the provided URL.

    Parameters
    ----------
    url : str
        The URL of the directory to search for files.
    file_extension : str
        The file extension to filter the files (e.g., '.txt', '.csv', '.pdf').

    Returns
    -------
    list
        A list of files with the specified file extension.

    Dependencies
    ------------
    - requests: Required for making HTTP requests to retrieve the webpage content.
    - BeautifulSoup: Required for parsing the HTML content of the webpage.

    Notes
    -----
    Function Name: get_files
    This function takes a URL and a file extension as input
    and retrieves a list of files with the specified file extension from the provided URL.
    It makes an HTTP GET request to the URL and uses BeautifulSoup to parse the HTML content of the webpage.
    It extracts the links to files with the specified file extension and appends them to the `files` list.
    If the `files` list is empty, it recursively searches the subdirectories
    by making additional HTTP GET requests to the subdirectory URLs and calling the `get_files` function recursively.
    The function returns a list of files with the specified file extension found in the provided URL
    and its subdirectories.

    Examples
    --------
    >>> url = 'http://example.com/files/'
    >>> file_extension = '.txt'
    >>> get_files(url, file_extension)
    (The `get_files` function is called with the specified URL and file extension,
    and a list of files with the specified file extension is returned.)
    """
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
    """
    Get a dictionary of video links for the provided observation dates.

    Parameters
    ----------
    obs_dates : list
        A list of observation dates in the format '20??/20??-??-??/'.

    lapalma_url : str, optional
        The base URL of the La Palma directory (default is 'http://tsih3.uio.no/lapalma/').

    Returns
    -------
    dict
        A dictionary of video links for the observation dates. The keys are the observation dates in the format '20??-??-??',
        and the values are lists of video links with either '.mp4' or '.mov' extensions.

    Dependencies
    ------------
    - get_files: The `get_files` function is used internally to retrieve the list of files
    with '.mp4' or '.mov' extensions from the provided URL.

    Notes
    -----
    Function Name: get_video_links
    This function takes a list of observation dates in the format '20??/20??-??-??/'
    and retrieves a dictionary of video links for each observation date.
    For each observation date, it appends the video links with either '.mp4'
    or '.mov' extensions found in the corresponding directory to the dictionary.
    The keys in the dictionary are the observation dates in the format '20??-??-??',
    obtained by removing the trailing slash and replacing the dots with dashes.
    If no video links are found for an observation date, an empty string is stored
    as the corresponding value in the dictionary.
    The function returns a dictionary of video links for the provided observation dates.

    Examples
    --------
    >>> obs_dates = ['2022/2022-01-01/', '2022/2022-02-15/', '2022/2022-03-10/']
    >>> get_video_links(obs_dates)
    (The `get_video_links` function is called with the provided observation dates,
    and a dictionary of video links for each observation date is returned.)
    """
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
    """
    Get a dictionary of image links for the provided observation dates.

    Parameters
    ----------
    obs_dates : list
        A list of observation dates in the format '20??/20??-??-??/'.

    lapalma_url : str, optional
        The base URL of the La Palma directory (default is 'http://tsih3.uio.no/lapalma/').

    Returns
    -------
    dict
        A dictionary of image links for the observation dates. The keys are the observation dates 
        in the format '20??-??-??',
        and the values are lists of image links with the '.jpg' extension.

    Dependencies
    ------------
    - get_files: The `get_files` function is used internally to retrieve the list of files 
    with the '.jpg' extension from the provided URL.

    Notes
    -----
    Function Name: get_image_links
    This function takes a list of observation dates in the format '20??/20??-??-??/'
    and retrieves a dictionary of image links for each observation date.
    For each observation date, it appends the image links with the '.jpg' extension
    found in the corresponding directory to the dictionary.
    The keys in the dictionary are the observation dates in the format '20??-??-??',
    obtained by removing the trailing slash and replacing the dots with dashes.
    If no image links are found for an observation date,
    an empty string is stored as the corresponding value in the dictionary.
    The function returns a dictionary of image links for the provided observation dates.

    Examples
    --------
    >>> obs_dates = ['2022/2022-01-01/', '2022/2022-02-15/', '2022/2022-03-10/']
    >>> get_image_links(obs_dates)
    (The `get_image_links` function is called with the provided observation dates, and a dictionary of image links for each observation date is returned.)
    """
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
    """
    Get a single list of all the links from the provided dictionary of links, sorted alphabetically.

    Parameters
    ----------
    links : dict
        A dictionary of links. The keys represent categories or labels, and the values are lists of links.

    Returns
    -------
    list
        A single list of all the links from the provided dictionary, sorted alphabetically.

    Dependencies
    ------------
    None

    Notes
    -----
    Function Name: get_all_links
    This function takes a dictionary of links as input and returns a single list containing
    all the links from the dictionary.
    The links are extracted from the dictionary values, excluding any empty values represented by an empty string ('').
    The resulting list of links is sorted alphabetically.
    The function also prints the total number of links in the list.
    The function returns the sorted list of links.

    Examples
    --------
    >>> links = {'Category 1': ['link1', 'link2', 'link3'], 'Category 2': ['link4', 'link5']}
    >>> get_all_links(links)
    (The `get_all_links` function is called with the provided dictionary of links,
    and a single sorted list of all the links is returned.)
    """
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
    """
    Extracts date and time information from a given string using a regular expression pattern.

    Parameters
    ----------
    link : str
        The input string from which to extract the date and time information.
    pattern : str, optional
        The regular expression pattern used to capture the date and time as groups 1 and 2, respectively.
        The default pattern is r'(\d{4}-\d{2}-\d{2})_(\d{2}:\d{2}:\d{2})'.

    Returns
    -------
    str or None
        If the date and time information is found in the input string,
        it returns a formatted string with the date and time
        in the format 'YYYY-MM-DD_HH:MM:SS'. If the date and time information is not found, it returns None.

    Dependencies
    ------------
    re (Regular Expression) module

    Notes
    -----
    Function Name: get_date_time_from_link
    This function takes a string and a regular expression pattern as input
    and extracts the date and time information from the string.
    The pattern is used to match and capture the date and time information as groups 1 and 2.
    If the date and time information is found, it is formatted into a string in the 'YYYY-MM-DD_HH:MM:SS' format.
    The function returns the formatted string or None if the date and time information is not found.

    Examples
    --------
    >>> link = 'http://example.com/2022-01-01_12:34:56/image.jpg'
    >>> get_date_time_from_link(link)
    '2022-01-01_12:34:56'
    (The `get_date_time_from_link` function is called with the provided link,
    and the formatted date and time string is returned.)
    """
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
