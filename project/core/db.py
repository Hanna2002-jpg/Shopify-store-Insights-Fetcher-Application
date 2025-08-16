from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Correct MySQL connection URL
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:Koloth%402002@localhost/shopify_insights"

# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base class for models
Base = declarative_base()

