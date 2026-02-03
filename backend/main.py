from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import ai_engine  # We import our new AI brain

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Smart Internship AI is Active"}

# --- Student Routes ---

@app.post("/students/")
def create_student(name: str, email: str, skills: str, db: Session = Depends(get_db)):
    new_student = models.Student(name=name, email=email, skills=skills)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@app.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...)):
    # 1. Read the uploaded file
    content = await file.read()
    
    # 2. Use our AI Engine to extract text
    resume_text = ai_engine.extract_text_from_pdf(content)
    
    # 3. (Demo) Let's match it against a fake job description to test
    sample_job_skills = "Python, Data Science, Machine Learning, SQL"
    match_score = ai_engine.calculate_match_score(resume_text, sample_job_skills)
    
    return {
        "filename": file.filename,
        "extracted_text_snippet": resume_text[:200] + "...", # Show first 200 chars
        "match_score": match_score,
        "matched_against": sample_job_skills
    }