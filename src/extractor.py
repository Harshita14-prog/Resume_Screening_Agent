import json
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

client = Groq(api_key=api_key)


def extract_resume_information(resume_text):
    """
    Extract structured information from a resume.
    The model must only use information present in the resume.
    """

    prompt = f"""
You are a resume information extraction assistant.

Extract information from the resume below.

Return ONLY valid JSON in exactly this format:

{{
    "skills": [],
    "education": [],
    "experience": []
}}

Rules:
- Use ONLY information explicitly present in the resume.
- Do not invent or infer information.
- "skills" should contain technical and professional skills.
- "education" should contain degrees, institutions, and relevant education details.
- "experience" should contain jobs, internships, projects, roles, organizations, and durations when stated.
- If a category is not present, return an empty list.
- Keep each item concise.

Resume:
{resume_text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You extract resume information accurately and return valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    # Handle possible markdown code fences
    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    try:
        return json.loads(content)

    except json.JSONDecodeError:
        raise ValueError(
            "LLM returned invalid JSON:\n" + content
        )
