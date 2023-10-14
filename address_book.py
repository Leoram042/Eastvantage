# Import the necessary modules and classes from FastAPI, SQLAlchemy, and your custom modules
from sqlalchemy.orm import Session
from database import session  # Import your database session
from models import Addresses  # Import the SQLAlchemy model for Addresses
from schemas import Address  # Import the Pydantic schema for Address
from typing import List
from fastapi import FastAPI, Depends

# Create a FastAPI instance
app = FastAPI()


# Define a function to get the database session
def get_db():
	db = session()  # Create a new database session
	try:
		yield db  # Yield the database session to the route functions
	finally:
		db.close()  # Close the database session when done


# Define the root route with a welcome message
@app.get("/")
def read_root():
	return {"message": "Welcome to my FastAPI application!"}


# Route to add a new address to the database
@app.post('/add_new_address', response_model=Address)
def add_address(address: Address, db: Session = Depends(get_db)):
	# Create a new Addresses object based on the input data
	new_address = Addresses(id=address.id, name=address.name, city=address.city,
	                        country=address.country, distance_from_chennai=address.distance_from_chennai)
	db.add(new_address)  # Add the new address to the database session
	db.commit()  # Commit the transaction to save the new address to the database
	db.refresh(new_address)  # Refresh the object to get any database-generated values
	return Addresses(**address.dict())  # Return the added address


# Route to list all addresses in the database
@app.get('/list_addresses', response_model=List[Address])
def get_addresses(db: Session = Depends(get_db)):
	result = db.query(Addresses).all()  # Query the database to retrieve all addresses
	return result  # Return the list of addresses


# Route to get an address based on city and distance
@app.get('/get_address/{city}/{distance}', response_model=Address)
def get_address_from_city_and_distance(city: str, distance: str, db: Session = Depends(get_db)):
	return db.query(Addresses).filter(Addresses.city == city and Addresses.distance_from_chennai == distance).first()


# Route to update an existing address
@app.put('/update_address/{id}', response_model=Address)
def update_address(id: int, address: Address, db: Session = Depends(get_db)):
	current_address = db.query(Addresses).filter(Addresses.id == id).first()  # Find the address by ID
	current_address.id = address.id
	current_address.name = address.name
	current_address.city = address.city
	current_address.country = address.country
	current_address.distance_from_chennai = address.distance_from_chennai
	db.commit()  # Commit the changes to the database
	return db.query(Addresses).filter(Addresses.id == id).first()  # Return the updated address


# Route to delete an address by ID
@app.delete('/delete_address/{id}')
def delete_address(id: int, db: Session = Depends(get_db)):
	try:
		db.query(Addresses).filter(Addresses.id == id).delete()  # Delete the address by ID
		db.commit()  # Commit the deletion
	except Exception as e:
		raise Exception(e)  # Handle any exceptions that occur during deletion
	return {"delete status": "success, address deleted"}  # Return a success message
