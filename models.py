from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

base = declarative_base()

# Users Model (Job Seekers)
class Users(base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    Firstname = Column(String(20), nullable=False)
    Lastname = Column(String(20), nullable=False)
    PhoneNumber = Column(Integer, nullable=False)
    Pincode = Column(Integer, nullable=False)
    Description = Column(String(500), nullable=True)
    Email = Column(String(50), nullable=True)
    role=Column(String(50),default='Employer')

    # Relationship with jobs

class Hirer(base):
    __tablename__ = 'hirers'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    phone_number = Column(String(15), nullable=False, unique=True)
    verified = Column(String(10), default="NO")
    pincode = Column(Integer, nullable=False)
    
    
    # Relationship to the Job model
    jobs = relationship('Job', backref='hirer', lazy=True)

    def __repr__(self):
        return f"<Hirer {self.firstname} {self.lastname}>"

# Job Model (Job Postings)
class Job(base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    location_link = Column(String(255), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(2000), nullable=False)
    pincode = Column(Integer, nullable=False)

    # Foreign Key to link job to hirer (Employer)
    hirer_id = Column(Integer, ForeignKey('hirers.id'), nullable=False)

    def __repr__(self):
        return f"<Job {self.title}>"