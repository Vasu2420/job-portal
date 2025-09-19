import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="vasu",
    password="root",
    database="job_portal"
)

print(conn.is_connected())
