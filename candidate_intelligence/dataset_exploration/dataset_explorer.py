import json
import os
from pprint import pprint

# Define default paths relative to the project root
SCHEMA_PATH = "data/candidate_schema.json"
SAMPLE_PATH = "data/sample_candidates.json"
DATASET_PATH = "data/candidates.jsonl"
OUTPUT_PATH = "output/dataset_summary.json"


def explore_schema(schema_path=SCHEMA_PATH):
    """Loads and prints the schema structure, required fields, and full nested property tree."""
    if not os.path.exists(schema_path):
        print(f"[Warning] Schema file not found at {schema_path}")
        return None

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    print("=" * 80)
    print("TOP LEVEL REQUIRED FIELDS")
    print("=" * 80)
    pprint(schema.get("required", []))
    print("\n")

    print("=" * 80)
    print("TOP LEVEL PROPERTIES")
    print("=" * 80)
    for key in schema.get("properties", {}):
        print(key)
    print("\n")

    def print_schema_tree(properties, indent=0):
        """Recursive helper to map nested dict and array schemas."""
        for key, value in properties.items():
            print("    " * indent + f"- {key}")
            if isinstance(value, dict):
                if "properties" in value:
                    print_schema_tree(value["properties"], indent + 1)
                elif value.get("type") == "array":
                    items = value.get("items", {})
                    if "properties" in items:
                        print_schema_tree(items["properties"], indent + 1)

    print("=" * 80)
    print("COMPLETE SCHEMA TREE")
    print("=" * 80)
    if "properties" in schema:
        print_schema_tree(schema["properties"])
    print("\n")
    
    return schema


def explore_sample_candidates(sample_path=SAMPLE_PATH):
    """Loads sample JSON candidates and performs detailed breakdowns of the first candidate."""
    if not os.path.exists(sample_path):
        print(f"[Warning] Sample file not found at {sample_path}")
        return

    with open(sample_path, "r", encoding="utf-8") as f:
        candidates = json.load(f)

    print("=" * 80)
    print(f"SAMPLE CANDIDATES EXPLORATION (Total: {len(candidates)})")
    print("=" * 80)

    if not candidates:
        print("Sample file is empty.")
        return

    candidate = candidates[0]
    print(f"First Candidate Top-Level Keys:\n{list(candidate.keys())}\n")

    print("--- Full Candidate Pretty Print ---")
    pprint(candidate)
    print("\n")

    # Nested Section: Profile Summary
    if "profile" in candidate:
        print("-" * 50)
        print("PROFILE SUMMARY")
        print("-" * 50)
        for k, v in candidate["profile"].items():
            print(f"{k}: {v}")
        print("\n")

    # Nested Section: Career History
    if "career_history" in candidate:
        career = candidate["career_history"]
        print("-" * 50)
        print(f"CAREER HISTORY (Jobs: {len(career)})")
        print("-" * 50)
        for i, job in enumerate(career):
            print(f"Job {i+1}:")
            for k, v in job.items():
                print(f"  {k}: {v}")
        print("\n")

    # Nested Section: Skills
    if "skills" in candidate:
        print("-" * 50)
        print(f"SKILLS (Total: {len(candidate['skills'])})")
        print("-" * 50)
        for skill in candidate["skills"]:
            print(skill)
        print("\n")

    # Nested Section: Education
    if "education" in candidate:
        print("-" * 50)
        print("EDUCATION")
        print("-" * 50)
        for edu in candidate["education"]:
            pprint(edu)
        print("\n")

    # Nested Section: Certifications
    if "certifications" in candidate:
        print("-" * 50)
        print("CERTIFICATIONS")
        print("-" * 50)
        print(candidate["certifications"])
        print("\n")

    # Nested Section: Languages
    if "languages" in candidate:
        print("-" * 50)
        print("LANGUAGES")
        print("-" * 50)
        for lang in candidate["languages"]:
            pprint(lang)
        print("\n")

    # Nested Section: Redrob Signals
    if "redrob_signals" in candidate:
        print("-" * 50)
        print("REDROB SIGNALS")
        print("-" * 50)
        for k, v in candidate["redrob_signals"].items():
            print(f"{k}: {v}")
        print("\n")


def explore_dataset_statistics(dataset_path=DATASET_PATH, output_path=OUTPUT_PATH):
    """Streams the full JSONL file to compute matrix statistics and exports a JSON summary."""
    if not os.path.exists(dataset_path):
        print(f"[Warning] Full dataset JSONL not found at {dataset_path}")
        return

    count = 0
    skill_names = set()
    countries = set()
    titles = set()
    industries = set()
    degrees = set()

    with open(dataset_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            candidate = json.loads(line)
            count += 1

            # Extract Profile Stats
            profile = candidate.get("profile", {})
            if "country" in profile: countries.add(profile["country"])
            if "current_title" in profile: titles.add(profile["current_title"])
            if "current_industry" in profile: industries.add(profile["current_industry"])

            # Extract Education Stats
            for edu in candidate.get("education", []):
                if "degree" in edu:
                    degrees.add(edu["degree"])

            # Extract Skills Stats
            for skill in candidate.get("skills", []):
                if "name" in skill:
                    skill_names.add(skill["name"])

    print("=" * 80)
    print("FULL DATASET SUMMARY STATISTICS")
    print("=" * 80)
    print(f"Total Candidates: {count}")
    print(f"Unique Countries: {len(countries)}")
    print(f"Unique Job Titles: {len(titles)}")
    print(f"Unique Industries: {len(industries)}")
    print(f"Unique Degrees   : {len(degrees)}")
    print(f"Unique Skills    : {len(skill_names)}")
    print("\n")

    # Save to file
    summary_data = {
        "num_candidates": count,
        "countries": sorted(list(countries)),
        "job_titles": sorted(list(titles)),
        "industries": sorted(list(industries)),
        "degrees": sorted(list(degrees)),
        "skills": sorted(list(skill_names))
    }

    # Ensure output directory exists before writing
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as out_f:
        json.dump(summary_data, out_f, indent=4)
    print(f"[Success] Metric summary exported to {output_path}\n")


if __name__ == "__main__":
    print("Starting Dataset Exploration Workflow...\n")
    
    # 1. Look over schema definitions
    explore_schema()
    
    # 2. Extract context details on specific subsets
    explore_sample_candidates()
    
    # 3. Stream through data pipeline and track high-level footprints
    explore_dataset_statistics()
    
    print("Exploration Complete.")