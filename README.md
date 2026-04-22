# Devs Bank of Mississippi

Devs Bank of Mississippi is a full stack Django banking application built to simulate core banking operations in a clean web interface. The project demonstrates backend logic, authentication, account management, transaction handling, and secure configuration practices using Python and Django.

## Overview

This project was built to model the kinds of features a real banking platform would need at a basic level, including user authentication, checking and savings account support, deposits, withdrawals, transfers, and transaction history.

It is designed as a portfolio project that shows practical software engineering skills with Django, database modeling, forms, views, templates, and environment based configuration.

## Features

- User registration, login, and logout
- Checking and savings account support
- Deposit functionality
- Withdrawal functionality
- Internal transfer functionality
- Transaction history tracking
- Environment variable based configuration
- Django admin support

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite
- **Frontend:** Django Templates, HTML, CSS
- **Environment Management:** python-dotenv
- **Version Control:** Git and GitHub

## Project Structure

```text
devs_bank_of_mississippi/
├── banking/
├── devs_bank_ms/
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore

Installation

1. Clone the repository
git clone https://github.com/veriesseals/devs_bank_of_mississippi.git
cd devs_bank_of_mississippi

2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Create your environment file

Create a file named .env in the project root and add your environment values.

SECRET_KEY=your-secret-key-here
DEBUG=True

5. Run migrations
python manage.py migrate

6. Create a superuser
python manage.py createsuperuser

7. Start the development server
python manage.py runserver

Then open your browser and go to:
http://127.0.0.1:8000/