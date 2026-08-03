# Resume_Screening_Agent

An NLP-based Resume Screening Agent that ranks multiple candidates against a Job Description.

## Features

- Parses TXT, PDF, and DOCX resumes
- Handles 10+ resumes in a single run
- Calculates NLP similarity using TF-IDF and cosine similarity
- Matches resumes against target skills
- Calculates a weighted final score
- Ranks candidates automatically
- Generates simple explanations for each candidate
- Exports results to CSV and JSON

## Project Structure

Resume_Screening_Agent/

├── data/
│   ├── job_description.txt
│   └── resumes/
├── src/
│   ├── main.py
│   ├── parser.py
│   └── scorer.py
├── output/
│   ├── ranked_candidates.csv
│   └── ranked_candidates.json
├── scoring_method.md
└── README.md

## Technologies Used

- Python
- TF-IDF
- Cosine Similarity
- pypdf
- python-docx
- scikit-learn

## How to Run

### 1. Install dependencies

```bash
pip install pypdf python-docx scikit-learn pandas
