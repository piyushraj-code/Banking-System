from config import database
import bcrypt
from utils import utils
from models import user
class Authentication():
    def __init__(self):
        self.db = database.DataBase()
        self.salt = bcrypt.gensalt()

    def register(self):
        (name, balance, password) = utils.get_details()
        hashed_password = bcrypt.hashpw(password.encode(), self.salt).decode()
        while True:
            account_number = utils.generate_account_number()
            query = "SELECT 1 FROM users WHERE account_number = %s"
            self.db.cunn.execute(query, (account_number,))
            if not self.db.cunn.fetchone():
                break
        try:
            query = "INSERT INTO users (name, account_number, balance, password) VALUES(%s, %s, %s, %s)"
            self.db.cunn.execute(query, (name, account_number, balance, hashed_password))
            self.db.commit()
            print("Registration Successful")
            print(f"You account_number is {account_number} Keep it safe")
        except Exception as e:
            print("Can't register Please Try again", e)
    def login(self):
        account_number = int(input("Enter your account number: "))
        password = input("Enter your password: ")
        try:
            query = "SELECT password FROM users WHERE account_number = %s"
            self.db.cunn.execute(query, (account_number, ))
            if bcrypt.checkpw(self.db.cunn.fetchone().encode(), password.encode()):
                print("Login SuccessfuL")
                return user.User()
        except Exception as e:
            pass  
        