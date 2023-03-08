[![Build Status](https://app.travis-ci.com/feelofgoodvibes/statok.svg?branch=main)](https://app.travis-ci.com/feelofgoodvibes/statok)
[![Coverage Status](https://coveralls.io/repos/github/feelofgoodvibes/statok/badge.svg?branch=main)](https://coveralls.io/github/feelofgoodvibes/statok?branch=main)

# 💰 Statok | Money Manager

Statok - is an application for money management.
It provides REST API and Web Application, which allows user to manage his budget:
- Add infomation about his incomes and expenses in a form of operations;
- Manage incomes and expenses categories;
- Sort operations by categories;
- View list of all operations and categories;
- View operations statistics and total avaiable budget;

## How to build
Before building, make sure you have python>=3.9 and MySQL installed and configured. Also, It is recommended to build inside separate virtual environment:
1. Clone repository (`git clone https://github.com/feelofgoodvibes/statok`)
2. Install dependencies (`pip install -r requirements.txt` or `pip install .`)
3. Set global environment variables `MYSQL_USER` and `MYSQL_PASS` (username and password for MySQL)
4. Create database `statok_db` (`CREATE DATABASE statok_db` via mysql-shell)
5. Change working directory to `statok_app` (`cd statok_app`). Apply migrations to database schema:
    - `flask db upgrade +1` - to create only database tables
    - `flask db upgrade` - to create database tables and populate them with test data
6. Go back to project root directory (`cd ..`)
7. Run application: `gunicorn "statok_app.app:create_app()"`

**🎉 App is up and running!**
It is available under address and port, specified inside `gunicorn.conf.py` configuration file (by default it's `http://localhost:5000`)
