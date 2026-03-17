import json
from datetime import datetime
from pathlib import Path

NOTES_FILE = Path.home() / ".biblia-cli" / "notes.json"

def _load():
    if NOTES_FILE.exists():
        try: return json.loads(NOTES_FILE.read_text(encoding="utf-8"))
        except Exception: pass
    return []

def _save(data):
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
    NOTES_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def get_chapter_notes(translation, book_id, chapter) -> dict:
    return {n["verse"]: n["text"] for n in _load()
            if n["translation"]==translation and n["book_id"]==book_id and n["chapter"]==chapter}

def get_note(translation, book_id, chapter, verse):
    for n in _load():
        if n["translation"]==translation and n["book_id"]==book_id and n["chapter"]==chapter and n["verse"]==verse:
            return n["text"]
    return None

def save_note(translation, book_id, chapter, verse, book_name, text):
    data = _load()
    for n in data:
        if n["translation"]==translation and n["book_id"]==book_id and n["chapter"]==chapter and n["verse"]==verse:
            n["text"]=text; n["updated_at"]=datetime.now().isoformat(timespec="seconds")
            _save(data); return
    data.append({"translation":translation,"book_id":book_id,"book_name":book_name,
                 "chapter":chapter,"verse":verse,"text":text,
                 "updated_at":datetime.now().isoformat(timespec="seconds")})
    _save(data)

def delete_note(translation, book_id, chapter, verse):
    data = [n for n in _load() if not (n["translation"]==translation and n["book_id"]==book_id
            and n["chapter"]==chapter and n["verse"]==verse)]
    _save(data)