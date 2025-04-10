import os
import re
import numpy as np
from utils.data_utils import insert_candidate, get_all_candidates, get_selected_candidates, clear_candidates
from langchain.embeddings import OllamaEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

# Initialize embeddings
embeddings = OllamaEmbeddings(model="mxbai-embed-large", base_url="http://localhost:11434")

# Extract relevant parts of the job description
def extract_relevant_sections(text):
    lines = text.split('\n')
    relevant_keywords = ['qualification', 'experience', 'skill', 'requirement']
    relevant_sections = [line for line in lines if any(kw in line.lower() for kw in relevant_keywords)]
    return "\n".join(relevant_sections) if relevant_sections else text

# Extract email from resume
def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else None

# Soft bonus scoring for keyword overlap
def keyword_bonus_loose(jd_text, resume_text):
    keywords = ['python', 'sql', 'cloud', 'diploma', 'machine learning', 'java', 'frontend', 'backend']
    jd_text_lower = jd_text.lower()
    resume_text_lower = resume_text.lower()
    matches = sum(1 for kw in keywords if kw in jd_text_lower and kw in resume_text_lower)
    return min(matches * 0.6, 2.5)  # Slightly higher weight and cap

def get_match_score(jd_text, resume_text):
    relevant_jd = extract_relevant_sections(jd_text)
    jd_keywords = set(relevant_jd.lower().split())

    resume_chunks = [
        chunk.strip() for chunk in resume_text.split('\n')
        if len(chunk.strip()) > 65 and any(word in chunk.lower() for word in jd_keywords)  # Looser threshold
    ]

    if not resume_chunks:
        return 0.0

    jd_vec = np.array(embeddings.embed_query(relevant_jd)).reshape(1, -1)
    scores = [
        cosine_similarity(jd_vec, np.array(embeddings.embed_query(chunk)).reshape(1, -1))[0][0]
        for chunk in resume_chunks
    ]

    top_scores = sorted(scores, reverse=True)[:3]
    base_score = (sum(top_scores) / len(top_scores)) * 100

    # Keyword bonus
    base_score += keyword_bonus_loose(jd_text, resume_text)

    # Reduced penalty for fewer chunks
    if len(resume_chunks) < 3:
        base_score -= 1.0

    return max(0.0, min(round(base_score, 2), 100.0))


# Class to handle recruiting logic
class RecruitingAgent:
    def __init__(self, cv_folder):
        self.cv_folder = cv_folder

    def extract_and_score(self, jd_summary, score_threshold=90):
        candidates = []
        for filename in os.listdir(self.cv_folder):
            if filename.endswith(".txt"):
                with open(os.path.join(self.cv_folder, filename), "r", encoding="utf-8") as f:
                    resume_text = f.read()
                    match_score = get_match_score(jd_summary, resume_text)
                    name = filename.replace(".txt", "")
                    email = extract_email(resume_text)

                    if match_score >= score_threshold:
                        insert_candidate(name, match_score, resume_text, email)
                        candidates.append({
                            "name": name,
                            "match": match_score,
                            "resume": resume_text,
                            "email": email
                        })
        return candidates


