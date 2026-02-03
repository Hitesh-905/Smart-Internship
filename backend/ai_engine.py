from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import io

# 1. Helper function to read PDF
def extract_text_from_pdf(file_content):
    # Wrap the raw bytes in a file-like object so pypdf can read it
    pdf_file = io.BytesIO(file_content)
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# 2. The Core AI Matching Function
def calculate_match_score(resume_text, job_skills):
    # If the resume or job description is empty, return 0
    if not resume_text or not job_skills:
        return 0.0

    # Create a list containing the resume and the job skills
    documents = [resume_text, job_skills]

    # Convert text to numbers (Vectors)
    tfidf = TfidfVectorizer().fit_transform(documents)
    
    # Calculate similarity (0 to 1)
    # This compares the resume (index 0) against the job skills (index 1)
    cosine_sim = cosine_similarity(tfidf[0:1], tfidf[1:2])
    
    # Return the score as a percentage (e.g., 85.5)
    return round(cosine_sim[0][0] * 100, 2)