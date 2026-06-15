import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.getenv("DATABASE_URL")
db_password = os.getenv("DB_PASSWORD")
class DataBase():
    def __init__(self):
        try:
            self.db = mysql.connector.connect(
                host = database_url,
                port = 3306,
                user = "root",
                password = db_password,
                database="banking_system"
            )
            
            print("DataBase Connection Sucessful")
        except mysql.connector.Error as e:
            print("Database Conncetion error:", e)
            self.db = None
    def get_cursor(self):
        try:
            self.db.ping(reconnect=True, attempts=3, delay=2)
            return self.db.cursor()
        except Exception as e:
            print("Could not connect to database:", e)
            return None       
