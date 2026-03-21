import json
import re
import httpx
import html
from .book_names import resolve_book

async def get_daily_reading():
    """
    Fetches the daily liturgical reading from Universalis.
    Returns (book_id, chapter, source_text).
    """
    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as c:
        r = await c.get("https://universalis.com/Europe.Spain/jsonpmass.js")
        r.raise_for_status()
        txt = r.text
        mj = re.search(r"universalisCallback\((.*)\);", txt, re.DOTALL)
        if not mj: 
            raise Exception("Error de formato en la respuesta de Universalis")
        
        data = json.loads(mj.group(1))
        # Try different sources in the mass data
        src = data.get("Mass_R1", {}).get("source", "")
        if not src: 
            src = data.get("Mass_G", {}).get("source", "")
        
        if not src:
            raise Exception("No se encontró lectura del día en los datos recibidos")
            
        # Regex to match something like "1 Juan 3" or "Juan 3"
        m = re.search(r"^([1-3]?\s?[a-zA-Z\sèéíóúÁÉÍÓÚñÑ]+)\s+(\d+)", src)
        if not m: 
            raise Exception(f"No se pudo parsear la referencia: {src}")
        
        bname, ch = m.group(1).strip(), int(m.group(2))
        bid = resolve_book(bname)
        if not bid: 
            raise Exception(f"No se reconoce el libro: {bname}")
        
        # Clean up problematic characters for terminal display
        src_clean = html.unescape(src)
        src_clean = src_clean.replace('\u2010', '-').replace('\u2013', '-').replace('\u2014', '-')
        
        return bid, ch, src_clean
