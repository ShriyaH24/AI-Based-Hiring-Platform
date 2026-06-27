class FeatureExtractor:

    def extract(self, candidate):
        # Part A — Profile Features
        profile = candidate["profile"]
        features = {
            "candidate_id": candidate["candidate_id"],
            "headline": profile["headline"],
            "summary": profile["summary"],
            "location": profile["location"],
            "country": profile["country"],
            "years_of_experience": profile["years_of_experience"],
            "current_title": profile["current_title"],
            "current_company": profile["current_company"],
            "industry": profile["current_industry"],
            "company_size": profile["current_company_size"]
        }

        # Part B — Skills
        skills = candidate["skills"]
        features["skills"] = [s["name"] for s in skills]
        features["skill_count"] = len(skills)
        features["expert_skill_count"] = sum(1 for s in skills if s["proficiency"] == "expert")
        features["advanced_skill_count"] = sum(1 for s in skills if s["proficiency"] == "advanced")
        features["total_endorsements"] = sum(s["endorsements"] for s in skills)
        features["avg_skill_duration"] = (
            sum(s.get("duration_months", 0) for s in skills) / len(skills)
            if skills else 0
        )

        # Part C — Career
        career = candidate["career_history"]
        features["job_count"] = len(career)
        features["career_length"] = sum(job["duration_months"] for job in career)
        features["current_job_duration"] = max(
            [j["duration_months"] for j in career if j["is_current"]],
            default=0
        )
        features["average_job_duration"] = (
            features["career_length"] / len(career) if career else 0
        )

        # Part D — Education
        education = candidate["education"]
        features["education_count"] = len(education)
        features["highest_degree"] = (
            education[-1]["degree"] if education else ""
        )

        # Part E — Certifications
        features["certification_count"] = len(candidate["certifications"])

        # Part F — Search Text
        career_text = " ".join(job["description"] for job in career)
        skill_text = " ".join(features["skills"])
        features["search_document"] = " ".join([
            features["headline"],
            features["summary"],
            skill_text,
            career_text
        ])

        # === NEW STEP 1 EXTENSIONS ===
        # 1.1 skill_string
        features["skill_string"] = " ".join(features["skills"])

        # 1.2 career_title_string
        career_titles = [job["title"] for job in candidate.get("career_history", [])]
        features["career_title_string"] = " ".join(career_titles)

        # 1.3 education_string
        education_parts = []
        for edu in candidate.get("education", []):
            education_parts.extend([
                edu.get("degree", ""),
                edu.get("field_of_study", ""),
                edu.get("institution", "")
            ])
        features["education_string"] = " ".join(education_parts)

        # 1.4 certification_string
        features["certification_string"] = " ".join(
            cert.get("name", "") for cert in candidate.get("certifications", [])
        )

        return features