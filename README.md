# Resume Screening Agent

An AI-powered Resume Screening Agent that evaluates and ranks multiple candidates against a given Job Description (JD).

The agent combines deterministic NLP-based scoring with an LLM-powered analysis layer to produce a ranked shortlist, candidate reasoning, skill gaps, education, and experience.

---

## What the Agent Does

> **My agent takes a Job Description and a folder of resumes, and produces a scored, ranked shortlist with AI-generated candidate analysis.**

The agent can process multiple resumes in a single run and supports TXT, PDF, and DOCX formats.

---

## Features

* Parses TXT, PDF, and DOCX resumes

* Handles 10+ resumes in a single run

* Calculates NLP relevance using TF-IDF and cosine similarity

* Matches resumes against required skills

* Calculates a weighted final score

* Extracts skills, education, and experience using an LLM

* Generates AI-powered candidate reasoning

* Identifies matched and missing skills

* Assigns deterministic recommendations:
  * `SHORTLIST`
  * `CONSIDER`
  * `REJECT`

* Automatically ranks candidates by final score

* Exports ranked results to CSV and JSON

---

## Architecture

```text
Job Description
       |
       v
Required Skill Set
       |
       v
+-------------------+       +----------------------+
|   Resume Folder   | ----> |    Resume Parser     |
|    10+ Resumes    |       |   TXT / PDF / DOCX   |
+-------------------+       +----------------------+
             |
             v
        Resume Text
             |
      +------+------+
      |             |
      v             v
 TF-IDF + Cosine   Skill Matching
   Similarity
      |             |
      +------+------+
             |
             v
        Final Score
      70% NLP + 30%
          Skills
             |
             v
     Candidate Ranking
             |
      +------+------+
      |             |
      v             v
LLM Information   LLM Reasoning
   Extraction
      |             |
      +------+------+
             |
             v
     Candidate Analysis
             |
             v
         CSV + JSON
```
---

## Scoring Method

The numerical candidate score is deterministic and does not depend on the LLM.

### 1. NLP Similarity — 70%

The Job Description and each resume are converted into TF-IDF vectors.

Cosine similarity is then calculated between the JD and resume.

```text

NLP Score = Cosine Similarity × 100

```

### 2. Skill Match — 30%

The resume is checked against the required target skills.

```text

Skill Match =

(Number of matched skills / Total required skills) × 100

```

### 3. Final Score

```text

Final Score =

(NLP Similarity × 0.70) +

(Skill Match × 0.30)

```

Candidates are ranked in descending order of the final score.

### Current Target Skills

The current implementation checks for:

* Python

* Machine Learning

* NLP

* SQL

* REST API

* Flask

* FastAPI

* Git

The detailed scoring explanation is available in `scoring_method.md`.

---

## Recommendation Logic

The recommendation is determined programmatically from the final score.

The LLM does **not** change the numerical score or recommendation.

```text

Final Score >= 50

→ SHORTLIST

Final Score >= 30 and < 50

→ CONSIDER

Final Score < 30

→ REJECT

```

This keeps the ranking and recommendation deterministic while using the LLM for candidate analysis and explanation.

---

## LLM Analysis

The agent uses the Groq API with the `llama-3.1-8b-instant` model.

The LLM is used for two tasks:

### 1. Structured Resume Extraction

The model extracts:

```text

Skills

Education

Experience

```

from the parsed resume text.

The extraction prompt instructs the model to use only information explicitly present in the resume and return structured JSON.

### 2. Candidate Reasoning

The LLM receives:

* Candidate name

* Final score

* Matched skills

* Missing skills

* Education

* Experience

* Deterministic recommendation

It then generates:

1. Candidate assessment

2. Key strengths

3. Important skill gaps

4. Final recommendation

The model is explicitly instructed not to invent candidate information.

---

## Project Structure

