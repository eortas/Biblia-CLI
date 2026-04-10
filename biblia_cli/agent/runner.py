"""
Runner público para el agente bíblico LangGraph.
Uso desde pipe_mode:   answer = await ask(question, translation)
"""
from __future__ import annotations

from dotenv import load_dotenv

from .graph import get_graph
from .state import AgentState


async def ask(question: str, translation: str = "RV1960") -> str:
    """
    Ejecuta el grafo LangGraph y devuelve la respuesta formateada.
    Lanza ValueError si GEMINI_API_KEY no está configurada.
    """
    load_dotenv()

    initial_state: AgentState = {
        "question":     question,
        "translation":  translation,
        "search_terms": [],
        "results":      [],
        "cycles":       0,
        "next_action":  "cite",
        "answer":       "",
    }

    graph  = get_graph()
    result = await graph.ainvoke(initial_state)
    return result.get("answer", "No se pudo generar una respuesta.")
