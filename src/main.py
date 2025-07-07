from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from db import weather_db_connection
from models import FilterWeatherData, FilterWeatherStats, WeatherRecord, WeatherStat, Response

app = FastAPI(title="Weather API")

default_page_size = 25
    
#get weather data with optional filtering
@app.post("/api/weather", response_model=Response)
def get_weather(body: FilterWeatherData):
    limit = default_page_size
    offset = (body.page - 1) * limit

    conn = weather_db_connection()
    cur = conn.cursor()

    count_sql = "SELECT COUNT(*) FROM weather WHERE TRUE"
    data_sql = """
        SELECT station_id, date, max_temp, min_temp, precipitation
        FROM weather WHERE TRUE
    """

    filters = []
    params = []

    if body.station_id:
        filters.append("station_id = %s")
        params.append(body.station_id)
    if body.date:
        filters.append("date = %s")
        params.append(body.date)

    if filters:
        clause = " AND ".join(filters)
        count_sql += f" AND {clause}"
        data_sql += f" AND {clause}"

    count_params = list(params)
    data_sql += " ORDER BY station_id, date LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    cur.execute(count_sql, count_params)
    total = cur.fetchone()[0]

    total_pages = (total + limit - 1) // limit

    cur.execute(data_sql, params)
    rows = cur.fetchall()
    conn.close()

    results = [
        WeatherRecord(
            station_id=r[0],
            date=r[1],
            max_temp=r[2],
            min_temp=r[3],
            precipitation=r[4]
        ) for r in rows
    ]

    return {
        "total_results": total,
        "total_pages" : total_pages,
        "current_page": body.page,
        "results_per_page": limit,
        "results": results
    }


#getting the weather statistics with optional filtering
@app.post("/api/weather/stats", response_model=Response)
def get_weather_stats(body: FilterWeatherStats):
    limit = default_page_size
    offset = (body.page - 1) * limit

    conn = weather_db_connection()
    cur = conn.cursor()

    count_sql = "SELECT COUNT(*) FROM weather_aggregate WHERE TRUE"
    data_sql = """
        SELECT station_id, year, avg_max_temp_celsius,
               avg_min_temp_celsius, total_precipitation
        FROM weather_aggregate WHERE TRUE
    """

    filters = []
    params = []

    if body.station_id:
        filters.append("station_id = %s")
        params.append(body.station_id)
    if body.year:
        filters.append("year = %s")
        params.append(body.year)

    if filters:
        clause = " AND ".join(filters)
        count_sql += f" AND {clause}"
        data_sql += f" AND {clause}"

    count_params = list(params)
    data_sql += " ORDER BY station_id, year LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    cur.execute(count_sql, count_params)
    total = cur.fetchone()[0]

    total_pages = (total + limit - 1) // limit

    cur.execute(data_sql, params)
    rows = cur.fetchall()
    conn.close()

    results = [
        WeatherStat(
            station_id=r[0],
            year=r[1],
            avg_max_temp_celsius=r[2],
            avg_min_temp_celsius=r[3],
            total_precipitation=r[4]
        ) for r in rows
    ]

    return {
        "total_results": total,
        "total_pages" : total_pages,
        "current_page": body.page,
        "results_per_page": limit,
        "results": results
    }
