from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

    def calculate_and_plot_win_loss_ratio(self, df):
        """
        Calculates the Win-Loss Ratio for each IPL team and plots a bar chart.

        This method first ensures that the 'Wins' (W) and 'Losses' (L) columns are of numeric type.
        It then calculates the Win-Loss Ratio for each team, and plots this ratio using a bar chart.
        """
        # Converting 'Wins' and 'Losses' columns to numeric values, handling non-numeric entries
        df['W'] = pd.to_numeric(df['W'], errors='coerce')
        df['L'] = pd.to_numeric(df['L'], errors='coerce')

        # Calculating the Win-Loss Ratio, adding a small constant to avoid division by zero
        df['Win_Loss_Ratio'] = df['W'] / (df['L'] + 0.0001)

        # Plotting the Win-Loss Ratio using seaborn's barplot
        plt.figure(figsize=(10, 6))
        sns.barplot(x='TEAM', y='Win_Loss_Ratio', data=df)
        plt.title('Win-Loss Ratio of IPL Teams')
        plt.xlabel('Team')
        plt.ylabel('Win-Loss Ratio')
        plt.xticks(rotation=45)
        plt.show()

    
    def plot_net_run_rate(self,df):
        """
        Plots the Net Run Rate (NRR) for each IPL team using a bar chart.

        This method assumes that the instance's DataFrame (self.df) contains a column 'NRR' with numeric values representing the Net Run Rate for each team. The bar chart displays each team's NRR on the y-axis and the team names on the x-axis.

        The method ensures that the 'NRR' column is treated as numeric and handles any non-numeric values by coercing them to NaN (Not a Number). The plot includes a title, labels for both axes, and the team names are rotated 45 degrees for better readability.

        Requirements:
            - The class must have an attribute 'df', which is a pandas DataFrame.
            - The DataFrame should have columns 'TEAM' and 'NRR'.

        Side Effects:
            - Modifies the 'NRR' column in 'df' to ensure it contains numeric values.
            - Displays a bar chart using matplotlib and seaborn.

        Returns:
            None
        """
        # Ensure 'NRR' column is numeric
        df['NRR'] = pd.to_numeric(df['NRR'], errors='coerce')

        # Plotting NRR
        plt.figure(figsize=(10, 6))
        sns.barplot(x='TEAM', y='NRR', data=df)
        plt.title('Net Run Rate of IPL Teams')
        plt.xlabel('Team')
        plt.ylabel('Net Run Rate')
        plt.xticks(rotation=45)
        plt.show()


    def plot_points_distribution(self, df):
        """
        Plots the Points Distribution for each IPL team using a bar chart.

        This method takes a DataFrame as an argument. It assumes the DataFrame
        contains a column 'PTS' with numeric values representing the points for
        each team. The bar chart displays each team's points on the y-axis and
        the team names on the x-axis.

        The method ensures that the 'PTS' column is treated as numeric and
        handles any non-numeric values by coercing them to NaN (Not a Number).
        The plot includes a title, labels for both axes, and the team names
        are rotated 45 degrees for better readability.

        Parameters:
            df (DataFrame): A pandas DataFrame containing IPL team data, 
                            specifically a 'TEAM' column for team names and a 
                            'PTS' column for points.

        Returns:
            None: The method displays a bar chart and returns nothing.
        """

        # Ensure 'PTS' column is numeric
        df['PTS'] = pd.to_numeric(df['PTS'], errors='coerce')

        # Plotting the Points Distribution
        plt.figure(figsize=(10, 6))
        sns.barplot(x='TEAM', y='PTS', data=df)
        plt.title('Points Distribution of IPL Teams')
        plt.xlabel('Team')
        plt.ylabel('Points')
        plt.xticks(rotation=45)
        plt.show()

