from __future__ import annotations
import asyncio, sys
from .api.bolls_client import BollsClient
from .book_names import resolve_book, lang_for_translation, get_books_for_lang, BOOKS
from .cache import stats as cache_stats

def run(args, translation): asyncio.run(_run(args, translation))

async def _run(args, translation):
    client = BollsClient(); lang = lang_for_translation(translation)
    cmd = (args[0] if args else "").lower()
    if not args or cmd in ("-h","--help","ayuda"):
        print("""
  biblia — modo consola
    biblia                     → TUI interactivo
    biblia juan 3:16           → versículo
    biblia juan 3:14-17        → rango
    biblia salmos 23           → capítulo completo
    biblia buscar "texto"      → búsqueda
    biblia libros              → 66 libros
    biblia cache               → capítulos offline
    biblia -t ARA juan 3:16   → otra traducción
        """); return
    if cmd in ("libros","books","livros"):
        print(f"\n  Libros [{translation}]\n")
        for bid,nes,npt,ch in BOOKS:
            print(f"  {bid:>3}.  {(nes if lang=='es' else npt):<22}  ({ch} cap.)")
        return
    if cmd in ("cache","caché"):
        s = cache_stats()
        if not s: print("  Cache vacío."); return
        for t,n in sorted(s.items()): print(f"  {t:<12} {n} capítulos")
        return
    if cmd in ("buscar","search","procurar"):
        query = " ".join(args[1:]).strip("\"' ")
        if not query: print("  Uso: biblia buscar \"texto\""); return
        print(f"\n  Buscando \"{query}\" en {translation}...")
        try:
            data = await client.search(translation, query, limit=10)
            results = data.get("results",[])
            names = {bid:(es if lang=="es" else pt) for bid,es,pt,_ in BOOKS}
            print(f"  {len(results)} de {data.get('total',0)} resultados\n")
            for r in results:
                print(f"  [{names.get(r['book'],str(r['book']))} {r['chapter']}:{r['verse']}]")
                print(f"  {r['text']}\n")
        except Exception as e: print(f"  Error: {e}", file=sys.stderr)
        return
    book_part, ref_part = cmd, ""
    for i in range(1, len(args)):
        t = args[i]
        if ":" in t or t.isdigit(): ref_part = t; break
        book_part += " " + t
    book_id = resolve_book(book_part.strip(), lang)
    if not book_id: print(f"  Libro no encontrado: '{book_part.strip()}'."); return
    names = {bid:(es if lang=="es" else pt) for bid,es,pt,_ in BOOKS}
    chapter, vs, ve = 1, None, None
    if ref_part:
        if ":" in ref_part:
            ch_s,v_s = ref_part.split(":",1); chapter = int(ch_s) if ch_s.isdigit() else 1
            if "-" in v_s:
                a,b = v_s.split("-",1); vs,ve = (int(a) if a.isdigit() else None),(int(b) if b.isdigit() else None)
            elif v_s.isdigit(): vs = ve = int(v_s)
        elif ref_part.isdigit(): chapter = int(ref_part)
    try: verses = await client.get_chapter(translation, book_id, chapter)
    except Exception as e: print(f"  Error: {e}", file=sys.stderr); return
    if vs: verses = [v for v in verses if vs <= v["verse"] <= (ve or vs)]
    print(f"\n  {names.get(book_id)} {chapter}  [{translation}]\n")
    for v in verses: print(f"  {v['verse']:>3}  {v['text']}")
    print()