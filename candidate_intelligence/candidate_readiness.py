from typing import Any, Dict


class CandidateReadinessIndex:
    """Compute a bounded readiness score from existing profile and behavior signals."""

    def extract(self, features: Dict[str, Any]) -> Dict[str, float]:
        """Return a candidate readiness index in the 0-100 range."""
        years_of_experience = self._to_float(features.get("years_of_experience", 0))
        skill_count = self._to_float(features.get("skill_count", 0))
        expert_skill_count = self._to_float(features.get("expert_skill_count", 0))
        advanced_skill_count = self._to_float(features.get("advanced_skill_count", 0))
        behavior_score = self._to_float(features.get("behavior_score", 0))
        career_length = self._to_float(features.get("career_length", 0))
        average_job_duration = self._to_float(features.get("average_job_duration", 0))
        profile_completeness = self._to_float(features.get("profile_completeness", 0))
        education_count = self._to_float(features.get("education_count", 0))
        certification_count = self._to_float(features.get("certification_count", 0))

        experience_component = self._clamp(years_of_experience * 10.0, 0, 100)
        skill_component = self._clamp(
            (skill_count * 6.0) + (expert_skill_count * 10.0) + (advanced_skill_count * 6.0),
            0,
            100,
        )
        behavior_component = self._clamp(behavior_score, 0, 100)
        career_component = self._clamp((career_length / 24.0) * 10.0, 0, 100)
        stability_component = self._clamp((average_job_duration / 12.0) * 10.0, 0, 100)
        profile_component = self._clamp(profile_completeness, 0, 100)
        education_component = self._clamp((education_count * 20.0) + (certification_count * 10.0), 0, 100)

        cri_score = (
            (0.20 * experience_component)
            + (0.20 * skill_component)
            + (0.15 * behavior_component)
            + (0.15 * career_component)
            + (0.10 * stability_component)
            + (0.10 * profile_component)
            + (0.10 * education_component)
        )

        return {"cri_score": round(self._clamp(cri_score, 0, 100), 1)}

    @staticmethod
    def _to_float(value: Any) -> float:
        try:
            return float(value or 0)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _clamp(value: float, lower: float, upper: float) -> float:
        return max(lower, min(upper, value))
