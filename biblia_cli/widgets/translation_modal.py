from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Label
from textual.containers import Vertical
from ..api.bolls_client import TRANSLATIONS

class TranslationModal(ModalScreen):
    DEFAULT_CSS="""
    TranslationModal { align: center middle; }
    #t-box { width: 50; height: auto; background: $surface; border: thick $primary; padding: 1 2; }
    #t-title { text-style: bold; color: $accent; text-align: center; width: 100%; margin-bottom: 1; }
    .t-lang  { color: $text-muted; text-style: italic; margin-top: 1; }
    .t-btn   { width: 100%; margin: 0; }
    #t-cancel{ width: 100%; margin-top: 1; }
    """
    def compose(self) -> ComposeResult:
        with Vertical(id="t-box"):
            yield Label("🌐 Seleccionar Traducción",id="t-title")
            for lang,items in TRANSLATIONS.items():
                yield Label(f"── {lang} ──",classes="t-lang")
                for code,name in items:
                    yield Button(f"{code}  {name}",id=f"t-{code}",classes="t-btn")
            yield Button("✕  Cancelar",id="t-cancel",variant="error")
    def on_button_pressed(self,event:Button.Pressed):
        if event.button.id=="t-cancel": self.dismiss(None)
        elif event.button.id and event.button.id.startswith("t-"): self.dismiss(event.button.id[2:])