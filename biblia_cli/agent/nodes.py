"""
Nodos del grafo LangGraph para el agente de consulta bíblica.

Flujo:
    interpret → search → evaluate → (cite | refine → search → …) → cite
"""
from __future__ import annotations

import json
import os

from langchain_google_genai import ChatGoogleGenerativeAI

from .state import AgentState
from ..api.bolls_client import BollsClient, PT_CODES
from ..book_names import BOOKS

# ─── Tablas de nombres de libros ────────────────────────────────────────────
_NAMES_ES: dict[int, str] = {bid: es  for bid, es, _,  _ in BOOKS}
_NAMES_PT: dict[int, str] = {bid: pt  for bid, _,  pt, _ in BOOKS}


# ─── LLM singleton ──────────────────────────────────────────────────────────
_llm_instance: ChatGoogleGenerativeAI | None = None


def _get_llm() -> ChatGoogleGenerativeAI:
    global _llm_instance
    if _llm_instance is None:
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            raise ValueError(
                "🔑 GEMINI_API_KEY no encontrada en el .env\n"
                "  Obtén una clave GRATIS en: https://aistudio.google.com/apikey\n"
                "  Luego añade al .env:  GEMINI_API_KEY=AIza..."
            )
        _llm_instance = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.3,
        )
    return _llm_instance


# ─── Utilidades ─────────────────────────────────────────────────────────────
def _parse_json(text: str) -> dict:
    """Parsea JSON de la respuesta del LLM, ignorando bloques markdown."""
    text = text.strip()
    if "```" in text:
        for block in text.split("```")[1::2]:
            block = block.lstrip("json").strip()
            try:
                return json.loads(block)
            except json.JSONDecodeError:
                continue
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}


def _lang(translation: str) -> str:
    return "pt" if translation in PT_CODES else "es"


def _book_names(translation: str) -> dict[int, str]:
    return _NAMES_PT if _lang(translation) == "pt" else _NAMES_ES


# ─── Nodos ──────────────────────────────────────────────────────────────────

async def node_interpret(state: AgentState) -> dict:
    """Extrae 1-3 términos de búsqueda concretos de la pregunta del usuario."""
    lang = _lang(state["translation"])
    lang_label = "en español" if lang == "es" else "em português"

    prompt = (
        f'Eres un asistente bíblico experto. El usuario pregunta:\n'
        f'"{state["question"]}"\n\n'
        f'Extrae entre 1 y 3 palabras clave {lang_label} para buscar en un índice bíblico. '
        f'Deben ser términos simples que aparecerían en los versículos '
        f'(ej: "perdón", "amor", "resurrección", "fe").\n'
        f'Devuelve ÚNICAMENTE este JSON, sin texto adicional: '
        f'{{"terms": ["término1", "término2"]}}'
    )

    response = await _get_llm().ainvoke(prompt)
    data = _parse_json(response.content)
    terms = [str(t).strip() for t in data.get("terms", [])][:3]

    if not terms:
        # Fallback: usa la pregunta simplificada
        fallback = state["question"].split("?")[0].split("¿")[-1].strip()[:50]
        terms = [fallback]

    return {"search_terms": terms, "results": [], "cycles": 0, "next_action": "cite"}


async def node_search(state: AgentState) -> dict:
    """Busca cada término en la API de Bolls.life y acumula versículos únicos."""
    client = BollsClient()
    existing: set[tuple] = {
        (r["book"], r["chapter"], r["verse"])
        for r in state.get("results", [])
    }
    accumulated = list(state.get("results", []))

    for term in state.get("search_terms", []):
        try:
            data = await client.search(state["translation"], term, limit=15)
            for r in data.get("results", []):
                key = (r["book"], r["chapter"], r["verse"])
                if key not in existing:
                    existing.add(key)
                    accumulated.append(r)
        except Exception:
            pass  # Errores de red se ignoran silenciosamente

    return {"results": accumulated}


async def node_evaluate(state: AgentState) -> dict:
    """Decide si los resultados son suficientes o si hay que refinar la búsqueda."""
    results = state.get("results", [])
    cycles  = state.get("cycles", 0)

    # Cortocircuitos sin llamada al LLM
    if not results or len(results) >= 5 or cycles >= 2:
        return {"next_action": "cite"}

    names = _book_names(state["translation"])
    snippets = "\n".join(
        f'- {names.get(r["book"], r["book"])} {r["chapter"]}:{r["verse"]}: '
        f'{r["text"][:100]}…'
        for r in results[:5]
    )
    prompt = (
        f'Pregunta: "{state["question"]}"\n\n'
        f'Versículos encontrados:\n{snippets}\n\n'
        f'¿Responden bien estos versículos a la pregunta?\n'
        f'Devuelve ÚNICAMENTE este JSON: {{"sufficient": true}} o {{"sufficient": false}}'
    )

    response = await _get_llm().ainvoke(prompt)
    data = _parse_json(response.content)

    if data.get("sufficient", True):
        return {"next_action": "cite"}
    else:
        return {"next_action": "refine", "cycles": cycles + 1}


async def node_refine(state: AgentState) -> dict:
    """Genera términos de búsqueda alternativos para un segundo ciclo."""
    lang = _lang(state["translation"])
    lang_label = "en español" if lang == "es" else "em português"
    used = ", ".join(f'"{t}"' for t in state.get("search_terms", []))

    prompt = (
        f'Pregunta bíblica: "{state["question"]}"\n'
        f'Ya buscaste por: {used} — los resultados no fueron suficientes.\n\n'
        f'Genera 2 términos alternativos {lang_label} distintos para buscar en la Biblia.\n'
        f'Devuelve ÚNICAMENTE: {{"terms": ["nuevo1", "nuevo2"]}}'
    )

    response = await _get_llm().ainvoke(prompt)
    data = _parse_json(response.content)
    new_terms = [str(t).strip() for t in data.get("terms", [])][:2]

    if not new_terms:
        new_terms = ["dios", "espíritu"]

    return {"search_terms": new_terms}


async def node_cite(state: AgentState) -> dict:
    """Sintetiza la respuesta final con citas bíblicas reales."""
    results    = state.get("results", [])
    translation = state["translation"]
    names      = _book_names(translation)

    # Sin resultados
    if not results:
        answer = (
            f'No encontré versículos relevantes para "{state["question"]}" '
            f'en la traducción {translation}.\n'
            f'Intenta reformular la pregunta o usar términos más generales.'
        )
        return {"answer": answer}

    # Construye contexto con los mejores 10 versículos
    context = "\n".join(
        f'[{names.get(r["book"], r["book"])} {r["chapter"]}:{r["verse"]}] {r["text"]}'
        for r in results[:10]
    )

    lang = _lang(translation)
    lang_label = "en español" if lang == "es" else "em português"

    prompt = (
        f'Eres un comentarista bíblico. El usuario preguntó:\n'
        f'"{state["question"]}"\n\n'
        f'Usando SOLO los siguientes versículos de la Biblia ({translation}):\n\n'
        f'{context}\n\n'
        f'Escribe una respuesta {lang_label}, clara y directa (máximo 4 frases) '
        f'que responda la pregunta citando los versículos más relevantes con su referencia '
        f'exacta (Libro Capítulo:Versículo). Si los versículos no responden bien la '
        f'pregunta, indícalo con honestidad.'
    )

    response = await _get_llm().ainvoke(prompt)

    # Añade lista de versículos al pie
    verse_lines = []
    for r in results[:6]:
        name = names.get(r["book"], str(r["book"]))
        ref  = f"{name} {r['chapter']}:{r['verse']}"
        text = r["text"] if len(r["text"]) <= 120 else r["text"][:117] + "…"
        verse_lines.append(f"    [{ref}]  {text}")

    answer = "\n".join([
        response.content.strip(),
        "",
        "  \U0001f4d6 Vers\u00edculos encontrados:",
        *verse_lines,
    ])

    return {"answer": answer}


# ─── Router (edge condicional) ───────────────────────────────────────────────

def route_after_evaluate(state: AgentState) -> str:
    """Devuelve 'cite' o 'refine' según lo decidido por node_evaluate."""
    return state.get("next_action", "cite")
