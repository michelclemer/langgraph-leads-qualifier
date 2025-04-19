import json
from typing import Dict, Any, List


class LeadProcessor:
    """Classe para processar e normalizar dados de leads de diferentes fontes."""

    def __init__(self):
        pass

    def load_leads_from_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Carrega leads de um arquivo JSON."""
        try:
            with open(file_path, 'r') as file:
                leads = json.load(file)
            return leads
        except Exception as e:
            print(f"Erro ao carregar leads: {e}")
            return []

    def normalize_lead_data(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        """Normaliza os dados do lead para um formato consistente."""
        normalized_lead = {
            "id": lead.get("id", ""),
            "name": lead.get("name", ""),
            "company": lead.get("company", ""),
            "position": lead.get("position", ""),
            "email": lead.get("email", ""),
            "phone": lead.get("phone", ""),
            "source": lead.get("source", "unknown"),
            "last_interaction": lead.get("last_interaction", ""),
            "interactions": lead.get("interactions", []),
            "company_size": lead.get("company_size", "unknown"),
            "industry": lead.get("industry", "unknown"),
            "budget_info": lead.get("budget_info", ""),
            "decision_maker": lead.get("is_decision_maker", False),
            "needs": lead.get("needs", ""),
            "timeline": lead.get("timeline", ""),
            "additional_notes": lead.get("notes", "")
        }
        return normalized_lead

    def format_lead_for_analysis(self, lead: Dict[str, Any]) -> str:
        """Formata os dados do lead para análise pelo LLM."""
        lead_info = f"""
            Nome: {lead['name']}
            Empresa: {lead['company']}
            Cargo: {lead['position']}
            Tamanho da empresa: {lead['company_size']}
            Indústria: {lead['industry']}
            Fonte do lead: {lead['source']}
            Última interação: {lead['last_interaction']}
            Histórico de interações: {'; '.join(lead['interactions']) if lead['interactions'] else 'Nenhuma'}
            Informações sobre orçamento: {lead['budget_info']}
            Tomador de decisão: {'Sim' if lead['decision_maker'] else 'Não'}
            Necessidades: {lead['needs']}
            Prazo: {lead['timeline']}
            Notas adicionais: {lead['additional_notes']}
            """
        return lead_info.strip()