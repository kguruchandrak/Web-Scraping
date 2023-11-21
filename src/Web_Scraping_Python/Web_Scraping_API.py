import requests
import pandas as pd

def fetch_tv_season_data(title, season, api_key):
    """
    Fetches TV show season data from the OMDb API using the title and season number.

    This function sends a GET request to the OMDb API with parameters for a specific TV show's title and season number. The API key is also included in the request. The response is then processed to create a pandas DataFrame containing information about each episode in the specified season.

    Args:
        title (str): The title of the TV show (e.g., 'Game of Thrones').
        season (int): The season number of the TV show.
        api_key (str): The API key for accessing the OMDb API.

    Returns:
        pd.DataFrame: A DataFrame containing data for each episode in the specified season of the TV show.
                     If no data is found, an empty DataFrame is returned.
    """
    # Base URL for the OMDb API
    base_url = "http://www.omdbapi.com/"

    # Parameters for the API request
    params = {
        't': title,        # Title of the TV show
        'Season': season,  # Season number
        'apikey': api_key  # API key for OMDb
    }

    # Sending the GET request to the OMDb API
    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Raises an exception for unsuccessful requests

    # Parsing the JSON response
    season_data = response.json()

    # Normalizing the episode data into a pandas DataFrame
    if 'Episodes' in season_data:
        episodes_df = pd.json_normalize(season_data, 'Episodes')
        return episodes_df
    else:
        # Return an empty DataFrame if no episodes data is present
        return pd.DataFrame()

