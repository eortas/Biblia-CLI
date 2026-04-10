import sys
from biblia_cli.config import Config

def _ensure_utf8():
    """Fuerza UTF-8 en stdout/stderr en Windows (CMD/PowerShell usan cp1252 por defecto)."""
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except AttributeError:
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

def main():
    _ensure_utf8()
    import argparse
    p = argparse.ArgumentParser(prog="biblia", add_help=False)
    p.add_argument("args", nargs="*"); p.add_argument("-t","--translation",default=None); p.add_argument("-h","--help",action="store_true")
    ns = p.parse_args(); translation = ns.translation or Config().load().get("translation","RV1960")
    if not ns.args and not ns.help:
        from biblia_cli.app import BibliaApp; BibliaApp().run()
    else:
        from biblia_cli.pipe_mode import run; run(ns.args if not ns.help else ["ayuda"], translation)

if __name__ == "__main__": main()