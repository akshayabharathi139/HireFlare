# utils/data_utils.py

# In-memory candidate storage (you can later connect this to a DB or CSV)
candidates_db = []

def insert_candidate(name, match_score, resume_text, email):
    candidate = {
        "name": name,
        "score": match_score,
        "resume": resume_text,
        "email": email
    }

    # Avoid inserting duplicates
    if not any(c['name'] == name and c['email'] == email for c in candidates_db):
        candidates_db.append(candidate)

def get_all_candidates():
    return candidates_db

def get_selected_candidates(threshold=60):
    return [c for c in candidates_db if c['score'] >= threshold]

def clear_candidates():
    candidates_db.clear()
