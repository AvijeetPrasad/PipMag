from bs4 import BeautifulSoup
from datetime import datetime
import os
import pandas as pd
import re
import requests
from pandas import DataFrame, to_datetime
from datetime import timedelta
from distutils.util import strtobool


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
        A dictionary of video links for the observation dates.
        The keys are the observation dates in the format '20??-??-??',
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
    (The `get_image_links` function is called with the provided observation dates,
    and a dictionary of image links for each observation date is returned.)
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


def load_or_fetch_links(reload=False, media_links_file='all_media_links.csv'):
    """
    Load media links from a specified file if it exists; otherwise, fetch the links from the La Palma website.

    Parameters
    ----------
    reload : bool, optional
        Flag to indicate whether to reload the media links from the La Palma website. Default is False.
    media_links_file : str, optional
        The name of the CSV file where media links are saved. Default is 'all_media_links.csv'.

    Returns
    -------
    list
        List of all media links either loaded from the file or fetched from the website.

    Dependencies
    ------------
    os
    pandas
    get_obs_years
    get_obs_dates
    get_video_links
    get_image_links
    get_all_links

    Notes
    -----
    Function Name: load_or_fetch_links
    The function checks for the existence of the MEDIA_LINKS_FILE.
    If the file exists and the reload flag is False,
    the function reads the file to load the media links.
    Otherwise, it fetches the media links from the La Palma website,
    sorts them, and saves them to the specified file.

    Examples
    --------
    >>> load_or_fetch_links()
    ['link1', 'link2', 'link3']

    >>> load_or_fetch_links(reload=True)
    ['new_link1', 'new_link2', 'new_link3']
    """

    # Check if MEDIA_LINKS_FILE exists then load the file, otherwise get the links
    if os.path.isfile(media_links_file):
        links_df = pd.read_csv(media_links_file)
        all_media_links = links_df['Links'].tolist()
    else:
        print("File not found!")
        print("Fetching links from the La Palma website by setting 'reload=True'...")

        # Confirm with the user if they want to reload, as it takes a long time
    if reload:
        user_input = input("Fetching links from the La Palma website takes a few minutes. Continue? (y/n): ")
        if user_input.lower() != 'y':
            print("Loading existing file!.")
            return all_media_links

        # Fetch observation years and dates
        obs_years = get_obs_years()

        obs_dates = get_obs_dates(obs_years)

        # Get video and image links for each observation date
        print("Fetching links...")
        video_links = get_video_liks(obs_dates)
        image_links = get_image_links(obs_dates)

        # Get all video and image links
        all_video_links = get_all_links(video_links)

        all_image_links = get_all_links(image_links)

        # Combine and sort all media links
        all_media_links = sorted(all_image_links + all_video_links)

        # Save media links to file
        links_df = pd.DataFrame(all_media_links, columns=['Links'])
        links_df.to_csv(media_links_file, index=False)

    return all_media_links

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
    """
    Extracts date and time information from a list of image links using multiple date patterns.

    Parameters
    ----------
    links_list : list
        A list of image links from which to extract the date and time information.
    date_pattern_list : list, optional
        A list of regular expression patterns used to capture the date and time from the image links.
        Each pattern is sequentially applied until a match is found.
        The default patterns include common date formats such as 'YYYY-MM-DD_HH:MM:SS', 'YYYY-MM-DD_HHMMSS',
        'YYYY-MM-DDTHH:MM:SS', 'DDMonYY_HHMMSS', 'DDMonYYYY_HHMMSS', 'YYYY.MM.DD_HHMMSS', and 'YYYYMMDD_HHMMSS'.
        Note that the patterns are tried in the order they appear in the list.

    Returns
    -------
    tuple
        A tuple containing two lists: date_time_list and date_time_not_found_list.
        - date_time_list : list
            A list of formatted date and time strings extracted from the image links.
            The format of the date and time strings is 'YYYY-MM-DD_HH:MM:SS'.
        - date_time_not_found_list : list
            A list of image links for which the date
            and time information could not be found using any of the provided patterns.

    Dependencies
    ------------
    re (Regular Expression) module
    get_date_time_from_link function

    Notes
    -----
    Function Name: get_date_time_from_link_list
    This function takes a list of image links and a list of date patterns as input.
    It sequentially tries to extract the date and time information from each image link using the provided patterns.
    If a match is found, the date and time information is formatted into a string in the 'YYYY-MM-DD_HH:MM:SS' format
    and added to the date_time_list.
    If the date and time information is not found using any of the patterns,
    the image link is added to the date_time_not_found_list.
    The function returns a tuple containing the date_time_list and date_time_not_found_list.

    Examples
    --------
    >>> links = ['http://example.com/2022-01-01_12:34:56/image.jpg',
                 'http://example.com/20220101_123456/image.jpg',
                 'http://example.com/2022-01-01T12:34:56/image.jpg']
    >>> get_date_time_from_link_list(links)
    (['2022-01-01_12:34:56'], ['http://example.com/20220101_123456/image.jpg',
      'http://example.com/2022-01-01T12:34:56/image.jpg'])
    (The `get_date_time_from_link_list` function is called with the provided links,
    and the formatted date and time string and unmatched links are returned in a tuple.)
    """
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
    """
    Checks if a date string matches any of the specified date formats.

    Parameters
    ----------
    date_string : str
        The date string to be checked.
    date_format_list : list
        A list of date formats against which the date string will be compared.

    Returns
    -------
    str or None
        If the date string matches any of the specified date formats, the matching format is returned as a string.
        If the date string does not match any of the specified formats, None is returned.

    Dependencies
    ------------
    datetime module from datetime library

    Notes
    -----
    Function Name: check_date_format
    This function takes a date string and a list of date formats as input.
    It iterates through the date_format_list and attempts to match the date string with each format.
    If a match is found, the matching format is returned as a string.
    If the date string does not match any of the specified formats, None is returned.
    Note that the function assumes the date_string is in a valid format and does not perform any validation.

    Examples
    --------
    >>> date_str = '2022-01-01_12:34:56'
    >>> format_list = ['%Y-%m-%d_%H:%M:%S', '%Y%m%d_%H%M%S', '%Y-%m-%dT%H:%M:%S']
    >>> check_date_format(date_str, format_list)
    '%Y-%m-%d_%H:%M:%S'
    (The `check_date_format` function is called with the provided date string and format list.
    The matching format '%Y-%m-%d_%H:%M:%S' is returned.)
    """
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
    """
    Retrieves the invalid dates from a list of date-time strings by comparing them against a list of date formats.

    Parameters
    ----------
    date_time_list : list
        A list of date-time strings to be checked for validity.
    date_format_list : list, optional
        A list of date formats against which the date-time strings will be compared.
        Default formats include '%Y-%m-%d_%H:%M:%S', '%d%b%Y_%H:%M:%S', '%Y.%m.%d_%H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f', '%Y%m%d_%H%M%S', '%Y%m%d_%H:%M:%S'.
        (Default: ['%Y-%m-%d_%H:%M:%S', '%d%b%Y_%H:%M:%S', '%Y.%m.%d_%H:%M:%S', '%Y-%m-%d %H:%M:%S.%f',
                   '%Y%m%d_%H%M%S', '%Y%m%d_%H:%M:%S'])

    Returns
    -------
    list
        A list of invalid date-time strings that do not match any of the specified formats.

    Dependencies
    ------------
    pandas module

    Notes
    -----
    Function Name: get_invalid_dates
    This function takes a list of date-time strings and an optional list of date formats as input.
    It compares each date-time string with the formats in the date_format_list.
    If a date-time string matches any of the formats, it is considered valid.
    If a date-time string does not match any of the formats,
    it is considered invalid and added to the invalid_dates list.
    The function returns the list of invalid date-time strings.
    Note that the function assumes the date-time strings are in a valid format and does not perform any validation.

    Examples
    --------
    >>> dates = ['2022-01-01_12:34:56', '2022-13-01_12:34:56', '20220101_123456']
    >>> get_invalid_dates(dates)
    ['2022-13-01_12:34:56']
    (The `get_invalid_dates` function is called with the provided list of date-time strings.
    The date '2022-13-01_12:34:56' does not match any of the specified formats and is considered invalid.
    The function returns a list containing the invalid date-time string.)
    """

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

