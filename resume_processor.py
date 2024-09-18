from PyPDF2 import PdfReader
import docx

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

import re
import spacy

nlp = spacy.load('en_core_web_sm')

def extract_metadata(text):
    doc = nlp(text)
    sections = ['Profile', 'Work Experience', 'Education', 'Skills', 'Technical Skills', 'Extracurricular', 'Projects', 'Technical Projects']
    extracted_data = {}
    for section in sections:
        match = re.search(f'{section}:(.*?)\n\n', text, re.DOTALL)
        extracted_data[section] = match.group(1) if match else None
    return extracted_data

from collections import Counter

def keyword_density(text, keywords):
    words = text.split()
    word_count = Counter(words)
    density = {keyword: word_count[keyword] / len(words) for keyword in keywords}
    return density

def keyword_proximity(text, keyword1, keyword2):
    words = text.split()
    positions1 = [i for i, word in enumerate(words) if word == keyword1]
    positions2 = [i for i, word in enumerate(words) if word == keyword2]
    if positions1 and positions2:
        return min([abs(pos1 - pos2) for pos1 in positions1 for pos2 in positions2])
    return None

def check_formatting(text):
    if re.search(r'\t+', text):
        return "Inconsistent formatting detected (tabs used)."
    elif re.search(r'\s\s+', text):
        return "Inconsistent spacing detected."
    return "Formatting is consistent."

def section_score(extracted_data, job_description):
    score = 0
    for section, content in extracted_data.items():
        if content and section in job_description:
            score += 1  
    return score

def match_requirements(resume_text, job_requirements):
    matches = [req for req in job_requirements if req in resume_text]
    return len(matches) / len(job_requirements)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def detect_duplicates(resume_texts):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(resume_texts)
    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix

def process_resume(file_path, job_description, job_requirements):
    text = extract_text_from_pdf(file_path) if file_path.endswith('.pdf') else extract_text_from_docx(file_path)
    metadata = extract_metadata(text)
    keyword_density_result = keyword_density(text, job_description.split())
    score = section_score(metadata, job_description)
    requirement_match = match_requirements(text, job_requirements)
    return {
        'metadata': metadata,
        'keyword_density': keyword_density_result,
        'score': score,
        'requirement_match': requirement_match,
    }

def test_system():
    resume_path = 'Resume.pdf'
    job_description = 'Software Developer with skills in Python, Django, and API development'
    job_requirements = ['Typescript', 'Microservices', 'AWS']
    result = process_resume(resume_path, job_description, job_requirements)
    print(result)

test_system()