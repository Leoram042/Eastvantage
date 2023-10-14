from sqlalchemy import create_engine
from sqlalchemy.dialects.sqlite import *
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from typing import List
from pydantic import BaseModel, constr
from fastapi import FastAPI, Depends

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./address_book.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Addresses(Base):
	__tablename__ = 'addresses'
	id = Column(Integer, primary_key=True, nullable=False)
	name = Column(String(50), unique=True)
	city = Column(String(50))
	country = Column(String(50))
	distance_from_chennai = Column(Float)


Base.metadata.create_all(bind=engine)


class Address(BaseModel):
	id: int
	name: str
	city: str
	country: str
	distance_from_chennai: int

	class Config:
		orm_mode = True


def get_db():
	db = session()
	try:
		yield db
	finally:
		db.close()


@app.post('/add_new_address', response_model=Address)
def add_address(address: Address, db: Session = Depends(get_db)):
	new_address = Addresses(id=address.id, name=address.name, city=address.city,
	                        country=address.country, distance_from_chennai=address.distance_from_chennai)
	db.add(new_address)
	db.commit()
	db.refresh(new_address)

	return Addresses(**address.dict())


@app.get('/list_addresses', response_model=List[Address])
def get_addresses(db: Session = Depends(get_db)):
	result = db.query(Addresses).all()

	return result


@app.get('/get_address/{city}/{distance}', response_model=Address)
def get_address_from_city_and_distance(city: str, distance: str, db: Session = Depends(get_db)):
	return db.query(Addresses).filter(Addresses.city == city and Addresses.distance_from_chennai == distance).first()


@app.put('/update_address/{id}', response_model=Address)
def update_address(id: int, address: Address, db: Session = Depends(get_db)):
	current_address = db.query(Addresses).filter(Addresses.id == id).first()
	current_address.id = address.id
	current_address.name = address.name
	current_address.city = address.city
	current_address.country = address.country
	current_address.distance_from_chennai = address.distance_from_chennai
	db.commit()

	return db.query(Addresses).filter(Addresses.id == id).first()


@app.delete('/delete_address/{id}')
def delete_address(id: int, db: Session = Depends(get_db)):
	try:
		db.query(Addresses).filter(Addresses.id == id).delete()
		db.commit()

	except Exception as e:
		raise Exception(e)

	return {"delete status": "success, address deleted"}
