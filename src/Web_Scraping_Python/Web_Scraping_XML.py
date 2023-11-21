import requests
import pandas as pd
import xml.etree.ElementTree as ET

class XMLDataFetcher:
    """
    A class for fetching and parsing XML data from a specified URL.

    Attributes:
        url (str): The URL from which to fetch the XML data.
    """

    def __init__(self, url):
        """
        Initialize the XMLDataFetcher instance with a URL.

        Args:
            url (str): The URL to fetch XML data from.
        """
        self.url = url

    def fetch_xml_data(self):
        """
        Fetches XML data from the specified URL.

        Returns:
            bytes: The content of the response in bytes, which is XML data.

        Raises:
            HTTPError: If the response status code is not successful.
        """
        response = requests.get(self.url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return response.content

    def parse_xml_to_dataframe(self, xml_data):
        """
        Parses XML data into a pandas DataFrame.

        Args:
            xml_data (bytes): XML data in bytes format.

        Returns:
            DataFrame: A pandas DataFrame constructed from the parsed XML data.
        """
        root = ET.fromstring(xml_data)

        # Extracting data and populating a list of dictionaries
        data = []
        for sitemap in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap'):
            loc = sitemap.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
            lastmod = sitemap.find('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod').text
            data.append({'loc': loc, 'lastmod': lastmod})

        # Converting the list of dictionaries into a pandas DataFrame
        return pd.DataFrame(data)

    def get_data(self):
        """
        Fetches and parses XML data from the URL and returns it as a pandas DataFrame.

        Returns:
            DataFrame: A pandas DataFrame containing the parsed XML data.
        """
        xml_data = self.fetch_xml_data()
        return self.parse_xml_to_dataframe(xml_data)


