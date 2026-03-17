from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, TextArea
from .. import overrides as ov

class OverrideModal(ModalScreen):
    DEFAULT_CSS="""
    OverrideModal { align: center middle; }
    #ov-box { width: 76; height: auto; background: $surface; border: thick $primary; padding: 1 2; }
    #ov-title { text-style: bold; color: $accent; text-align: center; width: 100%; margin-bottom: 1; }
    #ov-original { color: $text-muted; margin-bottom: 1; padding: 0 1; border-left: solid $primary; }
    #ov-area { height: 10; border: solid $primary; margin-bottom: 1; }
    #ov-foot { height: 3; align: right middle; }
    #ov-restore { margin-right: 1; }
    """
    def __init__(self,translation,book_id,book_name,chapter,verse,original_text):
        super().__init__(); self.translation=translation; self.book_id=book_id
        self.book_name=book_name; self.chapter=chapter; self.verse=verse
        self.original_text=original_text
        self._current=ov.get(translation,book_id,chapter,verse) or original_text
    def compose(self) -> ComposeResult:
        has_ov=ov.get(self.translation,self.book_id,self.chapter,self.verse) is not None
        with Vertical(id="ov-box"):
            yield Label(f"✍  {self.book_name} {self.chapter}:{self.verse}  [{self.translation}]",id="ov-title")
            yield Label(f"[dim]Original: {self.original_text[:120]}{'…' if len(self.original_text)>120 else ''}[/dim]",id="ov-original")
            yield TextArea(self._current,id="ov-area")
            with Horizontal(id="ov-foot"):
                if has_ov: yield Button("↩ Restaurar",id="ov-restore",variant="warning")
                yield Button("💾 Guardar",id="ov-save",variant="primary"); yield Button("Cancelar",id="ov-cancel")
    def on_mount(self): self.query_one("#ov-area",TextArea).focus()
    @on(Button.Pressed,"#ov-save")
    def save(self):
        text=self.query_one("#ov-area",TextArea).text.strip()
        if text and text!=self.original_text: ov.set(self.translation,self.book_id,self.chapter,self.verse,text)
        self.dismiss(True)
    @on(Button.Pressed,"#ov-restore")
    def restore(self): ov.delete(self.translation,self.book_id,self.chapter,self.verse); self.dismiss(True)
    @on(Button.Pressed,"#ov-cancel")
    def cancel(self): self.dismiss(None)