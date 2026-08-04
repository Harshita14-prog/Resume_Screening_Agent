import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

client = Groq(api_key=api_key)


def generate_reasoning(
    candidate_name,
    score,
    matched_skills,
    missing_skills,
    education,
    experience
):
    """
    Generate evidence-based candidate reasoning using the LLM.
    The numerical score and recommendation remain deterministic.
    """

    if score >= 50:
        recommendation = "SHORTLIST"
    elif score >= 30:
        recommendation = "CONSIDER"
    else:
        recommendation = "REJECT"

    prompt = f"""
You are an AI Resume Screening Assistant.

Analyze the candidate using ONLY the information provided below.

Candidate: {candidate_name}
Overall Score: {score:.2f}%

Matched Skills:
{", ".join(matched_skills) if matched_skills else "None"}

Missing Skills:
{", ".join(missing_skills) if missing_skills else "None"}

Education:
{str(education) if education else "Not provided"}

Experience:
{str(experience) if experience else "Not provided"}

The deterministic screening system has assigned this recommendation:

{recommendation}

Write a concise professional assessment containing:

1. Candidate assessment
2. Key strengths
3. Important skill gaps
4. Final recommendation

IMPORTANT RULES:
- Do not change the recommendation.
- Do not invent experience, education, skills, employers, dates, or qualifications.
- Use only the information provided above.
- Do not claim information that is not explicitly provided.
- Keep the assessment concise.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful, evidence-based resume screening "
                    "assistant. Never invent candidate information."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content
