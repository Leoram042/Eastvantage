# Import the necessary modules from SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

# Import the 'engine' from the 'database' module
from database import engine

# Create a base class for declarative models
Base = declarative_base()


# Define a model for the 'addresses' table
class Addresses(Base):
	# Set the table name in the database
	__tablename__ = 'addresses'

	# Define individual columns in the 'addresses' table
	id = Column(Integer, primary_key=True, nullable=False)
	# Define an 'id' column as an Integer primary key that cannot be null
	name = Column(String(50), unique=True)
	# Define a 'name' column as a String with a maximum length of 50 characters,
	# and it should be unique
	city = Column(String(50))
	# Define a 'city' column as a String with a maximum length of 50 characters
	country = Column(String(50))
	# Define a 'country' column as a String with a maximum length of 50 characters
	distance_from_chennai = Column(Float)
	# Define a 'distance_from_chennai' column as a Float


# Create the table in the database using the 'engine'
# This step will create the 'addresses' table based on the model definition
Base.metadata.create_all(bind=engine)
