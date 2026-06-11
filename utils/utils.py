import random
from config import database
db = database.DataBase()
def generate_account_number():
    return random.randint(10000, 99999)

def get_details():
    name = input("Enter your name: ")
    balance = float(input("Enter initial deposit: "))
    password = input("Enter password: ")
    return name, balance, password

