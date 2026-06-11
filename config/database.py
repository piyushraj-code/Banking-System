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
            self.cunn = self.db.cursor()
            print("DataBase Connection Sucessful")
        except mysql.connector.Error as e:
            print("Database Conncetion error:", e)
            self.db = None
            self.cunn = None
