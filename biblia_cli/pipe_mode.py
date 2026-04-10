from __future__ import annotations
import asyncio, sys
from .api.bolls_client import BollsClient
from .book_names import resolve_book, lang_for_translation, get_books_for_lang, BOOKS
from .cache import stats as cache_stats

def run(args, translation): asyncio.run(_run(args, translation))

async def _run(args, translation):
    client = BollsClient(); lang = lang_for_translation(translation)
    names = {bid:(es if lang=="es" else pt) for bid,es,pt,_ in BOOKS}
    cmd = (args[0] if args else "").lower()
    if not args or cmd in ("-h","--help","ayuda"):
        print("""
  biblia — modo consola
    biblia                              → TUI interactivo
    biblia juan 3:16                    → versículo
    biblia juan 3:14-17                 → rango
    biblia salmos 23                    → capítulo completo
    biblia dia                          → lectura del día
    biblia buscar "texto"               → búsqueda
    biblia preguntar "¿pregunta?"       → agente IA (LangGraph + Gemini)
    biblia libros                       → 66 libros
    biblia cache                        → capítulos offline
    biblia -t ARA juan 3:16            → otra traducción
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
            print(f"  {len(results)} de {data.get('total',0)} resultados\n")
            for r in results:
                print(f"  [{names.get(r['book'],str(r['book']))} {r['chapter']}:{r['verse']}]")
                print(f"  {r['text']}\n")
        except Exception as e: print(f"  Error: {e}", file=sys.stderr)
        return
    if cmd in ("preguntar", "pregunta", "ask", "consultar"):
        question = " ".join(args[1:]).strip("\"' ")
        if not question:
            print("  Uso: biblia preguntar \"¿Qué dice la Biblia sobre el amor?\"")
            return
        sep = "\u2500" * 48
        q_short = question[:60] + ("\u2026" if len(question) > 60 else "")
        print(f"\n  \u2726 Agente b\u00edblico IA  [{translation}]")
        print(f"  {sep}")
        print(f"  \u23f3 Procesando: {q_short}\n", flush=True)
        try:
            from .agent.runner import ask as agent_ask
            answer = await agent_ask(question, translation)
            for line in answer.splitlines():
                print(f"  {line}" if line.strip() else "")
            print()
        except ValueError as e:
            print(f"  \u274c {e}", file=sys.stderr)
        except Exception as e:
            print(f"  \u274c Error del agente: {e}", file=sys.stderr)
        return
    vs, ve = None, None
    if cmd in ("dia", "day", "lectura"):
        sub = (args[1] if len(args) > 1 else "").lower()
        print(f"\n  Obteniendo lecturas del día para {translation}...")
        try:
            from .daily_reading import get_daily_readings
            results = await get_daily_readings()
            
            sel = results[0]  # default
            if sub:
                for r in results:
                    if sub in r["label"].lower() or sub in r["source"].lower():
                        sel = r; break
                else: 
                    # check if sub is an index
                    if sub.isdigit() and 1 <= int(sub) <= len(results):
                        sel = results[int(sub)-1]
            
            book_id, chapter, src = sel["book_id"], sel["chapter"], sel["source"]
            print(f"  [{sel['label']}] {src}\n")
            if not sub and len(results) > 1:
                print("  Otras lecturas disponibles:")
                for i, r in enumerate(results[1:], 2):
                    print(f"    - {r['label']}: {r['source']} (usa 'biblia dia {i}' o 'biblia dia {r['label'].split()[0].lower()}')")
                print()
        except Exception as e:
            print(f"  Error: {e}", file=sys.stderr); return
    else:
        book_part, ref_part = cmd, ""
        for i in range(1, len(args)):
            t = args[i]
            if ":" in t or t.isdigit(): ref_part = t; break
            book_part += " " + t
        book_id = resolve_book(book_part.strip(), lang)
        if not book_id: print(f"  Libro no encontrado: '{book_part.strip()}'."); return
        chapter = 1
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