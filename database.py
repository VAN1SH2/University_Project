from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, declarative_base

SQL_DB_URL = "postgresql://postgres:qawsed12qE!@localhost:5432/test_db"
engine = create_engine(SQL_DB_URL)
session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)
base = declarative_base()
