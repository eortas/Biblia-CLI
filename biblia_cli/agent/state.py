from __future__ import annotations
from typing import TypedDict


class AgentState(TypedDict):
    """Estado que fluye a través del grafo LangGraph del agente bíblico."""
    question:     str          # Pregunta original del usuario
    translation:  str          # Código de traducción (RV1960, ARA…)
    search_terms: list[str]    # Términos extraídos por el nodo interpret
    results:      list[dict]   # Versículos acumulados de la API
    cycles:       int          # Contador de ciclos de refinamiento (max 2)
    next_action:  str          # Señal de routing: "cite" | "refine"
    answer:       str          # Respuesta final del agente
