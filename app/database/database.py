from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app import config

secrets: config.Settings = config.Settings()

engine = create_engine(secrets.SQLALCHEMY_DATABASE_URI, pool_size=15, max_overflow=5)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
