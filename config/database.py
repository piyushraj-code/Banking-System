import mysql.connector
class DataBase():
    def __init__(self):
        try:
            self.db = mysql.connector.connect(
                host = "127.0.0.1",
                port = 3306,
                user = "root",
                password = "1908",
                database="banking_system"
            )
            self.cunn = self.db.cursor()
            print("DataBase Connection Sucessful")
        except mysql.connector.Error as e:
            print("Database Conncetion error:", e)
            self.db = None
            self.cunn = None
