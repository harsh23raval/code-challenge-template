import psycopg2

#setup db configurations
dbname = "weatherdata"
user = "postgres"
password = "12345678"
host = "localhost"
port = "5432"

#return connection
def weather_db_connection():
    return psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )