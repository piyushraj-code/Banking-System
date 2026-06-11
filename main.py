from services import authentication
from models import user
from utils import utils
current_user = None
def main():
    global current_user
    Auth = authentication.Authentication()
    while True:
        if current_user:
            utils.user_interface(current_user)
            command = int(input("Enter your command: "))
            if command == 1:
                amount = int(input("Enter amount to deposit: "))
                current_user.deposite(amount)
            elif command == 2:
                amount = int(input("Enter amount to withdraw: "))
                current_user.withdraw(amount)
            elif command == 3:
                amount = int(input("Enter amount to transfer: "))
                other = int(input("Enter receiver's account number: "))
                current_user.transfer(other, amount)
            elif command == 4:
                current_user.view_balance()
            elif command == 5:
                current_user.view_transaction_history()
            elif command == 6:
                current_user = None
            elif command == 7:

                break 
        else:
            utils.interface()
            command = int(input("Enter your command: "))
            if command == 1:
                Auth.register()
            elif command == 2:
                current_user = Auth.login()
            elif command == 3:
                break

if __name__ == "__main__":
    main()