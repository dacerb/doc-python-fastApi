import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float
)

sqlite_file_name = "../database.sqlite"
base_dir = os.path.dirname(os.path.realpath(__file__)) # __file__ lee el directorio actual

database_url = f"sqlite:///{os.path.join(base_dir,sqlite_file_name)}"

engine = create_engine(database_url, echo=True)  # Echo muestra por consola lo que se realiza al momendo de crear la base de datos

Session = sessionmaker(bind=engine)

Base = declarative_base()


