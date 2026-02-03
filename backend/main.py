from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware  # <--- IMPORT THIS
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import ai_engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- CONFIGURING CORS ---
# This allows the frontend (running on port 5173) to talk to this backend
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],
)
# ------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Smart Internship AI is Active"}

@app.post("/students/")
def create_student(name: str, email: str, skills: str, db: Session = Depends(get_db)):
    new_student = models.Student(name=name, email=email, skills=skills)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@app.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()
    resume_text = ai_engine.extract_text_from_pdf(content)
    
    # Simple Matching Logic
    sample_job_skills = "Python, Data Science, Machine Learning, SQL"
    match_score = ai_engine.calculate_match_score(resume_text, sample_job_skills)
    
    return {
        "filename": file.filename,
        "extracted_text_snippet": resume_text[:200] + "...",
        "match_score": match_score,
        "matched_against": sample_job_skills
    }