import os
import csv
import json
from parser import get_resume_text
from scorer import calculate_final_score, REQUIRED_SKILLS
from llm import generate_reasoning
from extractor import extract_resume_information


print("================================")
print("   Resume Screening Agent")
print("================================")


# -----------------------------
# File paths
# -----------------------------

resume_folder = "../data/resumes"
jd_path = "../data/job_description.txt"


# -----------------------------
# Read Job Description
# -----------------------------

with open(jd_path, "r", encoding="utf-8") as file:
    jd_text = file.read()


# -----------------------------
# Store results
# -----------------------------

results = []

    
# -----------------------------
# Process every resume
# -----------------------------

for resume_file in os.listdir(resume_folder):

    resume_path = os.path.join(
        resume_folder,
        resume_file
    )

    try:

        # Extract resume text
        resume_text = get_resume_text(
            resume_path
        )
        resume_information = extract_resume_information(
            resume_text
        )

        extracted_skills = resume_information["skills"]
        education = resume_information["education"]
        experience = resume_information["experience"]

        # Calculate scores
        final_score, similarity_score, skill_score, matched_skills = calculate_final_score(
            jd_text,
            resume_text
        )

        if final_score >= 50:
            recommendation = "SHORTLIST"
        elif final_score >= 30:
            recommendation = "CONSIDER"
        else:
            recommendation = "REJECT"
    
        missing_skills = [
            skill
            for skill in REQUIRED_SKILLS
            if skill not in matched_skills
        ]

        reasoning = generate_reasoning(
            candidate_name=resume_file,
            score=final_score,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            education=education,
            experience=experience
        )

        # Store result
        results.append({
            "candidate": resume_file,
            "nlp_similarity": similarity_score,
            "skill_match": skill_score,
            "final_score": final_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "extracted_skills": extracted_skills,
            "education": education,
            "experience": experience,
            "reasoning": reasoning,
            "recommendation": recommendation
        })

    except ValueError as error:

        print(
            f"Skipping {resume_file}: {error}"
        )


# -----------------------------
# Sort by final score
# -----------------------------

results.sort(
    key=lambda x: x["final_score"],
    reverse=True
)


# -----------------------------
# Display ranked results
# -----------------------------

print("\n================================")
print("       RANKED CANDIDATES")
print("================================")


for rank, result in enumerate(
    results,
    start=1
):

    print(
        f"\n{rank}. {result['candidate']}"
    )

    print(
        "   NLP Similarity:",
        round(
            result["nlp_similarity"],
            2
        ),
        "%"
    )

    print(
        "   Skill Match:",
        round(
            result["skill_match"],
            2
        ),
        "%"
    )

    print(
        "   Final Score:",
        round(
            result["final_score"],
            2
        ),
        "%"
    )

    print(
        "   Matched Skills:",
        ", ".join(
            result["matched_skills"]
        )
    )
    print(
        "   Missing Skills:",
        ", ".join(
            result["missing_skills"]
        )
    )
    print(
        "   Recommendation:",
        result["recommendation"]
    )
    print(
        "   Reason:",
        result["reasoning"]
    )

    # -----------------------------
# Export results
# -----------------------------

output_folder = "../output"

os.makedirs(output_folder, exist_ok=True)


# CSV output
csv_path = os.path.join(
    output_folder,
    "ranked_candidates.csv"
)


with open(
    csv_path,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "Rank",
        "Candidate",
        "NLP Similarity",
        "Skill Match",
        "Final Score",
        "Matched Skills",
        "Missing Skills",
        "Education",
        "Experience",
        "Recommendation",
        "AI Reasoning"
    ])

    for rank, result in enumerate(
        results,
        start=1
    ):

        writer.writerow([
            rank,
            result["candidate"],
            round(result["nlp_similarity"], 2),
            round(result["skill_match"], 2),
            round(result["final_score"], 2),
            ", ".join(result["matched_skills"]),
            ", ".join(result["missing_skills"]),
            "; ".join(map(str, result["education"])),
            "; ".join(map(str, result["experience"])),
            result["recommendation"],
            result["reasoning"]
        ])


# JSON output
json_path = os.path.join(
    output_folder,
    "ranked_candidates.json"
)


json_results = []

for rank, result in enumerate(
    results,
    start=1
):

    json_results.append({
        "rank": rank,
        "candidate": result["candidate"],
        "nlp_similarity": round(
            result["nlp_similarity"],
            2
        ),
        "skill_match": round(
            result["skill_match"],
            2
        ),
        "final_score": round(
            result["final_score"],
            2
        ),
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "education": result["education"],
        "experience": result["experience"],
        "recommendation": result["recommendation"],
        "reason": result["reasoning"]
    })


with open(
    json_path,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        json_results,
        file,
        indent=4
    )


print("\n================================")
print("       OUTPUT FILES")
print("================================")

print(
    "CSV:",
    csv_path
)

print(
    "JSON:",
    json_path
)


print("\n================================")
print(
    "Total resumes processed:",
    len(results)
)
print("================================")
