from sqlalchemy import create_engine
import os

DBPASS = os.environ['DBPASSWORD']
DBUSER = os.environ['DBUSER']
DB = os.environ['DB']
DBHOST = os.environ['DBHOST']

Engine = create_engine(f'postgresql://{DBUSER}:{DBPASS}@{DBHOST}:5432/{DB}')