def preprocess_links(all_media_links):
    """
    Preprocess a list of media links by extracting date and time information and filtering out invalid dates.

    Parameters
    ----------
    all_media_links : list
        A list of media links that contain date and time information to be extracted and validated.

    Returns
    -------
    tuple
        A tuple containing two lists:
        - date_time_from_all_media_links : list
            A list of valid date and time strings extracted from the media links.
        - all_media_links_with_date_time : list
            A list of media links that have valid date and time information.

    Dependencies
    ------------
    get_date_time_from_link_list
    get_invalid_dates

    Notes
    -----
    Function Name: preprocess_links
    This function preprocesses the media links by first extracting date and time information using the
    `get_date_time_from_link_list` function. It then filters out media links that do not have valid date and time
    information. Finally, it filters out invalid dates from the extracted date and time list using the
    `get_invalid_dates` function.

    Examples
    --------
    >>> media_links = ['http://example.com/2022-01-01_12:34:56/image.jpg',
                        'http://example.com/20220101_123456/image.jpg',
                        'http://example.com/2022-01-01T12:34:56/image.jpg']
    >>> preprocess_links(media_links)
    (['2022-01-01_12:34:56'], ['http://example.com/2022-01-01_12:34:56/image.jpg'])
    (The `preprocess_links` function is called with the provided media links,
    and the valid date and time strings and corresponding media links are returned in a tuple.)
    """
    # Get date and time from link list
    date_time_from_all_media_links, date_time_not_found = get_date_time_from_link_list(all_media_links)

    # Filter out links without date and time
    all_media_links_with_date_time = [link for link in all_media_links if link not in date_time_not_found]

    # Filter out invalid dates
    invalid_dates = get_invalid_dates(date_time_from_all_media_links)
    date_time_from_all_media_links = [date for date in date_time_from_all_media_links if date not in invalid_dates]

    return date_time_from_all_media_links, all_media_links_with_date_time


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
    """
    Converts a list of datetime strings to datetime objects using specified date formats.

    Parameters
    ----------
    date_time_list : list
        A list of datetime strings to be converted to datetime objects.
    date_format_list : list, optional
        A list of date formats used for parsing the datetime strings.
        Default formats include '%Y-%m-%d_%H:%M:%S', '%d%b%Y_%H:%M:%S', '%Y.%m.%d_%H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f', '%Y%m%d_%H%M%S', '%Y%m%d_%H:%M:%S'.
        (Default: ['%Y-%m-%d_%H:%M:%S', '%d%b%Y_%H:%M:%S', '%Y.%m.%d_%H:%M:%S', '%Y-%m-%d %H:%M:%S.%f',
                   '%Y%m%d_%H%M%S', '%Y%m%d_%H:%M:%S'])

    Returns
    -------
    list
        A list of datetime objects converted from the datetime strings.

    Dependencies
    ------------
    datetime module

    Notes
    -----
    Function Name: convert_to_datetime
    This function takes a list of datetime strings and an optional list of date formats as input.
    It iterates over each datetime string and tries to convert it to a datetime object using the specified formats.
    If a datetime string matches any of the formats,
    it is converted to a datetime object and added to the date_time_obj_list.
    The function returns the list of datetime objects.
    Note that the function assumes the datetime strings are in a valid format and does not perform any validation.

    Examples
    --------
    >>> dates = ['2022-01-01_12:34:56', '01Jan2022_12:34:56']
    >>> convert_to_datetime(dates)
    [datetime.datetime(2022, 1, 1, 12, 34, 56)]
    (The `convert_to_datetime` function is called with the provided list of datetime strings.
    The first datetime string '2022-01-01_12:34:56' matches the specified format '%Y-%m-%d_%H:%M:%S'
    and is successfully converted to a datetime object.
    The function returns a list containing the converted datetime object.)
    """
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
    """
    Searches for a string pattern in a list of strings and returns the matched strings.

    Parameters
    ----------
    string_list : list
        A list of strings to be searched.
    pattern : str
        The string pattern to search for in the list of strings.

    Returns
    -------
    list or None
        A list of matched strings if the pattern is found in the string_list.
        If no matches are found, None is returned.

    Dependencies
    ------------
    re module

    Notes
    -----
    Function Name: search_string_in_list
    This function takes a list of strings and a string pattern as input.
    It iterates over each string in the string_list
    and checks if the pattern is found in the string using regular expressions.
    If a match is found, the string is added to the matched_string list.
    If no matches are found, None is returned.
    The function returns a list of matched strings or None.

    Examples
    --------
    >>> strings = ['apple', 'banana', 'orange']
    >>> search_string_in_list(strings, 'an')
    ['banana', 'orange']
    (The `search_string_in_list` function is called with the provided list of strings and the pattern 'an'.
    Both 'banana' and 'orange' contain the pattern 'an' and are returned as the matched strings.)
    """
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

