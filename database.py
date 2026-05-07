
# # used to connect our fastapi to sqllite database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLite database URL- # # this below is the string for the sqllite database
URL_DATABASE = "sqlite:///./finance.db"

# Create engine
engine = create_engine(URL_DATABASE, connect_args={"check_same_thread": False})

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