```text

Resume_Screening_Agent/
│
├── data/
│   ├── job_description.txt
│   └── resumes/
│       ├── candidate_01.txt
│       ├── candidate_02.txt
│       ├── ...
│       ├── candidate_11.docx
│       └── candidate_12.pdf
│
├── output/
│   ├── ranked_candidates.csv
│   └── ranked_candidates.json
│
├── src/
│   ├── main.py
│   ├── parser.py
│   ├── scorer.py
│   ├── llm.py
│   └── extractor.py
│
├── .gitignore
├── requirements.txt
├── scoring_method.md
└── README.md
```
> `.env` is local configuration and must not be committed to GitHub.
---

## Technologies Used

* Python

* Groq API

* Llama 3.1 8B Instant

* scikit-learn

* TF-IDF

* Cosine Similarity

* pypdf

* python-docx

* python-dotenv

* CSV

* JSON

---

## Requirements

* Python 3.x

* Internet connection for Groq API calls

* A Groq API key

---

## Installation

### 1. Clone the repository

```bash

git clone https://github.com/Harshita14-prog/Resume_Screening_Agent.git

cd Resume_Screening_Agent

```

### 2. Install dependencies

```bash

pip install -r requirements.txt

```

If required, dependencies can also be installed manually:

```bash

pip install groq python-dotenv pypdf python-docx scikit-learn pandas

```

---

## Configure the API Key

Create a `.env` file in the project root:

```text

GROQ_API_KEY=your_groq_api_key_here

```

Do not commit this file to GitHub.

The `.gitignore` file contains:

```text

.env

__pycache__/

*.pyc

.venv/

venv/

```

---

## Input Data

### Job Description

Place the Job Description in:

```text

data/job_description.txt

```

### Resumes

Place candidate resumes inside:

```text

data/resumes/

```

Supported formats:

```text

.txt

.pdf

.docx

```

The system can process 10+ resumes in a single run.

---

## Running the Agent

From the project root:

```bash

cd src

python main.py

```

The agent will:

1. Load the Job Description.

2. Read all resumes from the resume folder.

3. Extract text from each resume.

4. Calculate TF-IDF and cosine similarity.

5. Calculate skill-match scores.

6. Calculate the final candidate score.

7. Extract education and experience using the LLM.

8. Identify matched and missing skills.

9. Generate AI-powered candidate reasoning.

10. Rank all candidates.

11. Export CSV and JSON results.

---

## Output

The generated files are stored in:

```text

output/

```

### CSV

```text

output/ranked_candidates.csv

```

The CSV contains:

```text

Rank

Candidate

NLP Similarity

Skill Match

Final Score

Matched Skills

Missing Skills

Education

Experience

Recommendation

AI Reasoning

```

### JSON

```text

output/ranked_candidates.json

```

The JSON contains the same information in structured form.

---

## Sample Demonstration

The repository contains a sample Job Description and 12 sample resumes in:

```text

data/job_description.txt

data/resumes/

```

Running:

```bash

cd src

python main.py

```

processes all 12 candidates in a single run.

### Sample Ranking Result

The current sample run produced:

| Rank | Candidate         | Final Score | Recommendation |
|------|-------------------|------------:|----------------|
| 1    | candidate_12.pdf  | 55.49%      | SHORTLIST      |
| 2    | candidate_01.txt  | 52.37%      | SHORTLIST      |
| 3    | candidate_08.txt  | 43.38%      | CONSIDER       |
| 4    | candidate_04.txt  | 40.18%      | CONSIDER       |
| 5    | candidate_03.txt  | 33.88%      | CONSIDER       |
| 6    | candidate_10.txt  | 32.46%      | CONSIDER       |
| 7    | candidate_05.txt  | 21.78%      | REJECT         |
| 8    | candidate_06.txt  | 16.55%      | REJECT         |
| 9    | candidate_02.txt  | 14.25%      | REJECT         |
| 10   | candidate_09.txt  | 11.18%      | REJECT         |
| 11   | candidate_07.txt  | 9.83%       | REJECT         |
| 12   | candidate_11.docx | 8.73%       | REJECT         |

