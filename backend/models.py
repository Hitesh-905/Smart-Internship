from sqlalchemy import Column, Integer, String
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    resume_text = Column(String)  # We will store the text from their resume here
    skills = Column(String)       # Extracted skills (e.g., "Python, React")

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    required_skills = Column(String) # e.g., "Python, AWS"