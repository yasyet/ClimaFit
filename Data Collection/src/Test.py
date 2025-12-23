# Test.py
# Author: Yasin Holzenkämpfer
# Last Modified: 15.12.2025
#
# Description: This module tests the modules.

import os
import dotenv


from WeatherService import WeatherService
from DataService import DataService

def main():
    # Load environment variables
    dotenv.load_dotenv()
    weather_api_key = os.getenv("openweathermap_api_key", "")

    # Test WeatherService
    weather_service = WeatherService(api_key=weather_api_key)
    weather_data = weather_service.get_current_weather("Delmenhorst")
    extracted_data = weather_service.extract_data(weather_data, ["main"])
    print("Extracted Weather Data:", extracted_data)

if __name__ == "__main__":
    main()