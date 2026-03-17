import json
from pathlib import Path

CONFIG_DIR  = Path.home() / ".biblia-cli"
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULTS = {"translation": "RV1960", "last_book_id": 1, "last_chapter": 1, "theme": "dark"}

class Config:
    def load(self) -> dict:
        if CONFIG_FILE.exists():
            try: return {**DEFAULTS, **json.loads(CONFIG_FILE.read_text(encoding="utf-8"))}
            except Exception: pass
        return dict(DEFAULTS)
    def save(self, data: dict) -> None:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        existing = self.load(); existing.update(data)
        CONFIG_FILE.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")