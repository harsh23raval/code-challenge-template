from fastapi import FastAPI
from db import weather_db_connection
from models import FilterWeatherData, FilterWeatherStats, WeatherRecord, WeatherStat, Response

app = FastAPI(title="Weather API")

default_page_size = 25
    
#weather data endpoint with optional station_id and date filtering, returns paginated JSON response
@app.post("/api/weather", response_model=Response)
def get_weather(body: FilterWeatherData):
    try:
        limit = default_page_size
        offset = (body.page - 1) * limit

        #make connection
        conn = weather_db_connection()
        cur = conn.cursor()

        #default query to get total records count from weather database without any filters
        count_sql = "SELECT COUNT(*) FROM weather WHERE TRUE"

        #default query to get weather data without any filters
        data_sql = """
            SELECT station_id, date, max_temp, min_temp, precipitation
            FROM weather WHERE TRUE
        """

        filters = []
        params = []

        #checks if user has applied station_id filter
        if body.station_id:
            filters.append("station_id = %s")
            params.append(body.station_id)
        #checks if user has applied the date filter
        if body.date:
            filters.append("date = %s")
            params.append(body.date)

        #append filters to queries
        if filters:
            clause = " AND ".join(filters)
            count_sql += f" AND {clause}"
            data_sql += f" AND {clause}"

        count_params = list(params)
        data_sql += " ORDER BY station_id, date LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        #execute query for count
        cur.execute(count_sql, count_params)
        total = cur.fetchone()[0]

        total_pages = (total + limit - 1) // limit

        #execute query for rows
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
            "results": results,
            "errorMessage" : "None"
        }
    except Exception as e:
        return{
            "total_results": 0,
            "total_pages" : 0,
            "current_page": body.page,
            "results_per_page": 0,
            "results": [],
            "errorMessage" : str(e)
        }


#weather statistics endpoint with optional station_id and year filtering, returns paginated JSON response
@app.post("/api/weather/stats", response_model=Response)
def get_weather_stats(body: FilterWeatherStats):
    try:
        #validating input
        if(body.year < 1900):
            raise Exception("Year cannot be less than 1900")

        limit = default_page_size
        offset = (body.page - 1) * limit

        #make connection
        conn = weather_db_connection()
        cur = conn.cursor()

        #default query to get total records count from weather aggregate DB without any filters
        count_sql = "SELECT COUNT(*) FROM weather_aggregate WHERE TRUE"

        #default query to get weather aggregate DB without any filters
        data_sql = """
            SELECT station_id, year, avg_max_temp_celsius,
                avg_min_temp_celsius, total_precipitation
            FROM weather_aggregate WHERE TRUE
        """

        filters = []
        params = []

        #checks if user has applied station_id filter
        if body.station_id:
            filters.append("station_id = %s")
            params.append(body.station_id)

        #checks if user has applied year filter
        if body.year:
            filters.append("year = %s")
            params.append(body.year)

        #append filters to queries
        if filters:
            clause = " AND ".join(filters)
            count_sql += f" AND {clause}"
            data_sql += f" AND {clause}"

        count_params = list(params)
        data_sql += " ORDER BY station_id, year LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        #execute query for count
        cur.execute(count_sql, count_params)
        total = cur.fetchone()[0]

        total_pages = (total + limit - 1) // limit

        #execute query for rows
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
            "results": results,
            "errorMessage" : "None"
        }
    except Exception as e:
        return{
            "total_results": 0,
            "total_pages" : 0,
            "current_page": body.page,
            "results_per_page": 0,
            "results": [],
            "errorMessage" : str(e)
        }
