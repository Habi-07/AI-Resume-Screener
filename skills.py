SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "html",
    "css",
    "javascript",
    "js",
    "react",
    "react.js",
    "node.js",
    "node",
    "django",
    "flask",
    "fastapi",
    "git",
    "github",
    "machine learning",
    "ml",
    "deep learning",
    "artificial intelligence",
    "ai",
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy",
    "scikit-learn",
    "power bi",
    "tableau",
    "excel",
    "mongodb",
    "mysql",
    "postgresql",
    "aws",
    "azure",
    "docker"
]


def extract_skills(text):
    """
    Extract skills from resume or job description text.
    """
    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    return list(set(found_skills))


def compare_skills(resume_skills, job_skills):
    """
    Compare resume skills with job description skills.
    """

    resume_skills = set(skill.lower() for skill in resume_skills)
    job_skills = set(skill.lower() for skill in job_skills)

    matched_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills - resume_skills

    return list(matched_skills), list(missing_skills)