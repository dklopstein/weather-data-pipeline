# Weather Data Pipeline

A Python project to fetch, validate, and store weather data from multiple APIs into a SQLite database using SQLModel and Pydantic for data validation.

---

## Features

- **Concurrent API Requests**: Uses `asyncio` + `aiohttp` for fast, parallel fetching of weather data.
- **Data Validation**: Utilizes Pydantic validators within `SQLModel` to ensure temperature, humidity, UV index, and datetime fields are valid.
- **SQLite Storage**: Stores structured weather data in a local SQLite database (`weather.db`).
- **Automatic Parsing**: Handles ISO datetime strings and converts them into Python `datetime` objects automatically.

---

## Installation

```bash
# Clone the repo
git clone https://github.com/dklopstein/weather-data-pipeline.git
cd weather-data-pipeline

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage
Replace `api_key` with your Tomorrow.io Weather API key. Then run the main pipeline script to fetch weather data and store in SQLite:
```
python main.py
```
The pipeline will:
1. Fetch data concurrently from all URLs listed in urls.
2. Validate and parse each JSON response using `WeatherDB`.
3. Insert the entries into `weather.db`.

## Project Structure
```
weather-data-pipeline/
├── main.py            # Main pipeline script
├── models.py          # SQLModel definitions and Pydantic validators
├── requirements.txt   # Python dependencies
├── README.md
└── .gitignore         # Ignore weather.db and .env
```

## Notes
- Database: weather.db is ignored in Git (.gitignore) as it can be regenerated using this pipeline.
- Extending APIs: Add additional API URLs to the urls list in `main.py` but ensure you're within [call limits](https://support.tomorrow.io/hc/en-us/articles/20273728362644-Free-API-Plan-Rate-Limits).
- Validation: All critical fields (temperature, humidity, UV index) are validated and will raise errors if out of bounds.