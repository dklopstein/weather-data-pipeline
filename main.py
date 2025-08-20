import os
from dotenv import load_dotenv
import asyncio
import aiohttp
from sqlmodel import SQLModel, create_engine, Session
from models import WeatherDB, json_to_weather_db

# Handle concurrent API calls
# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv('API_KEY')

# Create SQLite engine
engine = create_engine('sqlite:///weather.db')

# Create table in SQLite if it doesn't exist
SQLModel.metadata.create_all(engine)

# URLs for Tomorrow.io Realtime Weather API
locations = [
    '93312%20US', # Bakersfield, CA, USA
    '93106%20US', # UCSB
    '92093%20US'  # UCSD
    ]

urls = [f'https://api.tomorrow.io/v4/weather/realtime?location={location}&units=imperial&apikey={api_key}' for location in locations]

# Async API fetch
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