**Total candidates processed: 12**

```text

SHORTLIST : 2

CONSIDER  : 4

REJECT    : 6

```

The exact output depends on the supplied Job Description and resumes.

---

## Design Decisions

### Why TF-IDF + Cosine Similarity?

TF-IDF provides a simple and interpretable way to measure textual relevance between a Job Description and a resume.

Cosine similarity measures how closely the resulting vectors align.

This approach was chosen because it is:

* Lightweight

* Fast

* Easy to reproduce

* Easy to explain

* Suitable for a 24-hour implementation

### Why Keep Numerical Scoring Deterministic?

The numerical ranking should be reproducible.

Therefore, the LLM does not determine the final score.

Instead:

```text

NLP + Skill Matching

↓

Deterministic Score

↓

Deterministic Recommendation

↓

LLM Explanation

```

This reduces the risk of an LLM changing candidate rankings unpredictably.

### Why Use an LLM?

Traditional keyword matching is useful for numerical scoring but is limited when producing candidate-level explanations.

The LLM adds an analysis layer that can structure:

* Skills

* Education

* Experience

* Strengths

* Skill gaps

* Candidate assessment

The model is instructed to use only information provided in the resume.

### Why CLI Instead of UI?

A command-line interface was intentionally chosen because the challenge prioritizes a functioning end-to-end agent over visual polish.

A web interface could be added later without changing the core screening pipeline.

---

## Tradeoffs

### TF-IDF Instead of Embeddings

TF-IDF is simpler and faster to implement, but it may miss semantic relationships.

For example, two phrases with similar meanings may receive a low similarity score if they use different vocabulary.

With more development time, sentence embeddings could improve semantic matching.

### Keyword-Based Skill Matching

The current skill matching approach checks whether predefined target skills occur in the resume.

This is transparent and easy to audit, but it can miss:

* Synonyms

* Different spellings

* Related technologies

* Skills expressed indirectly

A future version could use an embedding-based skill matcher or LLM-assisted skill normalization.

### LLM Extraction

Using an LLM makes education and experience extraction more flexible than fixed regular expressions.

However, LLM extraction introduces API dependency, latency, and the possibility of imperfect extraction.

The prompt therefore explicitly instructs the model not to invent information.

### CLI Instead of UI

The CLI keeps the project small, reproducible, and easy for reviewers to run within the challenge constraints.

A web interface could be added later.

---

## Limitations

* Skill matching currently uses a predefined target skill list.

* TF-IDF does not provide deep semantic understanding.

* LLM functionality requires an internet connection and a valid Groq API key.

* LLM extraction may occasionally require validation.

* The system is designed as a screening aid and should not be treated as an autonomous hiring decision-maker.

* Resume formatting and unusual document layouts may affect extraction quality.

---

## Future Improvements

With additional development time, the agent could be improved with:

* Sentence-transformer embeddings

* Dynamic skill extraction from the Job Description

* Better synonym and skill normalization

* More robust resume section detection

* Experience-duration calculation

* Education-level comparison

* Configurable scoring weights

* Human-review flags for uncertain cases

* Web interface for uploading resumes

* Persistent candidate database

* Automated evaluation benchmarks

---

## Responsible Use

This system is intended as a resume screening and ranking aid.

Recruitment decisions can involve sensitive and consequential information. The output should therefore be reviewed by a human recruiter rather than being used as the sole basis for employment decisions.

---

## Summary

### Project Workflow

This project demonstrates an end-to-end AI-assisted resume screening pipeline:

```text
Job Description + 12 Resumes
            ↓
      Document Parsing
            ↓
   NLP + Skill Matching
            ↓
   Candidate Scoring
            ↓
    Candidate Ranking
            ↓
      AI Reasoning
            ↓
        CSV + JSON

```

The design prioritizes reproducibility, explainability, and a clear separation between deterministic ranking and LLM-generated analysis.
