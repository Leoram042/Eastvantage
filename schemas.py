# Import the necessary module for defining Pydantic models
from pydantic import BaseModel


# Create a Pydantic model called 'Address'
class Address(BaseModel):
	id: int  # An integer field for 'id'
	name: str  # A string field for 'name'
	city: str  # A string field for 'city'
	country: str  # A string field for 'country'
	distance_from_chennai: int  # An integer field for 'distance_from_chennai'

	# Define a configuration class for this Pydantic model
	class Config:
		orm_mode = True
		# Set 'orm_mode' to True, which allows this Pydantic model to be used
		# for interacting with SQLAlchemy ORM models for database operations

# This Pydantic model represents the structure of the data you expect
# for working with address-related information in your FastAPI application.
