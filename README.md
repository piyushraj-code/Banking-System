# 🏦 Digital Bank
 
A full-stack digital banking web application built with **Flask**, **MySQL**, and **vanilla JavaScript**. Supports user registration, authentication, balance management, fund transfers, and transaction history.
 
---
 
## 📋 Table of Contents
 
- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Features](#features)
- [Database Schema](#database-schema)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [API Reference](#api-reference)
- [CLI Mode](#cli-mode)
- [Known Limitations](#known-limitations)
---
 
## Overview
 
Digital Bank is a web-based banking simulation application where users can open an account, log in securely, and perform common banking operations such as depositing funds, withdrawing cash, transferring money to other accounts, and reviewing their full transaction history.
 
The application uses **bcrypt** for password hashing, **Flask sessions** for authentication state, and **MySQL** as the persistent data store with full ACID-compliant transaction handling.
 
---
 
## Tech Stack
 
| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | Python 3.x, Flask                 |
| Database   | MySQL 8.x, mysql-connector-python |
| Auth       | bcrypt, Flask sessions            |
| Frontend   | HTML5, CSS3, Vanilla JavaScript   |
| Config     | python-dotenv                     |
 
---
 
## Project Structure
 
```
digital-bank/
├── app.py                  # Flask application & route definitions
├── main.py                 # CLI interface (development/testing)
├── config/
│   ├── __init__.py
│   └── database.py         # MySQL connection management
├── models/
│   ├── __init__.py
│   └── user.py             # User model — deposit, withdraw, transfer, history
├── services/
│   ├── __init__.py
│   └── authentication.py   # Registration & login logic
├── utils/
│   ├── init.py
│   └── utils.py            # Account number generation, CLI helpers
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── img/
│       ├── bank.png
│       └── log-out.png
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── .env                    # Environment variables (not committed)
├── .gitignore
└── README.md
```
 
---
 
## Features
 
- **User Registration** — Creates a new account with a unique auto-generated account number and a bcrypt-hashed password
- **Secure Login / Logout** — Session-based authentication with password verification via bcrypt
- **View Balance** — Fetches and displays the current account balance
- **Deposit** — Adds funds to the authenticated user's account
- **Withdraw** — Deducts funds with an insufficient-balance guard
- **Transfer** — Moves funds atomically between two accounts with rollback on failure
- **Transaction History** — Displays a full chronological log of all debits, credits, and transfers
---
 
## Database Schema
 
Run the following SQL against your MySQL instance to create the required database and tables.
 
```sql
CREATE DATABASE IF NOT EXISTS banking_system;
USE banking_system;
```
 
### `users` table
 
```sql
CREATE TABLE `users` (
  `id`             int NOT NULL AUTO_INCREMENT,
  `name`           varchar(100) DEFAULT NULL,
  `account_number` int DEFAULT NULL,
  `balance`        decimal(15,2) DEFAULT NULL,
  `password`       varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_number` (`account_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```
 
### `transactions` table
 
```sql
CREATE TABLE `transactions` (
  `transaction_id`   int NOT NULL AUTO_INCREMENT,
  `from_account`     int DEFAULT NULL,
  `to_account`       int DEFAULT NULL,
  `transaction_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `amount`           decimal(15,2) DEFAULT NULL,
  `transaction_type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`transaction_id`),
  KEY `from_account` (`from_account`),
  KEY `to_account` (`to_account`),
  CONSTRAINT `transactions_ibfk_1`
    FOREIGN KEY (`from_account`) REFERENCES `users` (`account_number`),
  CONSTRAINT `transactions_ibfk_2`
    FOREIGN KEY (`to_account`)   REFERENCES `users` (`account_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```
 
### Schema Diagram
 
```
users
─────────────────────────────────────
id               INT  PK  AUTO_INCREMENT
name             VARCHAR(100)
account_number   INT  UNIQUE
balance          DECIMAL(15,2)
password         VARCHAR(255)           ← bcrypt hash
        │
        │ (FK: from_account, to_account)
        ▼
transactions
─────────────────────────────────────
transaction_id   INT  PK  AUTO_INCREMENT
from_account     INT  FK → users.account_number  (NULL for deposits)
to_account       INT  FK → users.account_number  (NULL for withdrawals)
transaction_date TIMESTAMP  DEFAULT CURRENT_TIMESTAMP
amount           DECIMAL(15,2)
transaction_type VARCHAR(20)            ← "Deposite" | "Withdrawn" | "Transfer"
```
 
> **Note:** `from_account` is NULL for deposit transactions. `to_account` is NULL for withdrawal transactions. Both are populated for transfers.
 
---
 
## Prerequisites
 
- Python 3.9+
- MySQL 8.x server running locally or remotely
- `pip` for Python package management
---
 
## Installation & Setup
 
### 1. Clone the repository
 
```bash
git clone https://github.com/your-username/digital-bank.git
cd digital-bank
```
 
### 2. Create and activate a virtual environment
 
```bash
python -m venv .venv
 
# macOS / Linux
source .venv/bin/activate
 
# Windows
.venv\Scripts\activate
```
 
### 3. Install dependencies
 
```bash
pip install flask mysql-connector-python bcrypt python-dotenv
```
 
> **Tip:** Generate a `requirements.txt` for your team:
> ```bash
> pip freeze > requirements.txt
> # Later: pip install -r requirements.txt
> ```
 
### 4. Set up the database
 
Log in to your MySQL instance and run the SQL in the [Database Schema](#database-schema) section above, or pipe it directly:
 
```bash
mysql -u root -p < schema.sql
```
 
### 5. Configure environment variables
 
Create a `.env` file in the project root (see [Environment Variables](#environment-variables) below).
 
---
 
## Environment Variables
 
Create a `.env` file at the project root. **Never commit this file.**
 
```env
# .env
 
# Flask session signing key — use a long, random string
SECRET_KEY=your-very-secret-random-key-here
 
# MySQL connection details
DATABASE_URL=127.0.0.1
DB_PASSWORD=your_mysql_root_password
```
 
| Variable       | Description                                              | Example              |
|----------------|----------------------------------------------------------|----------------------|
| `SECRET_KEY`   | Flask session secret. Generate with `python -c "import secrets; print(secrets.token_hex(32))"` | `a3f9...` |
| `DATABASE_URL` | MySQL host (IP or hostname)                              | `127.0.0.1`          |
| `DB_PASSWORD`  | Password for the `root` MySQL user                       | `mypassword`         |
 
---
 
## Running the Application
 
### Web application (Flask)
 
```bash
python app.py
```
 
The server starts at **http://127.0.0.1:5000** by default.
 
```
 * Running on http://127.0.0.1:5000
 * Database Connection Successful
```
 
Navigate to `http://127.0.0.1:5000` in your browser to access the landing page.
 
### Pages
 
| URL          | Description                          |
|--------------|--------------------------------------|
| `/`          | Landing / home page                  |
| `/register`  | New user registration form           |
| `/login`     | Login form                           |
| `/dashboard` | Authenticated user dashboard         |
 
---
 
## API Reference
 
All endpoints return JSON. State-mutating endpoints require an active session (set by `/login`). Unauthenticated requests to protected routes are redirected to `/login`.
 
---
 
### `POST /register`
 
Register a new user account.
 
**Request body**
```json
{
  "name": "Piyush Raj",
  "balance": 5000,
  "password": "securepassword"
}
```
 
**Success response**
```json
{
  "success": true,
  "message": "Registration Successful your account number is: 47291"
}
```
 
**Error responses**
```json
{ "success": false, "message": "Password must be at least 8 character long" }
{ "success": false, "message": "Registration Failed" }
```
 
---
 
### `POST /login`
 
Authenticate a user and create a session.
 
**Request body**
```json
{
  "account_number": 47291,
  "password": "securepassword"
}
```
 
**Success response**
```json
{
  "success": true,
  "message": "Login Successful"
}
```
 
**Error responses**
```json
{ "success": false, "message": "Account not found!" }
{ "success": false, "message": "Invaid account number or password" }
```
 
---
 
### `GET /view_balance` 🔒
 
Returns the current balance for the authenticated user.
 
**Success response**
```json
{
  "success": true,
  "message": "Your Current balance is: 5000.00"
}
```
 
---
 
### `POST /deposite` 🔒
 
Deposit funds into the authenticated user's account.
 
**Request body**
```json
{ "amount": 1000 }
```
 
**Success response**
```json
{
  "success": true,
  "message": "1000 Successfully deposited to account number: 47291"
}
```
 
**Error responses**
```json
{ "success": false, "message": "Amount must be greater than zero" }
{ "success": false, "message": "Deposite Failed!" }
```
 
---
 
### `POST /withdraw` 🔒
 
Withdraw funds from the authenticated user's account.
 
**Request body**
```json
{ "amount": 500 }
```
 
**Success response**
```json
{
  "success": true,
  "message": "500 Successfully withdrawn from account number: 47291"
}
```
 
**Error responses**
```json
{ "success": false, "message": "Amount must be greater than zero" }
{ "success": false, "message": "Not Enough Balance" }
{ "success": false, "message": "Withdraw Failed!" }
```
 
---
 
### `POST /transfer` 🔒
 
Transfer funds to another account atomically.
 
**Request body**
```json
{
  "recipient": 83402,
  "amount": 200
}
```
 
**Success response**
```json
{
  "success": true,
  "message": "200 Successfully transferred from account number 47291 to 83402"
}
```
 
**Error responses**
```json
{ "success": false, "message": "Amount must be greater than zero" }
{ "success": false, "message": "Cannot transfer to your own account" }
{ "success": false, "message": "Not Enough Balance" }
{ "success": false, "message": "Reciepient account does't exist" }
{ "success": false, "message": "Enter valid amount or account number" }
```
 
---
 
### `POST /transaction_history` 🔒
 
Returns full transaction history for the authenticated user, ordered by date descending.
 
**Success response**
```json
{
  "success": true,
  "data": [
    {
      "Transaction_id": 12,
      "Sender": 47291,
      "Receipent": 83402,
      "Amount": 200.00,
      "Date": "2026-06-15T10:23:01",
      "Type": "Sent"
    },
    {
      "Transaction_id": 8,
      "Sender": null,
      "Receipent": 47291,
      "Amount": 1000.00,
      "Date": "2026-06-14T09:10:45",
      "Type": "Deposite"
    }
  ]
}
```
 
**Transaction `Type` values**
 
| Value      | Meaning                                         |
|------------|-------------------------------------------------|
| `Deposite` | Funds were deposited into this account          |
| `Withdrawn`| Funds were withdrawn from this account          |
| `Sent`     | This account sent a transfer to another account |
| `Received` | This account received a transfer                |
 
---
 
### `POST /logout` 🔒
 
Clears the session and redirects to the home page.
 
**Response**
```json
{
  "success": true,
  "redirect": "/"
}
```
 
## License
 
© 2026 Piyush Raj. All rights reserved.