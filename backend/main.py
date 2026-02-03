from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# 1. Create the database tables automatically
models.Base.metadata.create_all(bind=engine)

# 2. Initialize the App
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. Simple API Routes (Endpoints)

@app.get("/")
def read_root():
    return {"message": "Smart Internship Allocation Engine is Running!"}

@app.post("/students/")
def create_student(name: str, email: str, skills: str, db: Session = Depends(get_db)):
    # Create a new student object
    new_student = models.Student(name=name, email=email, skills=skills)
    # Add to DB
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@app.get("/students/")
def read_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()