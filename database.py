from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import base

# Create all tables in the database (this should be run once to create tables)


DATABASE_URL="sqlite:///database.db"
engine=create_engine(DATABASE_URL)
base.metadata.create_all(engine)
Session=sessionmaker(bind=engine)
session=Session()