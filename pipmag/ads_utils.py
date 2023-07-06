import requests
import os
import pandas as pd
from IPython.display import display, HTML


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
