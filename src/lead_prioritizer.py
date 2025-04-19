from typing import Dict, Any, List
import datetime


class LeadPrioritizer:
    """Classe para priorizar leads com base na pontuação e outros fatores."""

    def __init__(self):
        self.prioritization_factors = {
            "overall_score": 0.5,
            "recency": 0.3,
            "engagement": 0.2
        }

    def calculate_recency_score(self, last_interaction: str) -> float:
        """Calcula uma pontuação baseada na recência da última interação."""
        try:
            if not last_interaction:
                return 0.0

            last_date = datetime.datetime.strptime(last_interaction, "%Y-%m-%d")
            today = datetime.datetime.now()
            days_since = (today - last_date).days

            if days_since <= 1:
                return 1.0
            elif days_since <= 7:
                return 0.8
            elif days_since <= 14:
                return 0.6
            elif days_since <= 30:
                return 0.4
            else:
                return 0.2
        except Exception:
            return 0.0

    def calculate_engagement_score(self, interactions: List[str]) -> float:
        """Calcula uma pontuação baseada no nível de engajamento."""
        if not interactions:
            return 0.0

        num_interactions = len(interactions)

        if num_interactions >= 5:
            return 1.0
        elif num_interactions >= 3:
            return 0.8
        elif num_interactions >= 2:
            return 0.6
        elif num_interactions >= 1:
            return 0.4
        else:
            return 0.0

    def prioritize_lead(self, lead: Dict[str, Any], qualification_result: Dict[str, Any]) -> Dict[str, Any]:
        """Prioriza um lead com base em múltiplos fatores."""
        recency_score = self.calculate_recency_score(lead.get("last_interaction", ""))

        engagement_score = self.calculate_engagement_score(lead.get("interactions", []))

        priority_score = (
                qualification_result["overall_score"] * self.prioritization_factors["overall_score"] +
                recency_score * self.prioritization_factors["recency"] +
                engagement_score * self.prioritization_factors["engagement"]
        )

        priority_level = "baixa"
        if priority_score >= 0.8:
            priority_level = "alta"
        elif priority_score >= 0.5:
            priority_level = "média"

        # Criar resultado de priorização
        prioritization_result = {
            "priority_score": round(priority_score, 2),
            "priority_level": priority_level,
            "factors": {
                "qualification_score": qualification_result["overall_score"],
                "recency_score": round(recency_score, 2),
                "engagement_score": round(engagement_score, 2)
            }
        }

        return prioritization_result

    def prioritize_leads(self, leads_with_qualification: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioriza uma lista de leads e os ordena por prioridade."""
        prioritized_leads = []

        for lead_data in leads_with_qualification:
            lead = lead_data["lead"]
            qualification = lead_data["qualification"]

            prioritization = self.prioritize_lead(lead, qualification)

            prioritized_lead = {
                "lead": lead,
                "qualification": qualification,
                "prioritization": prioritization
            }

            prioritized_leads.append(prioritized_lead)

        prioritized_leads.sort(key=lambda x: x["prioritization"]["priority_score"], reverse=True)

        return prioritized_leads