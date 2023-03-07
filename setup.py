from setuptools import setup

setup(
    name="statok_app",
    version='1.0',
    author='Maksym Kochut',
    description='A money manager application',
    long_description='This package implements REST API for money management application, along with web interface for that API',
    url='https://github.com/feelofgoodvibes/statok',
    python_requires='>=3.9, <4',
    package_dir = {'': 'statok_app'},
    packages=[
        '.',
        'models',
        'rest',
        'schemas',
        'service',
        'views',
        'templates',
        'static'
    ],
    include_package_data=True,
    install_requires=[
        'alembic==1.9.4',
        'Flask==2.2.3',
        'Flask-Migrate==4.0.4',
        'Flask-RESTful==0.3.9',
        'Flask-SQLAlchemy==3.0.3',
        'gunicorn==20.1.0',
        'mysql-connector-python==8.0.32',
        'orjson==3.8.6',
        'requests==2.28.2',
        'SQLAlchemy==2.0.4',
        'pydantic==1.10.5'
    ],
    extras_require = {
        'testing': ['pytest==7.2.1',
                    'coverage==6.5.0',
                    'pylint==2.16.2']
    },
)