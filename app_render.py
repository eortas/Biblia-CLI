import traceback
import sys

try:
    from biblia_cli.app import BibliaApp
    print("BibliaApp importada OK", flush=True)
    app = BibliaApp()
    print("BibliaApp instanciada OK", flush=True)
    app.run()
except Exception as e:
    print(f"ERROR: {e}", flush=True)
    traceback.print_exc()
    sys.exit(1)