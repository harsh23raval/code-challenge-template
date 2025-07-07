import psycopg2

dbname = "weatherdata"
user = "postgres"
password = "12345678"
host = "localhost"
port = "5432"

RESULTS_PER_PAGE = 25

def weather_db_connection():
    return psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )