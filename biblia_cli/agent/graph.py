"""
Construcción y compilación del StateGraph LangGraph.

Grafo:
    START → interpret → search → evaluate ──┬──► cite → END
                            ▲               │
                            └── refine ◄────┘ (si next_action == "refine")
"""
from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from .state import AgentState
from .nodes import (
    node_cite,
    node_evaluate,
    node_interpret,
    node_refine,
    node_search,
    route_after_evaluate,
)


def build_graph():
    """Crea y compila el StateGraph del agente bíblico."""
    g = StateGraph(AgentState)

    # Registrar nodos
    g.add_node("interpret", node_interpret)
    g.add_node("search",    node_search)
    g.add_node("evaluate",  node_evaluate)
    g.add_node("refine",    node_refine)
    g.add_node("cite",      node_cite)

    # Edges estáticos
    g.add_edge(START,       "interpret")
    g.add_edge("interpret", "search")
    g.add_edge("search",    "evaluate")
    g.add_edge("refine",    "search")
    g.add_edge("cite",      END)

    # Edge condicional: evaluate → cite | refine
    g.add_conditional_edges(
        "evaluate",
        route_after_evaluate,
        {"cite": "cite", "refine": "refine"},
    )

    return g.compile()


# Singleton del grafo compilado (se crea la primera vez que se usa)
_graph = None


def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph
