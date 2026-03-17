THEMES = ["dark","light","sepia","matrix"]
LABELS = {"dark":"🌑 Oscuro","light":"☀️  Claro","sepia":"📜 Sepia","matrix":"💻 Matrix"}
def next_theme(current):
    return THEMES[(THEMES.index(current)+1) % len(THEMES)] if current in THEMES else "dark"