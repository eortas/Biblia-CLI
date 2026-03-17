import json
from datetime import datetime
from pathlib import Path

FAV_FILE = Path.home() / ".biblia-cli" / "favorites.json"

def _load():
    if FAV_FILE.exists():
        try: return json.loads(FAV_FILE.read_text(encoding="utf-8"))
        except Exception: pass
    return []

def _save(data):
    FAV_FILE.parent.mkdir(parents=True, exist_ok=True)
    FAV_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def all_favorites(): return _load()

def is_favorite(translation, book_id, chapter):
    return any(f["translation"]==translation and f["book_id"]==book_id and f["chapter"]==chapter for f in _load())

def toggle(translation, book_id, book_name, chapter) -> bool:
    data = _load()
    for i, f in enumerate(data):
        if f["translation"]==translation and f["book_id"]==book_id and f["chapter"]==chapter:
            data.pop(i); _save(data); return False
    data.append({"translation":translation,"book_id":book_id,"book_name":book_name,
                 "chapter":chapter,"added_at":datetime.now().isoformat(timespec="seconds")})
    _save(data); return True