def get_instrument_info(link_list, keywords, default_return=None, is_polarimetry=False):
    """
    Retrieves keywords from a list of links based on a given dictionary of keywords.

    Parameters
    ----------
    link_list : list
        A list of links to search for keywords.
    keywords : dict
        A dictionary where the keys represent categories (e.g., instruments, polarimetry)
        and the values are lists of keywords associated with each category.
    default_return : any, optional
        The value to return when no keywords are found. If not provided, None is returned.
    is_polarimetry : bool, optional
        Flag to indicate whether the keywords represent polarimetry. Default is False.

    Returns
    -------
    list or None
        A list of categories extracted from the link_list based on the keywords.
        If no keywords are found, default_return is returned.

    Dependencies
    ------------
    None

    Notes
    -----
    Function Name: get_instrument_info
    This function takes a list of links and a dictionary of keywords as input.
    It iterates over each link in the link_list and checks if any of the keywords are present in the link.
    If a keyword is found, the corresponding category is added to the result set.
    The function returns a list of categories extracted from the link_list based on the keywords,
    or default_return if no categories are found.

    Examples
    --------
    >>> links = ['http://example.com/telescope', 'http://example.com/camera',
    'http://example.com/spectrometer', 'http://example.com/Bz+Bh']
    >>> keyword_dict = {'Telescope': ['telescope'], 'Camera': ['camera'],
        'Spectrometer': ['spectrometer'], 'Polarimetry': ['Bz+Bh']}
    >>> get_instrument_info(links, keyword_dict)
    ['Telescope', 'Camera', 'Spectrometer', 'Polarimetry']
    (The `get_instrument_info` function is called with the provided list of links and keywords.
    The categories 'Telescope', 'Camera', 'Spectrometer',
    and 'Polarimetry' are extracted based on the keywords found in the links and returned as a list.)
    """

    result = set()
    for string in link_list:
        for category, category_keywords in keywords.items():
            for keyword in category_keywords:
                if keyword in string:
                    result.add(category)
                    break
    if len(result) == 0:
        return default_return
    if is_polarimetry:
        return True if 'True' in result else None
    return list(result)


def get_links_with_string(link_list, string_list):
    """
    Retrieves links that match specific string patterns from a list of links.

    Parameters
    ----------
    link_list : list
        A list of links to search.
    string_list : list
        A list of string patterns to search for in the links.

    Returns
    -------
    list
        A list of links that match the specified string patterns.

    Dependencies
    ------------
    None

    Notes
    -----
    Function Name: get_links_with_string
    This function takes a list of links and a list of string patterns as input.
    It iterates over each link in the link_list and checks if any of the string patterns are present in the link.
    If a pattern is found, the link is added to the result list.
    The function returns a list of links that match the specified string patterns.

    Examples
    --------
    >>> links = ['http://example.com/image1.jpg', 'http://example.com/image2.jpg', 'http://example.com/video1.mp4']
    >>> strings = ['image', 'video']
    >>> get_links_with_string(links, strings)
    ['http://example.com/image1.jpg', 'http://example.com/image2.jpg', 'http://example.com/video1.mp4']
    (The `get_links_with_string` function is called with the provided list of links and string patterns.
    The links that contain the strings 'image' or 'video' are returned as a list.)
    """

    # define function that takes a list of links, searches for string patterns
    # and returns a list of the links that matrch the patterns
    result = []
    for link in link_list:
        for string in string_list:
            if string in link:
                result.append(link)
    return result


