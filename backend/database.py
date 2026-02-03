from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This creates a file named 'internship.db' in your folder
SQL_ALCHEMY_DATABASE_URL = "sqlite:///./internship.db"

# Create the engine to talk to the database
engine = create_engine(
    SQL_ALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class (we use this to create a database session for each request)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models
Base = declarative_base()