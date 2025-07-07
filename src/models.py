from pydantic import BaseModel
from datetime import date
from typing import List, Optional

#request model
class FilterWeatherData(BaseModel):
    station_id: Optional[str] = None
    date: Optional[str] = None
    page: int = 1

class FilterWeatherStats(BaseModel):
    station_id: Optional[str] = None
    year: Optional[int] = None
    page: int = 1

#models to fetch data for both base weather and weather aggregation tables
class WeatherRecord(BaseModel):
    station_id: str
    date: date
    max_temp: Optional[int]
    min_temp: Optional[int]
    precipitation: Optional[int]


class WeatherStat(BaseModel):
    station_id: str
    year: int
    avg_max_temp_celsius: Optional[float]
    avg_min_temp_celsius: Optional[float]
    total_precipitation: Optional[float]

#response model
class Response(BaseModel):
    total_results: int
    total_pages : int
    current_page: int
    results_per_page: int
    results: List
    errorMessage : str