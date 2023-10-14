# Import the SQLALCHEMY_DATABASE_URL from the 'config' module
from config import SQLALCHEMY_DATABASE_URL

# Import the necessary SQLAlchemy modules
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create a SQLAlchemy database engine by connecting to the database URL
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory using the engine
# This session factory will be used to create individual database sessions
# with specific configurations for your FastAPI application.
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
