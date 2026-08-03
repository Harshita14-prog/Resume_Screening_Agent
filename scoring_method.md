# Resume Screening Agent — Scoring Method

## Overview

The Resume Screening Agent ranks candidates by comparing their resumes against a given Job Description (JD).

The system combines NLP-based text similarity with explicit skill matching to produce a final candidate score.

## Scoring Formula

The final score is calculated as:

Final Score = (NLP Similarity × 0.70) + (Skill Match × 0.30)

### 1. NLP Similarity — 70%

TF-IDF (Term Frequency–Inverse Document Frequency) is used to convert the Job Description and resume into numerical vectors.

Cosine similarity is then calculated between the two vectors.

This measures how similar the resume content is to the Job Description.

### 2. Skill Match — 30%

The system maintains a list of skills relevant to the Job Description:

- Python
- Machine Learning
- NLP
- SQL
- REST API
- Flask
- FastAPI
- Git

The skill match percentage is calculated as:

Skill Match = (Matched Skills / Total Target Skills) × 100

For example, if a candidate matches 6 out of 8 target skills:

Skill Match = (6 / 8) × 100 = 75%

## Candidate Ranking

After calculating the final score for every resume, candidates are sorted in descending order.

The candidate with the highest final score receives Rank 1.

## Reasoning

For each candidate, the system reports:

- NLP similarity score
- Skill match score
- Final score
- Matched skills
- A short rule-based explanation

## Supported Resume Formats

The system supports:

- TXT
- PDF
- DOCX

## Limitations

The current system uses keyword-based skill matching and TF-IDF similarity.

It does not yet perform advanced semantic understanding of skills, job titles, or work experience.

For production use, the system could be extended with embeddings, better skill normalization, experience extraction, and education matching.