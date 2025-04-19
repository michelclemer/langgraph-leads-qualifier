# Guia de Execução e Teste - Sistema de Qualificação de Leads com LangGraph

## Problema Identificado
No processo de vendas, a qualificação inadequada de leads gera desperdício de tempo e recursos, uma vez que equipes comerciais gastam energia com prospects que não estão prontos para conversão. A ausência de uma padronização e de uma priorização baseada em dados compromete a eficiência das ações comerciais.

## Solução Proposta
Este sistema utiliza **LangGraph** para construir um grafo de fluxo de trabalho inteligente, dividido em etapas sequenciais:

1. **Processamento de Leads**: Normaliza os dados e os formata para análise.
2. **Qualificação**: Avalia os leads com base em critérios predefinidos.
3. **Priorizacão**: Ordena os leads com base em sua relevância e potencial.
4. **Recomendação de Abordagens**: Sugere a melhor estratégia para contato.

Em cada etapa, o sistema valida erros e decide dinamicamente o próximo passo.

---

## Como Executar

### 1. Instale as dependências
```bash
pip install -r requirements.txt
```

### 2. Estrutura esperada
```
project/
├── data/
│   └── sample_leads.json
├── src/
│   ├── lead_processor.py
│   ├── lead_qualifier.py
│   ├── lead_prioritizer.py
│   └── approach_recommender.py
├── main.py
└── resultados_leads.json
```

### 3. Execute o sistema
```bash
python main.py
```

O sistema carregará os dados do arquivo `sample_leads.json`, processará e salvará os resultados em `resultados_leads.json`.

---

## Como Testar
- Altere o arquivo `sample_leads.json` com dados fictícios de leads.
- Verifique o arquivo `resultados_leads.json` para conferir:
  - Ordem de priorização
  - Abordagem recomendada
  - Nível e pontuação de prioridade

**Exemplo de entrada:**
```json
{
  "id": "123",
  "name": "João Silva",
  "company": "Tech Ltda",
  "email": "joao@tech.com",
  "industry": "Software"
}
```

---

## Próximos Passos com Mais Tempo
- **Integração com CRM** (Ex: HubSpot, Pipedrive).
- **Aprimoramento do modelo de qualificação com IA supervisionada**.
- **Interface Web com dashboards e filtros dinâmicos**.
- **Armazenamento em banco de dados relacional ou NoSQL para consulta histórica**.
- **Agendamento de execução automática com workflows (ex: Airflow ou Prefect)**.

---

## Conclusão
Essa solução visa automatizar e escalar o processo de qualificação de leads com base em regras inteligentes e adaptáveis. O uso do LangGraph permite controlar o fluxo de decisões de forma robusta, favorecendo expansão e integração com outras ferramentas do ecossistema de vendas.

