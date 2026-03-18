import traceback
import sys
from biblia_cli.app import BibliaApp

try:
    app = BibliaApp()
    app.run()
except Exception as e:
    with open("error.log", "a") as f:
        f.write(f"ERROR: {e}\n")
        traceback.print_exc(file=f)
    sys.exit(1)