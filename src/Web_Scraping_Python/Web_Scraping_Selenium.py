from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

class IPLPointsTableScraper:
    """
    A class to scrape the IPL 2023 points table data using Selenium and BeautifulSoup.

    Attributes:
        url (str): URL of the IPL 2023 points table webpage.
        dataframe (DataFrame, optional): DataFrame to store the scraped data. Initially None.
    """

    def __init__(self):
        """
        Initializes the IPLPointsTableScraper with the URL of the IPL points table.
        """
        self.url = "https://www.iplt20.com/points-table/men/2023"
        self.dataframe = None

    def fetch_data(self):
        """
        Uses Selenium WebDriver to fetch the dynamically loaded content of the IPL points table page.

        Returns:
            str: HTML content of the page.
        """
        # Setting up Selenium WebDriver
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Runs Chrome in headless mode
        driver = webdriver.Chrome(service=service, options=options)

        # Fetching the page content
        driver.get(self.url)
        time.sleep(5)  # Waits for the page to load completely
        html_content = driver.page_source
        driver.quit()
        return html_content

    def parse_html(self, html_content):
        """
        Parses the HTML content using BeautifulSoup to extract the points table data.

        Args:
            html_content (str): HTML content of the IPL points table page.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table')  # Finds the table in the HTML
        if not table:
            raise ValueError("No table found on the page")

        # Extracting table headers and rows
        headers = [th.text.strip() for th in table.find('tr').find_all('th')]
        rows = [[ele.text.strip() for ele in row.find_all('td')] for row in table.find_all('tr')[1:]]

        self.dataframe = pd.DataFrame(rows, columns=headers)

    def get_data(self):
        """
        Fetches and parses the IPL points table data, and returns it as a pandas DataFrame.

        Returns:
            DataFrame: A DataFrame containing the parsed points table data.
        """
        html_content = self.fetch_data()
        self.parse_html(html_content)
        return self.dataframe

