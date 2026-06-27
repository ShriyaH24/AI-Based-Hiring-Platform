import json

from parser import load_candidates
from validator import CandidateValidator


schema = json.load(open("data/candidate_schema.json"))

validator = CandidateValidator(schema)

for candidate in load_candidates("data/candidates.jsonl"):

    validator.validate_candidate(candidate)

print("Validation Passed")