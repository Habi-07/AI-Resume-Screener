from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text, job_description):

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        [resume_text, job_description]
    )

    similarity_score = cosine_similarity(
        vectors[0],
        vectors[1]
    )[0][0]

    return similarity_score


def calculate_skill_match(resume_skills, job_skills):

    if not job_skills:
        return 0

    matched_skills = set(resume_skills).intersection(
        set(job_skills)
    )

    skill_match = (
        len(matched_skills) / len(set(job_skills))
    )

    return skill_match


def calculate_final_score(
    similarity_score,
    skill_match
):

    final_score = (
        (similarity_score * 100 * 0.30)
        +
        (skill_match * 100 * 0.70)
    )

    return round(final_score, 2)