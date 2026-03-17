"""
Anotaciones del autor — cifradas en Supabase, descifradas en memoria.

Flujo:
  · En Supabase: texto cifrado con Fernet (ilegible sin la clave)
  · En la app:   se descifra al vuelo con ANN_ENCRYPT_KEY de settings.py
  · En disco:    nada se guarda
"""
from __future__ import annotations
import json
from pathlib import Path

_chapter_cache: dict[str, dict[int, str]] = {}
_LOCAL_DRAFT = Path.home() / ".biblia-cli" / "ann_drafts.json"

def _prefix(t, b, c): return f"{t}/{b}/{c}"
def _key(t, b, c, v): return f"{t}/{b}/{c}/{v}"

def _client():
    from .settings import SUPABASE_URL, SUPABASE_ANON_KEY
    from supabase import create_client
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def _decrypt(text: str) -> str:
    try:
        from cryptography.fernet import Fernet
        from .settings import ANN_ENCRYPT_KEY
        return Fernet(ANN_ENCRYPT_KEY.encode()).decrypt(text.encode()).decode()
    except Exception:
        return text  # si falla el descifrado devuelve el texto tal cual

# ── Supabase (lectura + descifrado) ──────────────────────────────────────────
async def get_chapter(translation: str, book_id: int, chapter: int) -> dict[int, str]:
    key = _prefix(translation, book_id, chapter)
    if key in _chapter_cache: return _chapter_cache[key]
    try:
        res = _client().table("annotations") \
            .select("verse, text") \
            .eq("translation", translation) \
            .eq("book_id", book_id) \
            .eq("chapter", chapter) \
            .execute()
        result = {r["verse"]: _decrypt(r["text"]) for r in (res.data or [])}
    except Exception:
        result = {}
    _chapter_cache[key] = result
    return result

def invalidate(translation, book_id, chapter):
    _chapter_cache.pop(_prefix(translation, book_id, chapter), None)

# ── Borrador local (modal de escritura in-app) ────────────────────────────────
def _load_drafts():
    if _LOCAL_DRAFT.exists():
        try: return json.loads(_LOCAL_DRAFT.read_text(encoding="utf-8"))
        except Exception: pass
    return {}

def _save_drafts(data):
    _LOCAL_DRAFT.parent.mkdir(parents=True, exist_ok=True)
    _LOCAL_DRAFT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def get_note_local(translation, book_id, chapter, verse) -> str | None:
    return _load_drafts().get(_key(translation, book_id, chapter, verse))

def save_local(translation, book_id, chapter, verse, text):
    data = _load_drafts(); data[_key(translation, book_id, chapter, verse)] = text; _save_drafts(data)

def delete_local(translation, book_id, chapter, verse):
    data = _load_drafts(); data.pop(_key(translation, book_id, chapter, verse), None); _save_drafts(data)