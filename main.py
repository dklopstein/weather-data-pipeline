import os
from dotenv import load_dotenv
import asyncio
import aiohttp
from pydantic import field_validator
from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional

# Create table models for the data received from the API
# Flatten the JSON response for easier handling
def json_to_weather_db(json_data):
    """Convert Weather JSON data to WeatherDB"""

    return WeatherDB(
        time=datetime.fromisoformat(json_data['data']['time'].replace("Z", "+00:00")),
        location_name=json_data['location']['name'],
        lat=json_data['location']['lat'],
        lon=json_data['location']['lon'],
        humidity=json_data['data']['values']['humidity'],
        temperature=json_data['data']['values']['temperature'],
        uv_index=json_data['data']['values']['uvIndex']
    )


# Define Pydantic/SQLModel table model for validation and SQLite
class WeatherDB(SQLModel, table=True):
    # Use auto-increment ID as primary key for SQL efficiency
    id: Optional[int] = Field(default=None, primary_key=True)

    # Time field
    time: datetime
    
    # Location fields
    location_name: str
    lat: float
    lon: float
    
    # Weather values fields
    humidity: Optional[int] = None
    temperature: Optional[float] = None
    uv_index: Optional[int] = None
    
    # Validators for critical fields
    @field_validator('temperature')
    def temp_range(cls, v):
        if v is not None and not -50 <= v <= 125:
            raise ValueError('Temperature out of bounds')
        return v
    
    @field_validator('humidity')
    def humidity_range(cls, v):
        if v is not None and not 0 <= v <= 100:
            raise ValueError('Humidity out of bounds')
        return v
    
    @field_validator('uv_index')
    def uv_index_range(cls, v):
        if v is not None and not 0 <= v <= 11:
            raise ValueError('UV Index out of bounds')
        return v

# Create SQLite engine
engine = create_engine('sqlite:///weather.db')

# Create table in SQLite if it doesn't exist
SQLModel.metadata.create_all(engine)


# Handle concurrent API calls
# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv('API_KEY')

# URLs for Tomorrow.io Realtime Weather API
locations = [
    '93312%20US', # Bakersfield, CA, USA
    '93106%20US', # UCSB
    '92093%20US'  # UCSD
    ]

urls = [f'https://api.tomorrow.io/v4/weather/realtime?location={location}&units=imperial&apikey={api_key}' for location in locations]

# Run API requests concurrently
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results
    
async def main():
    # Fetch concurrently
    json_data = await fetch_all(urls)

    # Convert JSON to WeatherDB models
    weather_entries = [json_to_weather_db(data) for data in json_data]

    # Insert into SQLite
    with Session(engine) as session:
        session.add_all(weather_entries)
        session.commit()

if __name__ == "__main__":
    results = asyncio.run(main())
