from config import database
import bcrypt
from utils import utils
from models import user
from flask import jsonify, session
class Authentication():
    def __init__(self, db):
        self.db = db

    def register(self, name, balance, password):
        #(name, balance, password) = utils.get_details()
        cursor = self.db.db.cursor()
        if not name or not password or not balance:
            return {
                "sauccess": False,
                "message": "Name, balance, password is required"
            }
        if len(password) < 8:
            return {
                "success": False,
                "message": "Password must be at least 8 character long"
            } 
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode("utf-8")
        while True:
            account_number = utils.generate_account_number()
            query = "SELECT 1 FROM users WHERE account_number = %s"
            cursor.execute(query, (account_number,))
            if not cursor.fetchone():
                break
        try:
            query = "INSERT INTO users (name, account_number, balance, password) VALUES(%s, %s, %s, %s)"
            cursor.execute(query, (name, account_number, balance, hashed_password))
            self.db.db.commit()
            return {
                "success": True,
                "message": f"Registration Successful your account number is: {account_number}"
            }
            # print("Registration Successful")
            # print(f"You account_number is {account_number} Keep it safe")
        except Exception as e:
            self.db.db.rollback()
            # print("Can't register Please Try again", e)
            return {
                "success": False,
                "message": "Registration Failed"
            }
        finally:
            cursor.close()
    def login(self, account_number, password):
        # account_number = int(input("Enter your account number: "))
        # password = input("Enter your password: ")
        cursor = self.db.db.cursor()
        try:
            query = "SELECT password FROM users WHERE account_number = %s"
            cursor.execute(query, (account_number, ))
            result = cursor.fetchone()
            if result is None:
                return {
                    "success": False,
                    "message": "Account not found!"
                }
            
            elif bcrypt.checkpw(password.encode("utf-8"), result[0].encode("utf-8")):
                # print("Login SuccessfuL")
                query = "SELECT name FROM users WHERE account_number = %s"
                cursor.execute(query, (account_number,))
                name = cursor.fetchone()
                session["account_number"] = account_number
                session["name"] = name[0]
                return {
                    "success": True,
                    "message": "Login Successful"
                }
            else:
                # print("Invaid account number or password")
                return {
                    "success": False,
                    "message": "Invaid account number or password"
                }
        except Exception as e:
            # print("Can't login Please try again: ", e)
            return {
                "success": False,
                "message": f"Can't login Please try again: {e}"
            }
        finally:
            cursor.close()
        