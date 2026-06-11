from config import database

class User():
    db = database.DataBase()
    def __init__(self, name, account_number):
        self.name = name
        self.account_number = account_number

    def __str__(self):
        return f"{self.name} || Account Number: {self.account_number}"

    def deposite(self, amount):
        if amount <= 0:
            print("Amount must be greater than zero")
            return
        if self.db.cunn:
            query = "SELECT balance FROM users where account_number = %s"
            self.db.cunn.execute(query, (self.account_number,))
            initial = self.db.cunn.fetchone()
            final = initial[0] + amount
            try:
                query = "UPDATE users SET balance = %s WHERE account_number = %s"
                self.db.cunn.execute(query, (final, self.account_number))
                print(f"{amount} Successfully deposited to account number: {self.account_number}")
                query = "INSERT INTO transactions (to_account, amount, transaction_type) VALUES (%s, %s, %s)"
                self.db.cunn.execute(query, (self.account_number, amount, "Deposite"))
                self.db.db.commit()
            except Exception as e:
                print("Deposite Failed!!", e)

    def withdraw(self, amount):
        if amount <= 0:
            print("Amount must be greater than zero")
            return
        if self.db.cunn:
            query = "SELECT balance FROM users where account_number = %s"
            self.db.cunn.execute(query, (self.account_number,))
            initial = self.db.cunn.fetchone()
            if initial[0] < float(amount):
                print("Not Enough Balance")
            else:
                final = initial[0] - amount
                try:
                    query = "UPDATE users SET balance = %s WHERE account_number = %s"
                    self.db.cunn.execute(query, (final, self.account_number))
                    print(f"{amount} Successfully withdrawn from account number: {self.account_number}")
                    query = "INSERT INTO transactions (from_account, amount, transaction_type) VALUES (%s, %s, %s)"
                    self.db.cunn.execute(query, (self.account_number, amount, "Withdrawn"))
                    self.db.db.commit()
                except Exception as e:
                    print("Deposite Failed!!", e)

    def transfer(self, other, amount):
        if amount <= 0:
            print("Amount must be greater than zero")
            return
        if other == self.account_number:
            print("Cannot transfer to your own account")
            return
        if self.db.cunn:
            query = "SELECT balance FROM users where account_number = %s"
            self.db.cunn.execute(query, (self.account_number,))
            my_initial = self.db.cunn.fetchone()
            if my_initial[0] < float(amount):
                print("Not Enough Balance")
            else:
                my_final = my_initial[0] - amount
                query = "SELECT balance FROM users where account_number = %s"
                self.db.cunn.execute(query, (other,))
                other_initial = self.db.cunn.fetchone()
                if other_initial is None:
                    print("Reciepient account does't exist")
                    return
                other_final = other_initial[0] + amount
                try:
                    query = "UPDATE users SET balance = %s WHERE account_number = %s"
                    self.db.cunn.execute(query, (my_final, self.account_number))
                    
                    query = "UPDATE users SET balance = %s WHERE account_number = %s"
                    self.db.cunn.execute(query, (other_final, other))
                   
                    query = "INSERT INTO transactions (from_account, to_account, amount, transaction_type) values (%s, %s, %s, %s)"
                    self.db.cunn.execute(query, (self.account_number, other, amount, "Transfer"))
                    self.db.db.commit()
                    print(f"{amount} Successfully transferred from account number {self.account_number} to {other}")
                except Exception as e:
                    print("Transaction Failed", e) 

    def view_balance(self):
        query = "SELECT balance FROM users WHERE account_number = %s"
        self.db.cunn.execute(query, (self.account_number,))
        current_balance = self.db.cunn.fetchone()
        print(f"Your Current balance is: {current_balance[0]}")

    def view_transaction_history(self):
        query = "SELECT transaction_id, from_account, to_account, amount, transaction_date, transaction_type FROM transactions WHERE from_account = %s OR to_account = %s ORDER BY transaction_date DESC"
        self.db.cunn.execute(query, (self.account_number, self.account_number))
        history = self.db.cunn.fetchall()
        for i in history:
            print("-------------------------------------------------------")
            if i[5] == "Deposite":
                print(f"Transaction Type: Deposite || Transaction id: {i[0]} || Transferred to: {i[2]} || Transferred_from: {i[1]} || Amount: {i[3]} || Date {i[4]}")
            elif i[5] == "Withdrawn":
                print(f"Transaction Type: Withdrawn || Transaction id: {i[0]} || Transferred to: {i[2]} || Transferred_from: {i[1]} || Amount: {i[3]} || Date {i[4]}")
            elif i[1] == self.account_number:
                print(f"Transaction Type: Sent || Transaction id: {i[0]} || Transferred to: {i[2]} || Transferred_from: {i[1]} || Amount: {i[3]} || Date {i[4]}")
            else:
                print(f"Transaction Type: Received || Transaction id: {i[0]} || Transferred to: {i[2]} || Transferred_from: {i[1]} || Amount: {i[3]} || Date {i[4]}")
            