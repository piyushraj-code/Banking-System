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
def interface():
    print("Welcome to MyBank")
    print("-------------------------------------------------------")
    print("-------------------------------------------------------")
    print("Enter 1 to register new user: ")
    print("Enter 2 to login to an existing user: ")
    print("Enter 3 to exit: ")

def user_interface(user):
    print("-------------------------------------------------------")
    print("-------------------------------------------------------")
    print(f"Welcome, {user}")
    print("Enter 1 to deposite")
    print("Enter 2 to withdraw: ")
    print("Enter 3 to Transfer to another account")
    print("Enter 4 to view balance")
    print("Enter 5 to view transaction history")
    print("Enter 6 to logout")
    print("Enter 7 to exit")