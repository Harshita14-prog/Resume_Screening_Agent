from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Skills required/preferred by the Job Description
REQUIRED_SKILLS = [
    "python",
    "machine learning",
    "nlp",
    "sql",
    "rest api",
    "flask",
    "fastapi",
    "git"
]


def calculate_similarity(jd_text, resume_text):
    """
    Calculate NLP similarity using TF-IDF
    and cosine similarity.
    """

    documents = [jd_text, resume_text]

    vectorizer = TfidfVectorizer(stop_words="english")

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return similarity * 100


def calculate_skill_match(resume_text):
    """
    Calculate how many required skills
    appear in the resume.
    """

    resume_text = resume_text.lower()

    matched_skills = []

    for skill in REQUIRED_SKILLS:

        if skill in resume_text:
            matched_skills.append(skill)

    skill_score = (
        len(matched_skills) / len(REQUIRED_SKILLS)
    ) * 100

    return skill_score, matched_skills


def calculate_final_score(jd_text, resume_text):
    """
    Combine NLP similarity and skill matching.
    """

    similarity_score = calculate_similarity(
        jd_text,
        resume_text
    )

    skill_score, matched_skills = calculate_skill_match(
        resume_text
    )

    final_score = (
        similarity_score * 0.70
        + skill_score * 0.30
    )

    return final_score, similarity_score, skill_score, matched_skills

def generate_reasoning(
    final_score,
    skill_score,
    matched_skills
):
    """
    Generate a simple explanation for the candidate score.
    """

    skill_count = len(matched_skills)

    if final_score >= 50:
        level = "Strong match"

    elif final_score >= 30:
        level = "Moderate match"

    elif final_score >= 15:
        level = "Weak match"

    else:
        level = "Poor match"

    if skill_count > 0:

        skills_text = ", ".join(matched_skills)

        reason = (
            f"{level} for the Junior AI Developer role. "
            f"Matched {skill_count} target skill(s): "
            f"{skills_text}. "
            f"Skill match score: {skill_score:.2f}%."
        )

    else:

        reason = (
            f"{level} for the Junior AI Developer role. "
            "No target skills were detected in the resume."
        )

    return reason
