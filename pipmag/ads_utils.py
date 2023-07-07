import requests
import os
import pandas as pd
from IPython.display import display, HTML
import configparser


class ADSSearch:
    """
    Class for searching the ADS API.

    Parameters
    ----------
    None

    Attributes
    ----------
    api_token : str
        The API token used for authorization.

    Methods
    -------
    search(search_terms)
        Search the ADS API with the given search terms and return the results.

    Dependencies
    ------------
    - os: Required to retrieve the ADS API key from the environment.
    - requests: Required for making API requests to the ADS API.

    Notes
    -----
    Class Name: ADSSearch
    This class provides a convenient interface for searching the ADS API.
    The `api_token` attribute is initialized with the value of the `ADS_DEV_KEY` environmental variable.
    If the environmental variable is not set, a `ValueError` is raised.
    The `search` method performs a search using the given `search_terms` and returns a list of results.
    Each result is a dictionary with the keys: 'title', 'bibcode', 'first_author', 'year', and 'url'.
    The 'url' key provides a link to the paper on the ADS website.

    Examples
    --------
    >>> ads = ADSSearch()
    >>> results = ads.search(["SST", "CRISP", "25 May 2017"])
    (The `ADSSearch` class is instantiated, and a search is performed with the given search terms.)
    """

    def __init__(self):
        """
        Initialize the class instance by retrieving the ADS API key.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Dependencies
        ------------
        - os: Required to retrieve the ADS API key from the environment.

        Notes
        -----
        Function Name: __init__
        This special method is called when initializing an instance of a class.
        It retrieves the ADS API key from the environment by
        accessing the "ADS_DEV_KEY" environmental variable using `os.environ.get()`.
        If the API key is not found (i.e., `self.api_token` is None),
        a `ValueError` is raised with an appropriate error message.
        This ensures that the ADS API key is properly set before using the class instance.

        Examples
        --------
        >>> class_instance = ClassName()
        (The `__init__` method is automatically called upon instantiation of the class instance.)
        """

        self.api_token = os.environ.get("ADS_DEV_KEY")

        if not self.api_token:
            config = configparser.ConfigParser()
            config.read('../config.ini')
            self.api_token = config.get('DEFAULT', 'ADS_DEV_KEY', fallback=None)

        if not self.api_token:
            raise ValueError("ADS API key not found. Please set the ADS_DEV_KEY "
                             "environmental variable or add it to the config.ini file.")

    def search(self, search_terms):
        """
        Search the ADS API with the given search terms and return the results.

        Parameters
        ----------
        search_terms : list
            A list of search terms to query the ADS API.

        Returns
        -------
        list
            A list of dictionaries representing the search results.
            Each dictionary contains the keys: 'title', 'bibcode', 'first_author', 'year', and 'url'.

        Dependencies
        ------------
        - requests: Required for making API requests to the ADS API.

        Notes
        -----
        Function Name: search
        This method performs a search on the ADS API using the given search terms.
        It constructs the query string by joining the search terms with "AND" operators and wraps them in quotes.
        The query parameters are set up with the necessary fields, rows, and sort options.
        An API request is made to the ADS API with the constructed query and headers containing the authorization token.
        The response is processed and the relevant information is extracted to create a list of result dictionaries.
        Each result dictionary includes the paper's title, bibcode, first author, publication year,
        and a URL to the paper on the ADS website.
        The list of result dictionaries is returned as the search results.

        Examples
        --------
        >>> ads = ADSSearch()
        >>> results = ads.search(["SST", "CRISP", "25 May 2017"])
        (The `search` method is called on an instance of the `ADSSearch` class with the given search terms.)
        """

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
    """
    Convert a datetime object to a formatted string.

    Parameters
    ----------
    dt : datetime.datetime
        The datetime object to be converted to a string.

    Returns
    -------
    str
        The formatted string representation of the datetime object.

    Dependencies
    ------------
    None

    Notes
    -----
    Function Name: datetime_to_string
    This function takes a datetime object as input and converts it to a string representation.
    The datetime is formatted as "day Month year" where Month is the full month name.
    If the day is a single digit, the format is "d Month year" (e.g., "1 January 2022").
    If the day is two digits, the format is "dd Month year" (e.g., "25 May 2017").

    Examples
    --------
    >>> datetime_to_string(datetime(2022, 1, 1))
    "1 January 2022"

    >>> datetime_to_string(datetime(2017, 5, 25))
    "25 May 2017"
    """
    # convert datetime to string in the format 25 May 2017 if the date is two digits, otherwise 6 June 2019
    if dt.day < 10:
        return f"{dt.day} {dt.strftime('%B')} {dt.year}"
    else:
        return f"{dt.day} {dt.strftime('%B')} {dt.year}"


def get_search_terms(df, index):
    """
    Get search terms based on a dataframe index.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe containing the data.
    index : int
        The index of the dataframe to retrieve the search terms.

    Returns
    -------
    list
        A list of search terms based on the provided dataframe index.

    Dependencies
    ------------
    - datetime_to_string: Required to convert a datetime object to a formatted string.

    Notes
    -----
    Function Name: get_search_terms
    This function takes a pandas dataframe and an index as input.
    It reads the 'date_time' value from the specified index
    and converts it into a formatted string using the `datetime_to_string` function.
    The 'instruments' value from the specified index is also retrieved.
    The date string is then appended to the 'instruments' list,
    along with the term 'SST', to create the final list of search terms.
    The function returns the list of search terms.

    Examples
    --------
    >>> df = pd.DataFrame({'date_time': [datetime(2022, 1, 1)], 'instruments': ['CRISP']})
    >>> get_search_terms(df, 0)
    ['SST', 'CRISP', '1 January 2022']
    """

    # function that take dataframe index, reads the datetime, converts into string,
    # and appends in to the instruments list to search ADS
    date_string = datetime_to_string(df.at[index, 'date_time'])
    instruments = df.at[index, 'instruments']
    # append date string to instruments list
    search_terms = ['SST'] + instruments + [date_string]
    return search_terms


