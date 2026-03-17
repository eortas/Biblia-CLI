import sys
from biblia_cli.config import Config

def main():
    import argparse
    p = argparse.ArgumentParser(prog="biblia", add_help=False)
    p.add_argument("args", nargs="*"); p.add_argument("-t","--translation",default=None); p.add_argument("-h","--help",action="store_true")
    ns = p.parse_args(); translation = ns.translation or Config().load().get("translation","RV1960")
    if not ns.args and not ns.help:
        from biblia_cli.app import BibliaApp; BibliaApp().run()
    else:
        from biblia_cli.pipe_mode import run; run(ns.args if not ns.help else ["ayuda"], translation)

if __name__ == "__main__": main()