"""
Script de autor. USA SERVICE ROLE KEY + ANN_ENCRYPT_KEY — no distribuyas este archivo.

  python admin_annotations.py genkey              → genera una clave nueva (hazlo UNA vez)
  python admin_annotations.py add    RV1960 43 3 16 "Tu nota"
  python admin_annotations.py delete RV1960 43 3 16
  python admin_annotations.py list                → muestra texto DESCIFRADO
  python admin_annotations.py list-raw            → muestra texto cifrado tal como está en Supabase
"""
import sys, os
from dotenv import load_dotenv
from supabase import create_client
import sys

load_dotenv()
sys.stdout.reconfigure(encoding="utf-8")

SUPABASE_URL     = "https://dffmmbdwpuvjebixaulq.supabase.co"
SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
ANN_ENCRYPT_KEY  = os.getenv("ANN_ENCRYPT_KEY", "")

def _fernet():
    from cryptography.fernet import Fernet
    if not ANN_ENCRYPT_KEY or ANN_ENCRYPT_KEY == "PENDIENTE_GENERAR":
        print("❌  ANN_ENCRYPT_KEY no encontrada en .env"); sys.exit(1)
    return Fernet(ANN_ENCRYPT_KEY.encode())

def _client():
    if not SERVICE_ROLE_KEY:
        print("❌  SUPABASE_SERVICE_ROLE_KEY no encontrada en .env"); sys.exit(1)
    return create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

def genkey():
    from cryptography.fernet import Fernet
    key = Fernet.generate_key().decode()
    print(f"\n  Clave generada — cópiala en tu .env:\n")
    print(f"  ANN_ENCRYPT_KEY={key}\n")
    print("  ⚠️  Guárdala bien. Si la pierdes no podrás descifrar las anotaciones.\n")

def add(translation, book_id, chapter, verse, text):
    encrypted = _fernet().encrypt(text.encode()).decode()
    _client().table("annotations").upsert({
        "translation": translation, "book_id": int(book_id),
        "chapter": int(chapter), "verse": int(verse), "text": encrypted
    }).execute()
    print(f"✅  Guardada cifrada: {translation} {book_id}/{chapter}:{verse}")

def delete(translation, book_id, chapter, verse):
    _client().table("annotations").delete() \
        .eq("translation", translation).eq("book_id", int(book_id)) \
        .eq("chapter", int(chapter)).eq("verse", int(verse)).execute()
    print("🗑  Eliminada")

def list_all(raw=False):
    res = _client().table("annotations").select("*").order("book_id").order("chapter").order("verse").execute()
    f = _fernet() if not raw else None
    for r in res.data:
        text = r["text"] if raw else f.decrypt(r["text"].encode()).decode()
        preview = text[:80] + ("…" if len(text) > 80 else "")
        print(f"  [{r['translation']}] libro {r['book_id']} {r['chapter']}:{r['verse']}")
        print(f"    {preview}\n")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if   cmd == "genkey":                          genkey()
    elif cmd == "add"      and len(sys.argv) >= 7: add(*sys.argv[2:7])
    elif cmd == "delete"   and len(sys.argv) >= 6: delete(*sys.argv[2:6])
    elif cmd == "list":                            list_all(raw=False)
    elif cmd == "list-raw":                        list_all(raw=True)
    else: print(__doc__)