from typing import Any, Dict


class GrowthPotential:
    """Estimate future growth potential from career trajectory and engagement signal strength."""

    def extract(self, features: Dict[str, Any]) -> Dict[str, float]:
        """Return a bounded growth potential score in the 0-100 range."""
        career_length = self._to_float(features.get("career_length", 0))
        job_count = self._to_float(features.get("job_count", 0))
        education_count = self._to_float(features.get("education_count", 0))
        certification_count = self._to_float(features.get("certification_count", 0))
        skill_count = self._to_float(features.get("skill_count", 0))
        expert_skill_count = self._to_float(features.get("expert_skill_count", 0))
        advanced_skill_count = self._to_float(features.get("advanced_skill_count", 0))
        behavior_score = self._to_float(features.get("behavior_score", 0))

        trajectory_component = self._clamp((career_length / 36.0) * 12.0, 0, 100)
        mobility_component = self._clamp(job_count * 8.0, 0, 100)
        education_component = self._clamp((education_count * 15.0) + (certification_count * 8.0), 0, 100)
        skill_diversity_component = self._clamp((skill_count * 4.0) + (expert_skill_count * 6.0) + (advanced_skill_count * 4.0), 0, 100)
        behavior_component = self._clamp(behavior_score * 0.8, 0, 100)

        growth_potential_score = (
            0.25 * trajectory_component
            + 0.20 * mobility_component
            + 0.20 * education_component
            + 0.20 * skill_diversity_component
            + 0.15 * behavior_component
        )

        return {"growth_potential_score": round(self._clamp(growth_potential_score, 0, 100), 1)}

    @staticmethod
    def _to_float(value: Any) -> float:
        try:
            return float(value or 0)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _clamp(value: float, lower: float, upper: float) -> float:
        return max(lower, min(upper, value))
