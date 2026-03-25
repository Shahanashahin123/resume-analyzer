from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import clean_text

# -----------------------------
# SKILL DATABASE
# -----------------------------
skills_db = [
    "python", "machine learning", "deep learning",
    "nlp", "data science", "sql", "power bi",
    "tableau", "django", "flask", "react",
    "node js", "tensorflow", "pytorch"
]

# -----------------------------
# MATCH SCORE (WITH WEIGHTING)
# -----------------------------
def calculate_match(resume_text, jd_text):
    resume = clean_text(resume_text)
    jd = clean_text(jd_text)

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume, jd])

    base_score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    # Skill-based bonus
    important_keywords = ["python", "machine learning", "nlp", "sql"]

    bonus = 0
    for word in important_keywords:
        if word in resume and word in jd:
            bonus += 0.02

    final_score = min(base_score + bonus, 1.0)

    return final_score * 100

# -----------------------------
# SKILL MATCHING
# -----------------------------
def skill_match(resume_text):
    text = resume_text.lower()

    matched = []
    for skill in skills_db:
        if skill in text:
            matched.append(skill)

    missing = [s for s in skills_db if s not in matched]

    return matched, missing