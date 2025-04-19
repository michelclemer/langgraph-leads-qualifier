from typing import Dict, Any, List, Tuple
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
import json

from config import OPENAI_API_KEY, LLM_MODEL, QUALIFICATION_CRITERIA, LEAD_ANALYSIS_TEMPLATE, LEAD_TIERS


class LeadQualifier:
    """Classe para qualificar leads com base nos critérios BANT."""

    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model=LLM_MODEL,
            temperature=0.2
        )
        self.setup_output_parser()

    def setup_output_parser(self):
        """Configura o parser de saída estruturada para o LLM."""
        response_schemas = [
            ResponseSchema(name="budget", description="Pontuação de orçamento de 0 a 1", type="number"),
            ResponseSchema(name="authority", description="Pontuação de autoridade de 0 a 1", type="number"),
            ResponseSchema(name="need", description="Pontuação de necessidade de 0 a 1", type="number"),
            ResponseSchema(name="timeline", description="Pontuação de prazo de 0 a 1", type="number"),
            ResponseSchema(name="reasoning", description="Raciocínio detalhado para cada pontuação", type="string"),
        ]
        self.output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        self.format_instructions = self.output_parser.get_format_instructions()

    def qualify_lead(self, lead_info: str) -> Dict[str, Any]:
        """Qualifica um lead com base nas informações fornecidas."""
        prompt_template = ChatPromptTemplate.from_template(
            LEAD_ANALYSIS_TEMPLATE + "\n{format_instructions}"
        )

        prompt = prompt_template.format(
            lead_info=lead_info,
            format_instructions=self.format_instructions
        )

        response = self.llm.invoke(prompt)

        try:
            parsed_response = self.output_parser.parse(response.content)

            overall_score = (
                    parsed_response["budget"] * QUALIFICATION_CRITERIA["budget"]["weight"] +
                    parsed_response["authority"] * QUALIFICATION_CRITERIA["authority"]["weight"] +
                    parsed_response["need"] * QUALIFICATION_CRITERIA["need"]["weight"] +
                    parsed_response["timeline"] * QUALIFICATION_CRITERIA["timeline"]["weight"]
            )

            tier = "cold"
            for tier_name, threshold in sorted(LEAD_TIERS.items(), key=lambda x: x[1], reverse=True):
                if overall_score >= threshold:
                    tier = tier_name
                    break

            result = {
                "budget_score": parsed_response["budget"],
                "authority_score": parsed_response["authority"],
                "need_score": parsed_response["need"],
                "timeline_score": parsed_response["timeline"],
                "reasoning": parsed_response["reasoning"],
                "overall_score": round(overall_score, 2),
                "tier": tier
            }

            return result

        except Exception as e:
            print(f"Erro ao analisar a resposta: {e}")
            return {
                "budget_score": 0,
                "authority_score": 0,
                "need_score": 0,
                "timeline_score": 0,
                "reasoning": f"Erro na análise: {str(e)}",
                "overall_score": 0,
                "tier": "cold"
            }

    def check_qualification_thresholds(self, scores: Dict[str, float]) -> List[str]:
        """Verifica quais critérios não atingiram o limiar mínimo."""
        below_threshold = []

        for criterion, details in QUALIFICATION_CRITERIA.items():
            score_key = f"{criterion}_score"
            if score_key in scores and scores[score_key] < details["threshold"]:
                below_threshold.append(criterion)

        return below_threshold