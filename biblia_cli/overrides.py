import json
from pathlib import Path

_FILE = Path.home() / ".biblia-cli" / "overrides.json"

def _load():
    if _FILE.exists():
        try: return json.loads(_FILE.read_text(encoding="utf-8"))
        except Exception: pass
    return {}

def _save(data):
    _FILE.parent.mkdir(parents=True, exist_ok=True)
    _FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def _key(translation, book_id, chapter, verse): return f"{translation}/{book_id}/{chapter}/{verse}"

def get(translation, book_id, chapter, verse): return _load().get(_key(translation,book_id,chapter,verse))

def get_chapter(translation, book_id, chapter):
    prefix = f"{translation}/{book_id}/{chapter}/"
    return {int(k.split("/")[-1]): v for k,v in _load().items() if k.startswith(prefix)}

def set(translation, book_id, chapter, verse, text):
    data = _load(); data[_key(translation,book_id,chapter,verse)] = text; _save(data)

def delete(translation, book_id, chapter, verse):
    data = _load(); data.pop(_key(translation,book_id,chapter,verse), None); _save(data)

def apply_to_chapter(verses, translation, book_id, chapter):
    ov = get_chapter(translation, book_id, chapter)
    if not ov: return verses
    result = []
    for v in verses:
        if v["verse"] in ov:
            v = dict(v); v["original_text"] = v["text"]; v["text"] = ov[v["verse"]]
        result.append(v)
    return result