import json
from typing import Dict, Any, List, Annotated, TypedDict
from langgraph.graph import StateGraph, END
from operator import add

from src.lead_processor import LeadProcessor
from src.lead_qualifier import LeadQualifier
from src.lead_prioritizer import LeadPrioritizer
from src.approach_recommender import ApproachRecommender


class LeadProcessingState(TypedDict):
    leads: Annotated[List[Dict[str, Any]], add]
    processed_leads: List[Dict[str, Any]]
    qualified_leads: List[Dict[str, Any]]
    prioritized_leads: List[Dict[str, Any]]
    lead_approaches: Dict[str, str]
    current_lead_index: int
    error: str


def process_leads(state: LeadProcessingState) -> LeadProcessingState:
    """Processa os leads crus para o formato padronizado."""
    try:
        processor = LeadProcessor()
        processed_leads = []

        for lead in state["leads"]:
            normalized_lead = processor.normalize_lead_data(lead)
            formatted_info = processor.format_lead_for_analysis(normalized_lead)
            normalized_lead["formatted_info"] = formatted_info
            processed_leads.append(normalized_lead)

        state["processed_leads"] = processed_leads
        state["current_lead_index"] = 0
        return state

    except Exception as e:
        return {**state, "error": f"Erro ao processar leads: {str(e)}"}


def qualify_leads(state: LeadProcessingState) -> LeadProcessingState:
    """Qualifica os leads processados."""
    try:
        qualifier = LeadQualifier()
        qualified_leads = []

        for lead in state["processed_leads"]:
            qualification_result = qualifier.qualify_lead(lead["formatted_info"])
            qualified_leads.append({
                "lead": lead,
                "qualification": qualification_result
            })
        state["qualified_leads"] = qualified_leads

        return state

    except Exception as e:
        return {**state, "error": f"Erro ao qualificar leads: {str(e)}"}


def prioritize_leads(state: LeadProcessingState) -> LeadProcessingState:
    """Prioriza os leads qualificados."""
    try:
        prioritizer = LeadPrioritizer()
        prioritized_leads = prioritizer.prioritize_leads(state["qualified_leads"])

        state["prioritized_leads"] = prioritized_leads

        return state

    except Exception as e:
        return {**state, "error": f"Erro ao priorizar leads: {str(e)}"}


def recommend_approaches(state: LeadProcessingState) -> LeadProcessingState:
    """Recomenda abordagens personalizadas para cada lead."""
    try:
        recommender = ApproachRecommender()
        lead_approaches = {}

        for lead_data in state["prioritized_leads"]:
            lead_id = lead_data["lead"]["id"]
            approach = recommender.generate_approach(lead_data)
            lead_approaches[lead_id] = approach

        return {**state, "lead_approaches": lead_approaches}
    except Exception as e:
        return {**state, "error": f"Erro ao recomendar abordagens: {str(e)}"}


def check_errors(state: LeadProcessingState) -> str:
    """Verifica se há erros no estado."""
    if state.get("error", ""):
        return "handle_error"
    return "continue"


def handle_error(state: LeadProcessingState) -> LeadProcessingState:
    """Lida com erros no fluxo de trabalho."""
    print(f"Erro detectado: {state['error']}")
    return {**state}


def create_workflow_graph():
    """Cria o grafo de fluxo de trabalho para processamento de leads."""

    workflow = StateGraph(LeadProcessingState)

    workflow.add_node("process_leads", process_leads)
    workflow.add_node("qualify_leads", qualify_leads)
    workflow.add_node("prioritize_leads", prioritize_leads)
    workflow.add_node("recommend_approaches", recommend_approaches)
    workflow.add_node("handle_error", handle_error)

    workflow.set_entry_point("process_leads")

    workflow.add_edge("process_leads", "qualify_leads")
    workflow.add_edge("qualify_leads", "prioritize_leads")
    workflow.add_edge("prioritize_leads", "recommend_approaches")
    workflow.add_edge("recommend_approaches", END)

    workflow.add_conditional_edges(
        "process_leads",
        check_errors,
        {
            "handle_error": "handle_error",
            "continue": "qualify_leads"
        }
    )

    workflow.add_conditional_edges(
        "qualify_leads",
        check_errors,
        {
            "handle_error": "handle_error",
            "continue": "prioritize_leads"
        }
    )

    workflow.add_conditional_edges(
        "prioritize_leads",
        check_errors,
        {
            "handle_error": "handle_error",
            "continue": "recommend_approaches"
        }
    )

    workflow.add_conditional_edges(
        "recommend_approaches",
        check_errors,
        {
            "handle_error": "handle_error",
            "continue": END
        }
    )

    workflow.add_edge("handle_error", END)

    return workflow.compile()


def run_lead_qualification_system(leads_data: List[Dict[str, Any]]):
    """Executa o sistema de qualificação de leads."""

    workflow = create_workflow_graph()

    initial_state = {
        "leads": leads_data,
        "processed_leads": [],
        "qualified_leads": [],
        "prioritized_leads": [],
        "lead_approaches": {},
        "current_lead_index": -1,
        "error": ""
    }

    result = workflow.invoke(initial_state)

    return result


def save_results_to_file(result: Dict[str, Any], output_file: str):
    """Salva os resultados em um arquivo JSON."""
    output_data = {
        "prioritized_leads": []
    }

    for lead_data in result["prioritized_leads"]:
        lead_id = lead_data["lead"]["id"]
        approach = result["lead_approaches"].get(lead_id, "")

        output_data["prioritized_leads"].append({
            "id": lead_id,
            "name": lead_data["lead"]["name"],
            "company": lead_data["lead"]["company"],
            "qualification": lead_data["qualification"],
            "prioritization": lead_data["prioritization"],
            "recommended_approach": approach
        })

    with open(output_file, 'w') as file:
        json.dump(output_data, file, indent=2)

    print(f"Resultados salvos em {output_file}")


def main():
    """Função principal para executar o sistema."""
    print("Iniciando Sistema de Qualificação e Priorização de Leads...")

    lead_processor = LeadProcessor()
    leads_data = lead_processor.load_leads_from_file("data/sample_leads.json")

    if not leads_data:
        print("Nenhum lead encontrado. Verifique o arquivo de dados.")
        return

    print(f"Carregados {len(leads_data)} leads para processamento.")

    result = run_lead_qualification_system(leads_data)

    if result.get("error", ""):
        print(f"Erro durante a execução: {result['error']}")
        return

    print("\nResultados do processamento:")
    print(f"Leads processados: {len(result['processed_leads'])}")
    print(f"Leads qualificados e priorizados: {len(result['prioritized_leads'])}")

    print("\nTop 3 leads priorizados:")
    for i, lead_data in enumerate(result["prioritized_leads"][:3], 1):
        lead = lead_data["lead"]
        priority = lead_data["prioritization"]["priority_level"]
        score = lead_data["prioritization"]["priority_score"]
        print(f"{i}. {lead['name']} ({lead['company']}) - Prioridade {priority} (Score: {score})")

    save_results_to_file(result, "resultados_leads.json")


if __name__ == "__main__":
    main()
