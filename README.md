[![Build Status](https://app.travis-ci.com/feelofgoodvibes/statok.svg?branch=main)](https://app.travis-ci.com/feelofgoodvibes/statok)
[![Coverage Status](https://coveralls.io/repos/github/feelofgoodvibes/statok/badge.svg?branch=main)](https://coveralls.io/github/feelofgoodvibes/statok?branch=main)

# 💰 Statok | Money Manager

![image](https://user-images.githubusercontent.com/53279267/224517064-4c96bc1c-8f09-4544-91a6-7d9ce6b40390.png)

Statok - is an application for money management.
It provides REST API and Web Application, which allows user to manage his budget:
- Add infomation about his incomes and expenses in a form of operations;
- Manage incomes and expenses categories;
- Sort operations by categories;
- View list of all operations and categories;
- View operations statistics and total avaiable budget;

## Used technologies

#### Main

- [Flask](https://flask.palletsprojects.com) as web framework
- [MySQL](https://www.mysql.com) as database
- [SQLAlchemy](https://www.sqlalchemy.org) + [Alembic](https://alembic.sqlalchemy.org) as ORM and migrations management
- [Pydantic](https://docs.pydantic.dev) as data validator

#### Additional

- [pytest](https://docs.pytest.org) as framework for testing
- [Travis-CI](https://www.travis-ci.com) as CI/CD
- [Coveralls.io](https://coveralls.io) + [Coverage](https://coverage.readthedocs.io/en/7.2.1/) as code coverage tracker

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
It is available at the address and port specified in the `gunicorn.conf.py` configuration file (by default `http://localhost:5000`)
