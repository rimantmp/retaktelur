import mysql.connector

def get_database_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="liani_coba"
    )
    return conn