def print_obs_dates(year, obs_dates):
    """
    Prints the observing dates for a given year from a list of observing dates.

    Parameters
    ----------
    year : str
        The year for which observing dates will be printed.
    obs_dates : list
        A list of observing dates.

    Returns
    -------
    None

    Dependencies
    ------------
    None

    Notes
    -----
    Function Name: print_obs_dates
    This function takes a year and a list of observing dates as input.
    It filters the observing dates that match the specified year and prints the first, last, and total number of dates.
    The observing dates are formatted as '20??-??-??' and printed with an enumerated list.

    Examples
    --------
    >>> dates = ['2022-01-01/', '2022-01-02/', '2022-01-03/']
    >>> print_obs_dates('2022', dates)
    first: 2022-01-01, last: 2022-01-03, total: 3
    01: 01
    02: 02
    03: 03
    (The `print_obs_dates` function is called with the provided year and observing dates.
    The observing dates for the year '2022' are printed with their corresponding numbers.)
    """

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
    """
    Finds observing dates that match a partial string from a list of observing dates.

    Parameters
    ----------
    partial_string : str
        The partial string to match against the observing dates.
    obs_dates : list
        A list of observing dates.

    Returns
    -------
    None

    Dependencies
    ------------
    None

    Notes
    -----
    Function Name: find_obs_dates
    This function takes a partial string and a list of observing dates as input.
    It filters the observing dates that contain the specified partial string and prints the matching dates.
    The observing dates are formatted as '20??-??-??' and printed with an enumerated list.
    If no matching dates are found, it prints a message indicating no observation dates were found.

    Examples
    --------
    >>> dates = ['2022-01-01/', '2022-01-02/', '2022-01-03/']
    >>> find_obs_dates('02', dates)
    01: 02
    (The `find_obs_dates` function is called with the provided partial string '02' and observing dates.
    The observing date '02' is printed as the matching date.)
    """
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

def generate_dataframe(date_time_from_all_media_links, all_media_links_with_date_time,
                       instrument_keywords={
                           'CRISP': ['wb_6563', 'ha', 'Crisp', '6173', '8542', '6563', 'crisp'],
                           'CHROMIS': ['Chromis', 'cak', '4846'],
                           'IRIS': ['sji']
                       },
                       polarimetry_keywords={
                           'True': ['Bz+Bh', 'blos', 'Blos']
                       }):
    """
    Generates a DataFrame containing media observation details from provided datetime strings and media links.

    Parameters
    ----------
    date_time_from_all_media_links : list
        A list of datetime strings representing the date and time of each media observation.
    all_media_links_with_date_time : list
        A list of media links corresponding to the date and time provided in `date_time_from_all_media_links`.
    instrument_keywords : dict, optional
        A dictionary where the keys represent instrument names
        and the values are lists of keywords associated with each instrument.
    polarimetry_keywords : dict, optional
        A dictionary containing keywords that identify if polarimetry was performed.

    Returns
    -------
    DataFrame
        A pandas DataFrame where each row represents a media observation.
        The DataFrame includes columns for datetime, instruments, targets,
        comments, video links, image links, and polarimetry.

    Dependencies
    ------------
    pandas module
    convert_to_datetime
    get_instrument_info
    get_links_with_string

    Notes
    -----
    Function Name: generate_dataframe
    The function initializes a DataFrame using provided datetime strings and media links.
    It extracts various features such as instruments, video links, and image links based on the media links.
    The function is designed to allow manual updating of some fields like 'polarimetry'.

    Examples
    --------
    >>> dt_links = ['2022-01-01_12:34:56', '2022-01-01_12:35:56']
    >>> media_links = [['http://example.com/2022-01-01_12:34:56/image.jpg'],
                       ['http://example.com/2022-01-01_12:35:56/video.mp4']]
    >>> df = generate_dataframe(dt_links, media_links)
    >>> print(df)
           date_time     instruments      targets      comments     video_links    image_links polarimetry
    0      2022-01-01_12:34:56  [...]     []  ""     []            [...]         None
    1      2022-01-01_12:35:56  [...]     []  "" comments  [...]          []           None
    """

    # Convert date and time to datetime objects
    date_time_objects = convert_to_datetime(date_time_from_all_media_links)

    # Create DataFrame with datetime index
    df = pd.DataFrame({'links': all_media_links_with_date_time}, index=date_time_objects)

    # Group links by datetime index
    df = df.groupby(df.index).agg({'links': lambda x: list(x)})
    df['obs_id'] = range(len(df))
    df['date_time'] = df.index
    df = df.set_index('obs_id')

    # Initialize additional columns
    df['comments'] = None
    df['polarimetry'] = None

    # Use apply to update DataFrame
    df['instruments'] = df['links'].apply(lambda x: get_instrument_info(x, keywords=instrument_keywords))
    df['targets'] = df.apply(lambda x: [], axis=1)
    df['polarimetry'] = df['links'].apply(lambda x: get_instrument_info(
        x, keywords=polarimetry_keywords, is_polarimetry=True))
    df['video_links'] = df['links'].apply(lambda x: get_links_with_string(x, ['mp4', 'mov']))
    df['image_links'] = df['links'].apply(lambda x: get_links_with_string(x, ['jpg', 'png']))
    # Drop links column
    df.drop('links', axis=1, inplace=True)

    # Reorder columns
    column_order = ['date_time', 'instruments', 'targets', 'polarimetry', 'comments', 'video_links', 'image_links']
    df = df[column_order]

    return df

