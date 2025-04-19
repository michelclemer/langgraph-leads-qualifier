from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from config import OPENAI_API_KEY, LLM_MODEL, APPROACH_RECOMMENDATION_TEMPLATE


class ApproachRecommender:
    """Classe para recomendar abordagens personalizadas para cada lead."""

    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model=LLM_MODEL,
            temperature=0.7
        )

    def generate_approach(self, lead_data: Dict[str, Any]) -> str:
        """Gera uma recomendação de abordagem personalizada para o lead."""
        lead = lead_data["lead"]
        qualification = lead_data["qualification"]

        prompt_template = ChatPromptTemplate.from_template(APPROACH_RECOMMENDATION_TEMPLATE)

        prompt = prompt_template.format(
            lead_info=lead.get("formatted_info", ""),
            budget_score=qualification["budget_score"],
            authority_score=qualification["authority_score"],
            need_score=qualification["need_score"],
            timeline_score=qualification["timeline_score"],
            overall_score=qualification["overall_score"],
            tier=qualification["tier"]
        )

        response = self.llm.invoke(prompt)
        return response.content