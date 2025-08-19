import os
from dotenv import load_dotenv
import requests
from pydantic import BaseModel, field_validator
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv('API_KEY')

# URL for Tomorrow.io Realtime Weather API
url = f"https://api.tomorrow.io/v4/weather/realtime?location=93312%20US&units=imperial&apikey={api_key}"

headers = {
    "accept": "application/json",
    "accept-encoding": "deflate, gzip, br"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print('Successfully retrieved weather data.')
else:
    print(f"Error: {response.status_code} - {response.text}")


# Define Pydantic models for validation
class Values(BaseModel):
    temperature: float
    uvIndex: int
    humidity: float

    @field_validator('temperature')
    def temp_range(cls, v):
        if not -50 <= v <= 125:  # Realistic temp range
            raise ValueError("Temperature out of bounds")
        return v
    
    @field_validator('humidity')
    def humidity_range(cls, v):
        if not 0 <= v <= 100:  # Percentage 0-100
            raise ValueError("Humidity out of bounds")
        return v
    
    @field_validator('uvIndex')
    def uv_index_range(cls, v):
        if not 0 <= v <= 11:  # UV index typically ranges from 0 to 11+
            raise ValueError("UV Index out of bounds")
        return v
    
class Location(BaseModel):
    name: str
    lat: float
    lon: float
    
class Data(BaseModel):
    time: datetime
    values: Values

class Weather(BaseModel):
    data: Data
    location: Location


# Parse and validate API data
weather_data = Weather(**response.json())
print(weather_data)