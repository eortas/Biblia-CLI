import json
import re
import httpx
import html
from .book_names import resolve_book

async def get_daily_readings():
    """
    Fetches the daily liturgical readings from Universalis.
    Returns a list of dicts: [{"label": "Evangelio", "book_id": 43, "chapter": 3, "source": "Juan 3"}, ...]
    """
    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as c:
        r = await c.get("https://universalis.com/Europe.Spain/jsonpmass.js")
        r.raise_for_status()
        mj = re.search(r"universalisCallback\((.*)\);", r.text, re.DOTALL)
        if not mj: raise Exception("Error de formato en la respuesta de Universalis")
        
        data = json.loads(mj.group(1))
        mapping = {
            "Mass_R1": "Primera Lectura",
            "Mass_R2": "Segunda Lectura",
            "Mass_Ps": "Salmo Responsorial",
            "Mass_G":  "Evangelio"
        }
        
        results = []
        for key, label in mapping.items():
            src = data.get(key, {}).get("source", "")
            if not src: continue
            
            # Format: "1 Juan 3" or "Juan 3, 1-16"
            m = re.search(r"^([1-3]?\s?[a-zA-Z\sèéíóúÁÉÍÓÚñÑ]+)\s+(\d+)", src)
            if not m: continue
            
            bname, ch = m.group(1).strip(), int(m.group(2))
            bid = resolve_book(bname)
            if not bid: continue
            
            src_clean = html.unescape(src).replace('\u2010', '-').replace('\u2013', '-').replace('\u2014', '-')
            results.append({
                "label": label,
                "book_id": bid,
                "chapter": ch,
                "source": src_clean
            })
            
        if not results:
            raise Exception("No se encontraron lecturas para hoy")
        return results
