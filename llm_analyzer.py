import os
from google import genai


def analyze_resume_with_llm(resume_text, job_description):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "GEMINI_API_KEY is not configured."

    client = genai.Client(
        api_key=api_key
    )

    prompt = f"""
You are an AI assistant helping analyze a resume
against a job description.

Analyze the resume and job description below.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide the analysis in this format:

STRENGTHS:
- List the relevant strengths found in the resume.

MISSING OR WEAK AREAS:
- List important skills or requirements that are
  missing or not clearly demonstrated.

SUGGESTIONS:
- Give practical suggestions to improve the resume
  for this job.

SUMMARY:
- Give a short factual summary of how the resume
  relates to the job description.

Do not make a hiring decision or recommendation.
Do not infer personal characteristics.
Only use information present in the resume and job description.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text