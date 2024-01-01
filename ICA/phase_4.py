import requests
import pandas as pd

def fetch_weather_data(api_url):
    try:
        # Make a GET request to the Open-Meteo API
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON data from the response
            data = response.json()

            # Convert the data to a DataFrame
            df = pd.DataFrame(data)

            # Do something with the DataFrame (print it in this example)
            print(df)
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code}")
    except Exception as e:
        # Print an error message if an exception occurs
        print(f"An error occurred: {e}")

# Example API URL with parameters
api_url = "https://archive-api.open-meteo.com/v1/archive?latitude=52.52&longitude=13.41&start_date=2023-01-01&end_date=2023-12-01&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum&timeformat=unixtime&timezone=Europe%2FBerlin"

# Call the function with the API URL
fetch_weather_data(api_url)
