# TODO Create a database connection
# TODO Create a dynamic function to initialize tables and insertion of data
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid

from sqlalchemy import Enum, create_engine, inspect, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from utils.logger_config import logger
from utils.config import Config

# Credentials

DB_URL = Config.DB_URL

# Instantiate the engine and session
engine = create_engine(DB_URL)
session = sessionmaker(bind=engine)

# Instance for the base class to create models
# Base can be used to instantiate a parameter
# e.g func(model: Base)
class Base(DeclarativeBase):
    pass

# Dynamically creates a model class 
# table_name: name of the table to be created
# column_name: a dictionary of column names and their types (e.g., name=Column(String), age=Column(Integer))
def create_model(table_name: str, **column_name):
    
    params = {
        '__tablename__': table_name,
        
        **column_name
    }   
    
    return type(table_name, (Base,), params)

# init_tables function checks if the table exists, if not it creates the table
def init_tables(model: Base, ):
    try:
        inspector = inspect(engine)
        if not inspector.has_table(model.__tablename__):
            model.__table__.create(bind=engine)
            logger.info(f"Table '{model.__tablename__}' created successfully.")

        logger.info(f"Table '{model.__tablename__}' already exists.")
    except Exception as e:
        logger.error(f"Error creating table '{model.__tablename__}': {e}")
        
# insert_data function inserts data into the specified table
# **data: a dictionary of column names and their corresponding values to be inserted into the table
def insert_data(model: Base, **data):
    try: 
        db = session()
        new_record = model(**data)
        db.add(new_record)
        db.commit()
        db.close()
        
        logger.info(f"Data inserted successfully into {model.__tablename__}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error inserting data into {model.__tablename__}: {e}")

# ==============================================================================================================================================
# Instantiate tables 
# ==============================================================================================================================================

# Tables

Roles = ['admin', 'user']
Status = ['pending', 'confirmed', 'cancelled', 'completed']
Invitation = ['accepted', 'declined', 'pending', 'Not Sure']
Label = ['partner','family', 'friend', 'work', 'other',]


if __name__ == "__main__":
    pass