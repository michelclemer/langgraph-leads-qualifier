import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do modelo de linguagem
LLM_MODEL = "gpt-4o"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Critérios de qualificação
QUALIFICATION_CRITERIA = {
    "budget": {
        "weight": 0.25,
        "threshold": 0.6
    },
    "authority": {
        "weight": 0.25,
        "threshold": 0.7
    },
    "need": {
        "weight": 0.3,
        "threshold": 0.6
    },
    "timeline": {
        "weight": 0.2,
        "threshold": 0.5
    }
}

# Pontuações mínimas para cada categoria de lead
LEAD_TIERS = {
    "hot": 0.8,
    "warm": 0.6,
    "cold": 0.4
}

# Template para análise de lead
LEAD_ANALYSIS_TEMPLATE = """
Analise as informações deste lead e avalie os critérios BANT (Budget, Authority, Need, Timeline).
Informações do Lead:
{lead_info}

Avalie cada critério em uma escala de 0 a 1:
- Budget (Orçamento): O lead tem orçamento disponível para nossa solução?
- Authority (Autoridade): O contato tem poder de decisão ou influência no processo de compra?
- Need (Necessidade): O lead tem uma necessidade clara que nosso produto/serviço pode resolver?
- Timeline (Prazo): O lead tem um prazo definido para implementação ou compra?
"""

# Template para recomendação de abordagem
APPROACH_RECOMMENDATION_TEMPLATE = """
Com base nas informações e na qualificação deste lead, sugira uma abordagem personalizada para o time de vendas.
Informações do Lead:
{lead_info}

Qualificação BANT:
- Budget: {budget_score}
- Authority: {authority_score}
- Need: {need_score}
- Timeline: {timeline_score}
- Pontuação geral: {overall_score}
- Categoria: {tier}

Forneça:
1. Um assunto de email personalizado
2. Pontos principais a serem abordados na primeira interação
3. Objeções potenciais e como responder a elas
4. Próximos passos recomendados
"""