def fix_duplicate_times(df: DataFrame, TIME_DIFF_THRESHOLD_SECONDS: int = 60) -> DataFrame:
    """
    Fix duplicate times in DataFrame by grouping rows based on time proximity.

    Parameters
    ----------
    df : DataFrame
        The DataFrame containing media observation details.
    TIME_DIFF_THRESHOLD_SECONDS : int, optional
        Time difference threshold in seconds. Default is 60.

    Returns
    -------
    DataFrame
        A new DataFrame where rows with similar 'date_time' values are grouped.

    Notes
    -----
    Function Name: fix_duplicate_times
    This function converts the 'date_time' column to DateTime objects and sorts the DataFrame.
    It then groups the DataFrame based on time proximity and aggregates each column.
    Duplicates in the 'instruments' and 'polarimetry' columns are removed.
    """

    # Convert 'date_time' column to DateTime type and sort DataFrame by 'date_time'
    df['date_time'] = to_datetime(df['date_time'])
    sorted_df = df.sort_values('date_time')

    # Define threshold for time difference
    threshold = timedelta(seconds=TIME_DIFF_THRESHOLD_SECONDS)

    # Group rows based on time proximity
    grouped_df = sorted_df.groupby((sorted_df['date_time'].diff() > threshold).cumsum()).agg({
        'date_time': 'first',
        'instruments': lambda x: list(set(item for sublist in x if sublist is not None for item in sublist)),
        'targets': 'first',
        'comments': 'first',
        'video_links': lambda x: list(set(item for sublist in x if sublist is not None for item in sublist)),
        'image_links': lambda x: list(set(item for sublist in x if sublist is not None for item in sublist)),
        'polarimetry': 'first'
    })

    # Convert 'date_time' column back to native Python datetime
    grouped_df['date_time'] = grouped_df['date_time'].apply(lambda x: x.to_pydatetime())

    return grouped_df

