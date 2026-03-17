import re, httpx
from .. import cache as local_cache

BASE    = "https://bolls.life"
TIMEOUT = 15.0

TRANSLATIONS = {
    "Español 🇪🇸":  [("RV1960", "Reina-Valera 1960")],
    "Português 🇧🇷": [("ARA",   "Almeida Revista e Atualizada")],
}
PT_CODES = {"ARA","ARC09","NVIPT","NTLH","NVT","NAA","OL","KJA","CNBB","TB10","ACF11","NTJud","VFL","NBV07","ALM21"}

def _clean(text):
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    return re.sub(r"<[^>]+>", "", text).strip()

class BollsClient:
    async def get_books(self, translation):
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get(f"{BASE}/get-books/{translation}/"); r.raise_for_status()
            return r.json()

    async def get_chapter(self, translation, book_id, chapter):
        cached = local_cache.load(translation, book_id, chapter)
        if cached: return cached
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get(f"{BASE}/get-text/{translation}/{book_id}/{chapter}/"); r.raise_for_status()
            verses = r.json()
        for v in verses: v["text"] = _clean(v["text"])
        local_cache.save(translation, book_id, chapter, verses)
        return verses

    async def search(self, translation, query, page=1, limit=50):
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get(f"{BASE}/v2/find/{translation}", params={"search":query,"page":page,"limit":limit})
            r.raise_for_status(); data = r.json()
        for res in data.get("results",[]): res["text"] = _clean(res["text"])
        return data

    async def get_random_verse(self, translation):
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get(f"{BASE}/get-random-verse/{translation}/"); r.raise_for_status()
            v = r.json(); v["text"] = _clean(v["text"]); return v