# Author: Yasin Holzenkämpfer
# Last Modified: 23-12-2025
#
# Description: This module provides weather services for the application.

import requests

class WeatherService:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_current_weather(self, city: str) -> dict:
        """
        Fetch the current weather for a given city.
        Args:
            city (str): The name of the city to fetch weather for.
        Returns:
            dict: A dictionary containing weather data.
        """

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"

        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def extract_data(self, weather_data: dict, keys: list) -> dict:
        """
        Extract specific data points from the weather data.
        Args:
            weather_data (dict): The full weather data dictionary.
            keys (list): List of keys to extract from the weather data.
        Returns:
            dict: A dictionary containing the extracted data points.
        """

        extracted_data = {}
        for key in keys:
            if key in weather_data:
                extracted_data[key] = weather_data[key]
        return extracted_data
