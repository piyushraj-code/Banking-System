from flask import Flask, render_template, request, redirect, session, jsonify
from services import authentication
from config import database
from models import user
import uuid
from dotenv import load_dotenv
import os
load_dotenv()
db = database.DataBase()
auth = authentication.Authentication(db)
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
if not app.secret_key:
   raise RuntimeError("SECRET_KEY is not set in the environment")
@app.route('/')
def index():
   return render_template('register.html')

@app.route("/login", methods= ["GET","POST"])
def login():
   if request.method == "POST":
      data = request.get_json()
      account_number = int(data.get("account_number"))
      password = data.get("password")
      result = auth.login(account_number, password)
      return jsonify(result)
   else:
      return render_template("login.html")


@app.route("/register", methods= ["GET", "POST"])
def register():
   if request.method == "POST":
      data = request.get_json()
      name = data.get("name")
      balance = data.get("balance")
      password = data.get("password")
      result = auth.register(name, balance, password)
      return jsonify(result)
   else:
      return render_template("register.html")

@app.route("/dashboard", methods= ["GET"])
def dashboard():
   if "account_number" not in session:
      return redirect("/login")
   return render_template("dashboard.html")

@app.route("/view_balance", methods= ["GET", "POST"])
def view_balance():
   if "account_number" not in session:
      return redirect("/login")
   name = session["name"]
   account_number = session["account_number"]
   current_user = user.User(name, account_number, db)
   result = current_user.view_balance()
   return jsonify(result)

@app.route("/deposite", methods= ["POST"])
def deposite():
   if "account_number" not in session:
      return redirect("/login")
   data = request.get_json()
   amount = int(data.get("amount"))
   name = session["name"]
   account_number = session["account_number"]
   current_user = user.User(name, account_number, db)
   result = current_user.deposite(amount)
   return jsonify(result)

@app.route("/withdraw" , methods=["POST"])
def withdraw():
   if "account_number" not in session:
      return redirect("/login")
   data = request.get_json()
   amount = int(data.get("amount"))
   name = session["name"]
   account_number = session["account_number"]
   current_user = user.User(name, account_number, db)
   result = current_user.withdraw(amount)
   return jsonify(result)

@app.route("/logout", methods= ["GET", "POST"])
def logout():
   session.clear()
   return jsonify({
      "message": " You have been logged out"
   })

@app.route("/transaction_history", methods= ["POST"])
def transaction_history():
   if "account_number" not in session:
      return redirect("/login")
   name = session["name"]
   account_number = session["account_number"]
   current_user = user.User(name, account_number, db)
   result = current_user.view_transaction_history()
   return jsonify(result)

@app.route("/transfer", methods= ["POST"])
def transfer():
   if "account_number" not in session:
      return redirect("/login")
   data = request.get_json()
   try:
      recipient= int(data.get("recipient"))  
      amount = int(data.get("amount"))
   except Exception as e:
      return jsonify({
         "success": False,
         "message": "Enter valid amount or account number"
      })
   name = session["name"]
   account_number = session["account_number"]
   current_user = user.User(name, account_number, db)
   result = current_user.transfer(recipient, amount)
   return jsonify(result)

if __name__ == '__main__':
   app.run(debug=True)