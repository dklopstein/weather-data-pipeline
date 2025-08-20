from pydantic import field_validator
from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional

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
