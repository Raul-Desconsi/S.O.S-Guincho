import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", #SUA SENHA 
        database="guincho_db_def",
        port="3306"
    )


