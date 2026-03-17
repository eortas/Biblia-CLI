import os
from dotenv import load_dotenv

load_dotenv()

# Pública — solo permite leer filas cifradas (el texto es ilegible sin ANN_ENCRYPT_KEY)
SUPABASE_URL      = "https://dffmmbdwpuvjebixaulq.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_RgsSeOxSM5jcOjo55UmRyA_2E0BHZSI"

# Clave de descifrado — va hardcodeada aquí para que todos los lectores puedan descifrar
# No importa que sea visible: sin los datos cifrados de Supabase no sirve de nada.
ANN_ENCRYPT_KEY = os.getenv("ANN_ENCRYPT_KEY", "rSYfNjzPFm-FB3bo9ORRD1b18xVNrXPC_0NcnxWlcKk=")