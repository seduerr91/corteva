from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a db URL for schema
SQLALCHEMY_DATABASE_URL = "sqlite:///./corteva_fastapi.db"

# Create SQL Alchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Alembic Note
# Normally we would probably initialize this database(create tables, etc) with Alembic to use it for migrations.
