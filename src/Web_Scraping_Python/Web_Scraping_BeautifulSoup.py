import requests
from bs4 import BeautifulSoup
import pandas as pd

class CovidDataScraper:
    """
    A class to scrape COVID-19 data from the Worldometer website.

    Attributes:
        url (str): URL of the Worldometer COVID-19 data page.
    """

    def __init__(self):
        """
        Initializes the CovidDataScraper with the Worldometer COVID-19 page URL.
        """
        self.url = "https://www.worldometers.info/coronavirus/"

    def fetch_data(self):
        """
        Makes an HTTP GET request to the Worldometer COVID-19 page and fetches the HTML content.

        Returns:
            str: The HTML content of the page.

        Raises:
            HTTPError: If an HTTP error occurs during the request.
        """
        response = requests.get(self.url)
        response.raise_for_status()  # Raises an exception for unsuccessful requests
        return response.text

    def parse_html(self, html_content):
        """
        Parses the HTML content to extract COVID-19 data and converts it to a DataFrame.

        Args:
            html_content (str): HTML content fetched from the Worldometer website.

        Returns:
            DataFrame: A pandas DataFrame containing COVID-19 data.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table', id='main_table_countries_today')

        # Extracting table headers
        headers = [th.text.strip() for th in table.find('thead').find_all('th')]

        # Extracting rows
        rows = []
        for row in table.find('tbody').find_all('tr'):
            cols = [ele.text.strip() for ele in row.find_all('td')]
            rows.append(cols)

        return pd.DataFrame(rows, columns=headers)

    def get_data(self):
        """
        Fetches and parses COVID-19 data from the Worldometer website.

        Returns:
            DataFrame: A pandas DataFrame containing the parsed COVID-19 data.
        """
        html_content = self.fetch_data()
        return self.parse_html(html_content)

