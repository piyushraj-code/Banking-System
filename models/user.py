from config import database

class User():
    
    def __init__(self, name, account_number, db):
        self.name = name
        self.account_number = account_number
        self.db = db

    def __str__(self):
        return f"{self.name} || Account Number: {self.account_number}"

    def deposite(self, amount):
        
        if amount <= 0:
            # print("Amount must be greater than zero")
            return {
                "success": False,
                "message": "Amount must be greater than zero"
            }
        cursor = self.db.get_cursor()
        try:
            if cursor:
                # query = "SELECT balance FROM users where account_number = %s"
                # self.db.cunn.execute(query, (self.account_number,))
                # initial = self.db.cunn.fetchone()
                # final = initial[0] + amount
                try:
                    query = "UPDATE users SET balance = balance + %s WHERE account_number = %s"
                    cursor.execute(query, (amount, self.account_number))
                    # print(f"{amount} Successfully deposited to account number: {self.account_number}")
                    query = "INSERT INTO transactions (to_account, amount, transaction_type) VALUES (%s, %s, %s)"
                    cursor.execute(query, (self.account_number, amount, "Deposite"))
                    self.db.db.commit()
                    return {
                        "success": True,
                        "message": f"{amount} Successfully deposited to account number: {self.account_number}"
                    }
                except Exception as e:
                    self.db.db.rollback()
                    # print("Deposite Failed!!", e)
                    return {
                        "success": False,
                        "message": "Deposite Failed!"
                    }
        finally:
            cursor.close()

    def withdraw(self, amount):
        if amount <= 0:
            # print("Amount must be greater than zero")
            return {
                "success": False,
                "message": "Amount must be greater than zero"
            }
        cursor = self.db.get_cursor()
        try:
            if cursor:
                query = "SELECT balance FROM users where account_number = %s"
                cursor.execute(query, (self.account_number,))
                initial = cursor.fetchone()
                if initial[0] < float(amount):
                    # print("Not Enough Balance")
                    return {
                        "success": False,
                        "message": "Not Enough Balance"
                    }
                else:
                    try:
                        query = "UPDATE users SET balance = balance - %s WHERE account_number = %s"
                        cursor.execute(query, (amount, self.account_number))
                        # print(f"{amount} Successfully withdrawn from account number: {self.account_number}")
                        query = "INSERT INTO transactions (from_account, amount, transaction_type) VALUES (%s, %s, %s)"
                        cursor.execute(query, (self.account_number, amount, "Withdrawn"))
                        self.db.db.commit()
                        return {
                            "success": True,
                            "message": f"{amount} Successfully withdrawn from account number: {self.account_number}"
                        }
                    except Exception as e:
                        self.db.db.rollback()
                        # print("Withdraw Failed!!", e)
                        return {
                            "success": False,
                            "message": "Withdraw Failed!"
                        }
        finally:
            cursor.close()

    def transfer(self, other, amount):
        if amount <= 0:
            # print("Amount must be greater than zero")
            return {
                "success": False,
                "message": "Amount must be greater than zero"
            }
        if other == self.account_number:
            # print("Cannot transfer to your own account")
            return {
                "success": False,
                "message": "Cannot transfer to your own account"
            }
        cursor = self.db.get_cursor()
        try:
            if cursor:
                query = "SELECT balance FROM users where account_number = %s"
                cursor.execute(query, (self.account_number,))
                my_initial = cursor.fetchone()
                if my_initial[0] < float(amount):
                    # print("Not Enough Balance")
                    return {
                    "success": False,
                    "message": "Not Enough Balance"
                    }
                else:
                    my_final = my_initial[0] - amount
                    query = "SELECT balance FROM users where account_number = %s"
                    cursor.execute(query, (other,))
                    other_initial = cursor.fetchone()
                    if other_initial is None:
                        # print("Reciepient account does't exist")
                        return {
                            "success": False,
                            "message": "Reciepient account does't exist"
                        }
                    other_final = other_initial[0] + amount
                    try:
                        query = "UPDATE users SET balance = balance - %s WHERE account_number = %s"
                        cursor.execute(query, (amount, self.account_number))

                        query = "UPDATE users SET balance = balance + %s WHERE account_number = %s"
                        cursor.execute(query, (amount, other))

                        query = "INSERT INTO transactions (from_account, to_account, amount, transaction_type) values (%s, %s, %s, %s)"
                        cursor.execute(query, (self.account_number, other, amount, "Transfer"))
                        self.db.db.commit()
                        # print(f"{amount} Successfully transferred from account number {self.account_number} to {other}")
                        return {
                            "success": True,
                            "message": f"{amount} Successfully transferred from account number {self.account_number} to {other}"
                        }
                    except Exception as e:
                        self.db.db.rollback()
                        # print("Transaction Failed", e) 
                        return {
                            "success": False,
                            "message": f"Transactrion Failed {e}"
                        }
        finally:
            cursor.close()

    def view_balance(self):
        cursor = self.db.get_cursor()
        if cursor:
            try:
                query = "SELECT balance FROM users WHERE account_number = %s"
                cursor.execute(query, (self.account_number,))
                current_balance = cursor.fetchone()
                return {
                    "message": f"Your Current balance is: {current_balance[0]}"
                }
            except Exception as e:
                return {
                    "message": "Can't Fetch your balance please try again"
                }
            finally:
                cursor.close()

    def view_transaction_history(self):
        cursor = self.db.get_cursor()
        query = "SELECT transaction_id, from_account, to_account, amount, transaction_date, transaction_type FROM transactions WHERE from_account = %s OR to_account = %s ORDER BY transaction_date DESC"
        cursor.execute(query, (self.account_number, self.account_number))
        history = cursor.fetchall()
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
            