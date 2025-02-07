from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

base = declarative_base()

# Users Model (Job Seekers)
class UsersLD(base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    Firstname = Column(String(20), nullable=False)
    Lastname = Column(String(20), nullable=False)
    Phone = Column(Integer, nullable=False)
    Email = Column(String(500), nullable=True)
    Password = Column(String(50), nullable=True)
    