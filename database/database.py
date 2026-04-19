# TODO Create a database connection
# TODO Create a dynamic function to initialize tables and insertion of data

import uuid

from sqlalchemy import Enum, create_engine, inspect, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from logger_config import logger

# Instantiate the engine and session

engine = create_engine('sqlite:///booking.db')
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
    except Exception as e:
        logger.error(f"Error creating table '{model.__tablename__}': {e}")
        
# insert_data function inserts data into the specified table
# **data: a dictionary of column names and their corresponding values to be inserted into the table
def insert_data(model: Base, **data):
    try: 
        session = session()
        new_record = model(**data)
        session.add(new_record)
        session.commit()
        session.close()
        
        logger.info(f"Data inserted successfully into {model.__tablename__}")
    except Exception as e:
        logger.error(f"Error inserting data into {model.__tablename__}: {e}")


# ==============================================================================================================================================
# Instantiate tables 
# ==============================================================================================================================================

# Tables

Roles = ['provider', 'customer']
Status = ['pending', 'confirmed', 'cancelled', 'completed']

Providers = create_model(
    'providers',
    id=Column(String, primary_key=True, default=lambda: str(uuid.uuid4())),
    name=Column(String, nullable=False),
    service=Column(String, nullable=False),
    email=Column(String, nullable=False, unique=True),
    password=Column(String, nullable=False),
    created_at=Column(DateTime, nullable=False)
)

Customers = create_model(
    'customers',
    id=Column(String, primary_key=True, default=lambda: str(uuid.uuid4())),
    name=Column(String, nullable=False),
    email=Column(String, nullable=False, unique=True),
    password=Column(String, nullable=False),
    created_at=Column(DateTime, nullable=False)
)

Services = create_model(
    'services',
    id=Column(String, primary_key=True, default=lambda: str(uuid.uuid4())),
    provider_id=Column(String, ForeignKey('providers.id'), nullable=False),  # Foreign key to Providers table
    name=Column(String, nullable=False),
    description=Column(String, nullable=False),
    price=Column(Integer, nullable=False),
    created_at=Column(DateTime, nullable=False)
)

Bookings = create_model(
    'bookings',
    id=Column(String, primary_key=True, default=lambda: str(uuid.uuid4())),
    provider_id=Column(String, ForeignKey('providers.id'), nullable=False),  # Foreign key to Providers table
    customer_id=Column(String, ForeignKey('customers.id'), nullable=False),  # Foreign key to Customers table
    service=Column(String, nullable=False),
    booking_time=Column(DateTime, nullable=False),
    status=Column(Enum(*Status, name="status_enum"), nullable=False, default='pending'),
    created_at=Column(DateTime, nullable=False),
)

if __name__ == "__main__":
    pass
    # Test