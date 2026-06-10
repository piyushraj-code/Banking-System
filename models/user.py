from config import database
class User():
    db = database.DataBase()
    def __init__(self, name, account_number):
        self.name = name
        self.account_number = account_number

    def deposite(self, amount):
        if self.db.cunn:
            query = "SELECT balance FROM users where account_number = %s"
            self.db.cunn.execute(query, (self.account_number))
            initial = self.db.cunn.fetchone()
            final = initial + amount
            try:
                query = "UPDATE users SET balance = %s WHERE account_number = %s"
                self.db.cunn.execute(query, (final, self.account_number))
                self.db.commit()
                print(f"{amount} Successfully deposited to account number: {self.account_number}")
            except Exception as e:
                print("Deposite Failed!!", e)

    def withdraw(self, amount):
        if self.db.cunn:
            query = "SELECT balance FROM users where account_number = %s"
            self.db.cunn.execute(query, (self.account_number))
            initial = self.db.cunn.fetchone()
            if initial < amount:
                print("Not Enough Balance")
            else:
                final = initial - amount
                try:
                    query = "UPDATE users SET balance = %s WHERE account_number = %s"
                    self.db.cunn.execute(query, (final, self.account_number))
                    self.db.commit()
                    print(f"{amount} Successfully withdrawn from account number: {self.account_number}")
                except Exception as e:
                    print("Deposite Failed!!", e)

    def transfer(self, other, amount):
        if self.db.cunn:
            query = "SELECT balance FROM users where account_number = %s"
            self.db.cunn.execute(query, (self.account_number))
            my_initial = self.db.cunn.fetchone()
            if my_initial < amount:
                print("Not Enough Balance")
            else:
                my_final = my_initial - amount
                query = "SELECT balance FROM users where account_number = %s"
                self.db.cunn.execute(query, (self.account_number))
                other_initial = self.db.cunn.fetchone()
                other_final = other_initial + amount
                try:
                    query = "UPDATE users SET balance = %s WHERE account_number = %s"
                    self.db.cunn.execute(query, (my_final, self.account_number))
                    self.db.commit()
                    query = "UPDATE users SET balance = %s WHERE account_number = %s"
                    self.db.cunn.execute(query, (other_final, other))
                    self.db.commit()
                    query = "INSERT INTO transactions (from_account, to_account) values (%s, %s)"
                    self.db.cunn.execute(query, (self.account_number, other))
                    self.db.commit()
                    print(f"{amount} Successfully transferred from account number {self.account_number} to {other}")
                except Exception as e:
                    print("Transaction Failed", e) 
                      
    def view_balance(self):
        query = "SELECT balance FROM users WHERE account_number = %s"
        self.db.cunn.execute(query, (self.account_number,))
        current_balance = self.db.cunn.fetchaone()
        print(f"Your Current balance is: {current_balance}")

