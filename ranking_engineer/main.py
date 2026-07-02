# main.py
import pandas as pd
import re
from role_fit import calculate_role_fit
from ranking import calculate_final_score
from explainability import generate_explanation
from submission import generate_submission
# -----------------------------
# Load Candidate Data
# -----------------------------
df = pd.read_csv("data/retrieved_candidates.csv")


# -----------------------------
# Load Job Description
# -----------------------------
with open("data/job_description.txt", "r", encoding="utf-8") as file:
    jd_text = file.read().lower()


# -----------------------------
# Extract JD Skills
# -----------------------------
jd_skills = []

for line in jd_text.splitlines():

    line = line.strip()

    if line == "":
        continue

    if line in [
        "required skills",
        "preferred skills",
        "ai/ml engineer",
        "job description"
    ]:
        continue

    jd_skills.append(line)


print("\nJob Description Skills:")
print(jd_skills)


# -----------------------------
# Calculate Role Fit
# -----------------------------
role_fit_scores = []
matched_skill_list = []

for skills in df["skills"]:

    role_fit, matched_skills = calculate_role_fit(
        jd_skills,
        skills
    )

    role_fit_scores.append(role_fit)
    matched_skill_list.append(", ".join(matched_skills))


df["role_fit"] = role_fit_scores
df["matched_skills"] = matched_skill_list


# -----------------------------
# Final Score
# -----------------------------
df["final_score"] = df.apply(
    lambda row: calculate_final_score(
        row["score"],
        row["role_fit"]
    ),
    axis=1
)


# -----------------------------
# Explanation
# -----------------------------
df["explanation"] = df.apply(
    lambda row: generate_explanation(
        row["score"],
        row["role_fit"],
        row["matched_skills"].split(", ")
        if row["matched_skills"] != ""
        else []
    ),
    axis=1
)


# -----------------------------
# Sort Candidates
# -----------------------------
df = df.sort_values(
    by="final_score",
    ascending=False
)


# -----------------------------
# Save Ranked Candidates
# -----------------------------
df.to_csv(
    "ranked_candidates.csv",
    index=False
)


# -----------------------------
# Generate Submission
# -----------------------------
generate_submission(df)


# -----------------------------
# Display Top Candidates
# -----------------------------
print("\nTop 10 Candidates\n")

print(
    df[
        [
            "candidate_id",
            "score",
            "role_fit",
            "final_score",
            "matched_skills",
            "explanation"
        ]
    ].head(10)
)
print("\nRanking Completed Successfully!")