from dotenv import load_dotenv
from pprint import pprint
import requests
import os
import json
from datetime import datetime

load_dotenv()

def get_current_weather(city="Kansas City", country_code=None, units="metric"):
    """
    Get current weather for a city with optional country code and units
    
    Args:
        city (str): City name
        country_code (str): ISO 3166 country code (e.g., 'FR', 'US')
        units (str): 'metric', 'imperial', or 'kelvin'
    """
    # Build query string
    query = city
    if country_code:
        query = f"{city},{country_code}"
    
    request_url = f'https://api.openweathermap.org/data/2.5/weather?appid={os.getenv("API_KEY")}&q={query}&units={units}'
    
    try:
        weather_data = requests.get(request_url).json()
        return weather_data
    except requests.RequestException as e:
        return {"cod": 500, "message": f"Request failed: {str(e)}"}

def get_weather_by_coordinates(lat, lon, units="metric"):
    """
    Get current weather by GPS coordinates
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        units (str): 'metric', 'imperial', or 'kelvin'
    """
    request_url = f'https://api.openweathermap.org/data/2.5/weather?appid={os.getenv("API_KEY")}&lat={lat}&lon={lon}&units={units}'
    
    try:
        weather_data = requests.get(request_url).json()
        return weather_data
    except requests.RequestException as e:
        return {"cod": 500, "message": f"Request failed: {str(e)}"}

def get_weather_forecast(city, country_code=None, units="metric", days=5):
    """
    Get weather forecast for multiple days
    
    Args:
        city (str): City name
        country_code (str): ISO 3166 country code
        units (str): 'metric', 'imperial', or 'kelvin'
        days (int): Number of days (max 5 for free API)
    """
    query = city
    if country_code:
        query = f"{city},{country_code}"
    
    request_url = f'https://api.openweathermap.org/data/2.5/forecast?appid={os.getenv("API_KEY")}&q={query}&units={units}&cnt={days * 8}'
    
    try:
        forecast_data = requests.get(request_url).json()
        return forecast_data
    except requests.RequestException as e:
        return {"cod": 500, "message": f"Request failed: {str(e)}"}

def search_cities(query, limit=5):
    """
    Search for cities using OpenWeatherMap Geocoding API
    
    Args:
        query (str): City name to search
        limit (int): Maximum number of results
    """
    request_url = f'http://api.openweathermap.org/geo/1.0/direct?q={query}&limit={limit}&appid={os.getenv("API_KEY")}'
    
    try:
        cities_data = requests.get(request_url).json()
        return cities_data
    except requests.RequestException as e:
        return []

def get_air_quality(lat, lon):
    """
    Get air quality data for coordinates
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
    """
    request_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={os.getenv("API_KEY")}'
    
    try:
        air_quality_data = requests.get(request_url).json()
        return air_quality_data
    except requests.RequestException as e:
        return {"cod": 500, "message": f"Request failed: {str(e)}"}

def convert_temperature(temp, from_unit, to_unit):
    """
    Convert temperature between different units
    
    Args:
        temp (float): Temperature value
        from_unit (str): 'celsius', 'fahrenheit', 'kelvin'
        to_unit (str): 'celsius', 'fahrenheit', 'kelvin'
    """
    # Convert to Celsius first
    if from_unit == 'fahrenheit':
        celsius = (temp - 32) * 5/9
    elif from_unit == 'kelvin':
        celsius = temp - 273.15
    else:
        celsius = temp
    
    # Convert from Celsius to target unit
    if to_unit == 'fahrenheit':
        return celsius * 9/5 + 32
    elif to_unit == 'kelvin':
        return celsius + 273.15
    else:
        return celsius

# Country codes mapping for popular countries
COUNTRY_CODES = {
    'France': 'FR',
    'United States': 'US',
    'United Kingdom': 'GB',
    'Germany': 'DE',
    'Spain': 'ES',
    'Italy': 'IT',
    'Canada': 'CA',
    'Australia': 'AU',
    'Japan': 'JP',
    'China': 'CN',
    'Brazil': 'BR',
    'India': 'IN',
    'Russia': 'RU',
    'Mexico': 'MX',
    'Netherlands': 'NL',
    'Belgium': 'BE',
    'Switzerland': 'CH',
    'Austria': 'AT',
    'Sweden': 'SE',
    'Norway': 'NO',
    'Denmark': 'DK',
    'Finland': 'FI',
    'Poland': 'PL',
    'Portugal': 'PT',
    'Greece': 'GR',
    'Turkey': 'TR',
    'South Korea': 'KR',
    'Argentina': 'AR',
    'Chile': 'CL',
    'Colombia': 'CO',
    'Peru': 'PE',
    'Venezuela': 'VE',
    'Egypt': 'EG',
    'South Africa': 'ZA',
    'Morocco': 'MA',
    'Algeria': 'DZ',
    'Tunisia': 'TN',
    'Israel': 'IL',
    'Saudi Arabia': 'SA',
    'UAE': 'AE',
    'Thailand': 'TH',
    'Vietnam': 'VN',
    'Malaysia': 'MY',
    'Singapore': 'SG',
    'Indonesia': 'ID',
    'Philippines': 'PH',
    'New Zealand': 'NZ'
}

if __name__ == "__main__":
    print('\n*** Get Current Weather Conditions ***\n')

    city = input("\nPlease enter a city name: ")

    # Check for empty strings or string with only spaces
    if not bool(city.strip()):
        city = "Kansas City"

    weather_data = get_current_weather(city)

    print("\n")
    pprint(weather_data)