def get_ads_results(search_terms):
    """
    Get ADS results based on a list of search terms.

    Parameters
    ----------
    search_terms : list
        A list of search terms to query the ADS API.

    Returns
    -------
    list
        A list of dictionaries representing the ADS search results.
        Each dictionary contains the keys: 'title', 'bibcode', 'first_author', 'year', and 'url'.

    Dependencies
    ------------
    - ADSSearch: Required for performing the ADS API search.
      Make sure the ADSSearch class is properly defined and imported.

    Notes
    -----
    Function Name: get_ads_results
    This function takes a list of search terms as input and performs an ADS API search using the ADSSearch class.
    An instance of the ADSSearch class is created,
    and the `search` method of the instance is called with the provided search terms.
    The function returns a list of dictionaries representing the search results.
    Each dictionary includes information such as the paper's title, bibcode, first author, publication year,
    and a URL to the paper on the ADS website.

    Examples
    --------
    >>> search_terms = ['SST', 'CRISP', '1 January 2022']
    >>> get_ads_results(search_terms)
    (The `get_ads_results` function is called with the provided search terms,
    and the search results are returned as a list of dictionaries.)
    """

    # function that takes a list of search terms and returns the ADS results
    ads = ADSSearch()
    results = ads.search(search_terms)
    return results


class ADS_Search(ADSSearch):
    """
    Class for searching the ADS API based on data in a Pandas DataFrame.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        The dataframe containing the data to be used for searching the ADS API.

    Attributes
    ----------
    dataframe : pandas.DataFrame
        The dataframe containing the data.

    Methods
    -------
    get_results(index, pretty_print=False)
        Get the ADS search results based on the specified index from the dataframe.

    Dependencies
    ------------
    - pandas: Required for working with the dataframe.
    - get_search_terms: Required to retrieve search terms from the dataframe.
      Make sure the get_search_terms function is properly defined and imported.
    - get_ads_results: Required to retrieve ADS search results based on the search terms.
      Make sure the get_ads_results function is properly defined and imported.

    Notes
    -----
    Class Name: ADS_Search
    This class extends the ADSSearch class to provide search functionality based on data in a Pandas DataFrame.
    The `dataframe` attribute stores the dataframe passed to the class during initialization.
    The `get_results` method retrieves the search terms from the dataframe using the `get_search_terms` function.
    It then uses the `get_ads_results` function to obtain the ADS search results.
    If `pretty_print` is set to True, the results are displayed in a formatted HTML table.
    Otherwise, the results are printed in a text-based format.

    Examples
    --------
    >>> df = pd.DataFrame({'date_time': [datetime(2022, 1, 1)], 'instruments': ['CRISP']})
    >>> ads_search = ADS_Search(df)
    >>> ads_search.get_results(0)
    (The `get_results` method is called on an instance of the `ADS_Search` class
    with the specified index from the dataframe.)
    """

    def __init__(self, dataframe):
        """
        Initialize an instance of the ADS_Search class with a Pandas DataFrame.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            The dataframe containing the data to be used for searching the ADS API.

        Returns
        -------
        None

        Dependencies
        ------------
        - pandas: Required for working with the dataframe.

        Notes
        -----
        Function Name: __init__
        This special method is called when initializing an instance of the ADS_Search class.
        It takes a Pandas DataFrame as input and assigns it to the `dataframe` attribute of the instance.
        The `dataframe` attribute will be used for performing ADS searches based on the data in the dataframe.

        Examples
        --------
        >>> df = pd.DataFrame({'date_time': [datetime(2022, 1, 1)], 'instruments': ['CRISP']})
        >>> ads_search = ADS_Search(df)
        (An instance of the ADS_Search class is created, initialized with the provided dataframe.)
        """
        self.dataframe = dataframe

    def get_results(self, index, pretty_print=False):
        """
        Get the ADS search results based on the specified index from the dataframe.

        Parameters
        ----------
        index : int
            The index of the dataframe from which the search terms and results will be obtained.
        pretty_print : bool, optional
            Flag indicating whether to display the results in a formatted HTML table (default: False).

        Returns
        -------
        None

        Dependencies
        ------------
        - pandas: Required for working with the dataframe.
        - get_search_terms: Required to retrieve search terms from the dataframe.
        Make sure the get_search_terms function is properly defined and imported.
        - get_ads_results: Required to retrieve ADS search results based on the search terms.
        Make sure the get_ads_results function is properly defined and imported.
        - pd.DataFrame: Required for creating a DataFrame to format the search results.
        - display: Required to display the HTML table of results.
        - HTML: Required to format the HTML table of results.

        Notes
        -----
        Function Name: get_results
        This method retrieves the search terms from the dataframe using the `get_search_terms` function.
        It then calls the `get_ads_results` function to obtain the ADS search results based on the search terms.
        If `pretty_print` is set to True, the results are displayed in a formatted HTML table using pandas DataFrame
        and HTML modules.
        Otherwise, the results are printed in a text-based format.
        The text-based format includes the search terms and the details of each search result,
        such as the title, bibcode, first author, and URL.

        Examples
        --------
        >>> ads_search = ADS_Search(dataframe)
        >>> ads_search.get_results(0, pretty_print=True)
        (The `get_results` method is called on an instance of the `ADS_Search` class
        with the specified index from the dataframe, and the results are displayed in a formatted HTML table.)
        """
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
