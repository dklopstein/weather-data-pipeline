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
    print(response.text)
else:
    print(f"Error: {response.status_code} - {response.text}")



