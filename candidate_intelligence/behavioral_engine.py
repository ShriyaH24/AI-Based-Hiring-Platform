class BehavioralEngine:

    def extract(self, candidate):
        signals = candidate["redrob_signals"]

        # Calculate weighted compliance matrix scores
        score = 0.0
        score += signals.get("profile_completeness_score", 0) * 0.20
        score += signals.get("recruiter_response_rate", 0) * 100 * 0.20
        score += signals.get("interview_completion_rate", 0) * 100 * 0.15
        
        github = signals.get("github_activity_score", 0)
        score += github if github > 0 else 0
        
        score += min(signals.get("saved_by_recruiters_30d", 0), 20) * 2
        score += min(signals.get("search_appearance_30d", 0), 100) * 0.2

        if signals.get("verified_email"):
            score += 5
        if signals.get("verified_phone"):
            score += 5
        if signals.get("open_to_work_flag"):
            score += 10

        # Enforce ceiling limit cap boundary
        behavior_score = min(score, 100)

        # Return aggregated array with raw values
        return {
            "profile_completeness": signals["profile_completeness_score"],
            "response_rate": signals["recruiter_response_rate"],
            "response_time": signals["avg_response_time_hours"],
            "open_to_work": signals["open_to_work_flag"],
            "github_score": signals["github_activity_score"],
            "interview_completion": signals["interview_completion_rate"],
            "offer_acceptance": signals["offer_acceptance_rate"],
            "profile_views": signals["profile_views_received_30d"],
            "search_appearances": signals["search_appearance_30d"],
            "saved_by_recruiters": signals["saved_by_recruiters_30d"],
            "endorsements_received": signals["endorsements_received"],
            "notice_period": signals["notice_period_days"],
            "behavior_score": behavior_score  
        }