import psycopg2
from psycopg2.extras import execute_values
import logging

logging.basicConfig(level=logging.INFO)

# ---db configurations---
DB_PARAMS = {
    'dbname': 'weatherdata',
    'user': 'postgres',
    'password': '12345678',
    'host': 'localhost',
    'port': 5432
}

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS weather_aggregate (                   
                station_id TEXT NOT NULL,
                year INTEGER NOT NULL,
                avg_max_temp_celsius FLOAT,
                avg_min_temp_celsius FLOAT,
                total_precipitation FLOAT,
                PRIMARY KEY (station_id, year)
            );
        """)
        conn.commit()

def connection(DB_PARAMS):
    return psycopg2.connect(**DB_PARAMS)

def count_records(conn):
    count = """
        SELECT COUNT(*) from weather_aggregate;
    """
    with conn.cursor() as cur:
        cur.execute(count)
        total = cur.fetchone()[0]
    
    return total

def aggregate_data(conn):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO weather_aggregate(
                station_id, year, avg_max_temp_celsius, avg_min_temp_celsius, total_precipitation
            )
            Select station_id, Extract(Year from date) as year, 
                    ROUND(avg(max_temp)/10.0, 3) as avg_max_temp_celsius,
                    ROUND(avg(min_temp)/10.0, 3) as avg_min_temp_celsius,
                    sum(precipitation)/100.0 as total_precipitation
            From weather
            Where max_temp != -9999 And min_temp != -9999 AND precipitation != -9999
            Group By Extract(Year from date), station_id
            Order By station_id, year;
        """)
        conn.commit()

def main():
    try:
        #create connection
        conn = connection(DB_PARAMS)
        logging.info("Connection to DB Successfull")

        #create table if not exists
        create_table(conn)

        #execute data analysis query for weather summary
        aggregate_data(conn)

        #get record count
        count = count_records(conn)

        logging.info(f"Count of aggregated records : {count}")
        
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()