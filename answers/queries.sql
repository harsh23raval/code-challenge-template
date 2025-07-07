--The below queries are used within the project.

--Query to create data model for weather table
CREATE TABLE IF NOT EXISTS weather (
                station_id TEXT NOT NULL,
                date DATE NOT NULL,
                max_temp INTEGER,
                min_temp INTEGER,
                precipitation INTEGER,
                PRIMARY KEY (station_id, date)
            );


--Query to insert into rows into weather table
INSERT INTO weather (station_id, date, max_temp, min_temp, precipitation)
VALUES %s;
--Note : My code design loads(inserts) all valid rows of each file from wx_data directory at once into the weather table.


--Query to create data model for weather aggregation table
CREATE TABLE IF NOT EXISTS weather_aggregate (                   
                station_id TEXT NOT NULL,
                year INTEGER NOT NULL,
                avg_max_temp_celsius FLOAT,
                avg_min_temp_celsius FLOAT,
                total_precipitation FLOAT,
                PRIMARY KEY (station_id, year)
            );

--Query to insert rows into weather_aggregate table by aggregating data from weather table
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
