from sqlalchemy import Column, String, Integer, Date, JSON
from database import Base

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    password = Column(String)

# Dynamic Dataset model that stores uploaded data as JSON
class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String, index=True)       # The username of the uploader
    upload_time = Column(Date)               # The time of upload
    data = Column(JSON)                      # Stores the entire dataset as JSON
