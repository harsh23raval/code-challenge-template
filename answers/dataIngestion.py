import psycopg2
import os
from datetime import datetime
import pandas as pd
from psycopg2.extras import execute_values
import shutil
from datetime import datetime
import logging

# ---- DB Config ----
DB_PARAMS = {
    'dbname': 'weatherdata',
    'user': 'postgres',
    'password': '12345678',
    'host': 'localhost',
    'port': 5432
}

#weather data directory
wx_data = '../wx_data'

#archive
archive_dir = "../archive"

#function to create a dataframe from a given file
def extract_data(fileName, filePath):
    
    rows = []
    count_row_not_processed = 0

    station_id = fileName.replace(".txt", "")
    file_path = os.path.join(filePath, fileName)
    with open(file_path, "r") as file:
        for line in file:
            row = line.strip().split("\t")

            #only valid data proceeds further
            if len(row) != 4:
                count_row_not_processed += 1
                continue

            try:
                date = datetime.strptime(row[0], "%Y%m%d").date()
                max_temp = row[1]
                min_temp = row[2]
                precipitation = row[3]
                rows.append((station_id, date, max_temp.strip(), min_temp.strip(), precipitation.strip()))
            except Exception as e:
                count_row_not_processed += 1
                print(f"failed to process row : {line.strip()} in file {file_path} - {e}")

    return rows, count_row_not_processed

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS weather (
                station_id TEXT NOT NULL,
                date DATE NOT NULL,
                max_temp INTEGER,
                min_temp INTEGER,
                precipitation INTEGER,
                PRIMARY KEY (station_id, date)
            );
        """)
        conn.commit()

def bulk_insert(conn, rows):

    before_inserting = count_records(conn)

    insert = """
        INSERT INTO weather (station_id, date, max_temp, min_temp, precipitation)
        VALUES %s;
    """
    with conn.cursor() as cur:
        execute_values(cur, insert, rows)
        conn.commit()
    
    after_inserting = count_records(conn)

    return after_inserting - before_inserting

def count_records(conn):
    count = """
        SELECT COUNT(*) from weather;
    """
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM weather")
        total = cur.fetchone()[0]
    
    return total

#archive file
def archive_file(fileName, source_dir, archive_dir):
    # Create archive folder if it doesn't exist
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)  

    file_path = os.path.join(source_dir, fileName)
    archive_path = os.path.join(archive_dir, fileName)

    shutil.move(file_path, archive_path)
    print(f"{fileName} moved file to archive directory")


def connection(DB_PARAMS):
    return psycopg2.connect(**DB_PARAMS)


def main():
    try:
        #process start
        start_time = datetime.now()
        print(f"Start Time : {start_time}")

        #create connection
        conn = connection(DB_PARAMS)
        print("Connection to DB Successfull")

        #create table if not exists
        create_table(conn)

        total_rows = 0

        #read through files
        for file in os.listdir(wx_data):

            if not file.endswith(".txt"):
                continue
            
            #extract and transform data
            try:
                rows, count_of_bad_records = extract_data(file, wx_data)
                print(f"File {file} having rows {len(rows)} being processed..")
                if(count_of_bad_records > 0):
                    print(f"File {file} had {count_of_bad_records} bad records, successfully ignored")

                total_rows += len(rows)

                insertion_count = bulk_insert(conn, rows)
                print(f"{insertion_count} rows inserted from file {file}")

                archive_file(file, wx_data, archive_dir)
                
            except Exception as e:
                print(f"Exception occured while processing file {file} : ", e)

        #process end
        end_time = datetime.now()
        print(f"End Time : {end_time}")

        print(f"[INFO] Processing started at {start_time} and finished at {end_time}, (Duration: {end_time - start_time})")
        
        db_count = count_records(conn)

        print(f"Total number of records ingested : {total_rows}")
        print(f"Total number of records in db : {db_count}")

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()