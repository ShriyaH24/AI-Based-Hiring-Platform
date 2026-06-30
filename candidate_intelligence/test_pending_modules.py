import unittest

from candidate_readiness import CandidateReadinessIndex
from skill_evidence import SkillEvidence
from growth_potential import GrowthPotential


class PendingModulesTest(unittest.TestCase):
    def setUp(self):
        self.readiness = CandidateReadinessIndex()
        self.skill_evidence = SkillEvidence()
        self.growth = GrowthPotential()

    def test_scores_are_bounded_and_structured(self):
        features = {
            "years_of_experience": 6,
            "skill_count": 8,
            "expert_skill_count": 2,
            "advanced_skill_count": 3,
            "behavior_score": 84,
            "career_length": 72,
            "average_job_duration": 18,
            "profile_completeness": 90,
            "education_count": 2,
            "certification_count": 2,
            "total_endorsements": 50,
            "avg_skill_duration": 24,
            "job_count": 4,
            "skills": ["Python", "AWS", "ML", "SQL"],
            "search_document": "Python AWS ML SQL",
            "skill_string": "Python AWS ML SQL",
            "career_title_string": "Data Scientist ML Engineer",
            "education_string": "M.Tech Computer Science",
            "certification_string": "AWS Certified",
        }

        cri = self.readiness.extract(features)
        evidence = self.skill_evidence.extract(features)
        growth = self.growth.extract(features)

        self.assertIn("cri_score", cri)
        self.assertIn("skill_evidence_score", evidence)
        self.assertIn("growth_potential_score", growth)
        self.assertTrue(0 <= cri["cri_score"] <= 100)
        self.assertTrue(0 <= evidence["skill_evidence_score"] <= 100)
        self.assertTrue(0 <= growth["growth_potential_score"] <= 100)


if __name__ == "__main__":
    unittest.main()
