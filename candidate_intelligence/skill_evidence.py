from typing import Any, Dict, List


class SkillEvidence:
    """Estimate how well a candidate's skills are supported by available evidence."""

    def extract(self, features: Dict[str, Any]) -> Dict[str, float]:
        """Return a bounded skill evidence score based on duration, endorsements, and text evidence."""
        skill_count = self._to_float(features.get("skill_count", 0))
        total_endorsements = self._to_float(features.get("total_endorsements", 0))
        avg_skill_duration = self._to_float(features.get("avg_skill_duration", 0))
        years_of_experience = self._to_float(features.get("years_of_experience", 0))
        search_document = str(features.get("search_document", "") or "")
        skill_string = str(features.get("skill_string", "") or "")
        career_title_string = str(features.get("career_title_string", "") or "")
        education_string = str(features.get("education_string", "") or "")
        certification_string = str(features.get("certification_string", "") or "")

        evidence_strength = 0.0
        evidence_strength += min(skill_count * 5.0, 30.0)
        evidence_strength += min(total_endorsements / 5.0, 25.0)
        evidence_strength += min(avg_skill_duration / 6.0, 20.0)
        evidence_strength += min(years_of_experience * 2.0, 15.0)

        text_evidence = self._count_matches(search_document, skill_string, career_title_string, education_string, certification_string)
        evidence_strength += min(text_evidence * 2.0, 10.0)

        return {"skill_evidence_score": round(self._clamp(evidence_strength, 0, 100), 1)}

    @staticmethod
    def _count_matches(*values: str) -> int:
        total = 0
        for value in values:
            if value:
                total += 1
        return total

    @staticmethod
    def _to_float(value: Any) -> float:
        try:
            return float(value or 0)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _clamp(value: float, lower: float, upper: float) -> float:
        return max(lower, min(upper, value))
