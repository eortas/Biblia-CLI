import json
from pathlib import Path

CACHE_DIR = Path.home() / ".biblia-cli" / "cache"

def _p(t, b, c): return CACHE_DIR / t / f"{b}_{c}.json"

def load(translation, book_id, chapter):
    p = _p(translation, book_id, chapter)
    if p.exists():
        try: return json.loads(p.read_text(encoding="utf-8"))
        except Exception: pass
    return None

def save(translation, book_id, chapter, verses):
    p = _p(translation, book_id, chapter)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(verses, ensure_ascii=False), encoding="utf-8")

def stats():
    if not CACHE_DIR.exists(): return {}
    return {d.name: len(list(d.glob("*.json"))) for d in CACHE_DIR.iterdir() if d.is_dir()}