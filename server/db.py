import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Phu090204#my05',
        database='MilkTeaShopDB'
    )
    return connection