def add_existing_and_new_dataframes(new_df: pd.DataFrame,
                                    LA_PALMA_OBS_DATA_FILE: str = 'la_palma_obs_data.csv') -> pd.DataFrame:
    """
    Add a potential new DataFrame to the old DataFrame file without losing any data.

    Parameters
    ----------
    new_df : pd.DataFrame
        New DataFrame containing media observation details.
    LA_PALMA_OBS_DATA_FILE : str, optional
        File name of the existing DataFrame CSV file. Default is 'la_palma_obs_data.csv'.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the merged data.

    Notes
    -----
    Function Name: add_existing_and_new_dataframes
    This function loads an existing DataFrame from a CSV file, performs necessary data type conversions,
    and then concatenates it with the new DataFrame. Duplicates, if any, are removed.
    """

    # Load the existing CSV file as a DataFrame
    try:
        existing_df = pd.read_csv(LA_PALMA_OBS_DATA_FILE)
    except FileNotFoundError:
        print(f"File {LA_PALMA_OBS_DATA_FILE} not found. Creating a new DataFrame.")
        return new_df

    # Convert 'date_time' column to DateTime type
    existing_df['date_time'] = pd.to_datetime(existing_df['date_time'])
    new_df['date_time'] = pd.to_datetime(new_df['date_time'])

    # List of columns to convert from strings to lists
    columns_to_convert = ['video_links', 'image_links', 'instruments']

    # Convert the strings in each column back to lists
    for col in columns_to_convert:
        existing_df[col] = existing_df[col].apply(lambda x: x.split(';') if isinstance(x, str) else [])
        new_df[col] = new_df[col].apply(lambda x: x.split(';') if isinstance(x, str) else [])

    # List of columns to convert from NaN to None
    columns_to_convert = ['comments', 'polarimetry', 'targets']

    # Convert the NaNs in each column back to None
    for col in columns_to_convert:
        existing_df[col] = existing_df[col].apply(lambda x: None if pd.isna(x) else x)
        new_df[col] = new_df[col].apply(lambda x: None if pd.isna(x) else x)

    # Concatenate the existing DataFrame and the new DataFrame
    combined_df = pd.concat([existing_df, new_df])

    # Remove duplicates based on 'date_time'
    combined_df.drop_duplicates(subset=['date_time'], inplace=True, keep='first')

    # Optionally, you can save the combined DataFrame back to the CSV
    # combined_df.to_csv(LA_PALMA_OBS_DATA_FILE, index=False)

    return combined_df


def save_dataframe_to_csv(df, csv_filename, index=False):
    # Identify columns that contain lists
    columns_to_convert = [col for col, dtype in zip(
        df.columns, df.dtypes) if isinstance(df.loc[df.first_valid_index(), col], list)]

    # Convert lists to strings
    for col in columns_to_convert:
        df[col] = df[col].apply(lambda x: ';'.join(map(str, x)) if x is not None else None)

    # Convert None to empty string
    df.fillna("", inplace=True)

    # Convert boolean columns to string
    boolean_columns = [col for col in df.columns if df[col].dtype == 'bool']
    for col in boolean_columns:
        df[col] = df[col].apply(lambda x: str(x) if x is not None else x)

    # Save to CSV, optionally include index
    df.to_csv(csv_filename, index=index)

def read_csv_to_dataframe(csv_filename, list_columns=None):
    """
    Reads a CSV file and returns a DataFrame, converting specific columns back to lists, None, and booleans.

    Parameters:
        csv_filename (str): The name of the CSV file to read.
        list_columns (list, optional): List of columns which should be of list type.

    Returns:
        pd.DataFrame: The DataFrame containing the CSV data.
    """
    # Read CSV to DataFrame
    df = pd.read_csv(csv_filename, dtype=str)

    # Convert columns that should contain lists
    if list_columns is not None:
        for col in list_columns:
            df[col] = df[col].apply(lambda x: x.split(';') if pd.notna(x) else [])

    # Convert empty strings back to None
    df.replace("", None, inplace=True)

    # Convert NaN to None for all non-list columns
    for col in df.columns:
        if col not in list_columns:
            df[col] = df[col].apply(lambda x: None if pd.isna(x) else x)

    # Convert string 'True'/'False' back to boolean
    boolean_columns = [col for col in df.columns if df[col].astype(str).str.contains('True|False').any()]
    for col in boolean_columns:
        df[col] = df[col].apply(lambda x: bool(strtobool(x)) if pd.notna(x) and isinstance(x, str) else None)

    return df
