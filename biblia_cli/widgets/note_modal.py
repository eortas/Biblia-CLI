from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Label, TextArea
from textual.containers import Vertical, Horizontal
from ..notes import get_note, save_note, delete_note

class NoteModal(ModalScreen):
    DEFAULT_CSS="""
    NoteModal { align: center middle; }
    #n-box { width: 72; height: auto; background: $surface; border: thick $primary; padding: 1 2; }
    #n-title { text-style: bold; color: $accent; text-align: center; width: 100%; margin-bottom: 1; }
    #n-ref { color: $text-muted; text-align: center; width: 100%; margin-bottom: 1; }
    #n-area { height: 12; border: solid $primary; margin-bottom: 1; }
    #n-foot { height: 3; align: right middle; }
    #n-delete { margin-right: 1; }
    """
    def __init__(self,translation,book_id,book_name,chapter,verse):
        super().__init__(); self.translation=translation; self.book_id=book_id
        self.book_name=book_name; self.chapter=chapter; self.verse=verse
        self._existing=get_note(translation,book_id,chapter,verse) or ""
    def compose(self) -> ComposeResult:
        with Vertical(id="n-box"):
            yield Label("✏️  Nota personal",id="n-title")
            yield Label(f"[dim]{self.book_name} {self.chapter}:{self.verse}  [{self.translation}][/dim]",id="n-ref")
            yield TextArea(self._existing,id="n-area",language=None)
            with Horizontal(id="n-foot"):
                if self._existing: yield Button("🗑 Eliminar",id="n-delete",variant="error")
                yield Button("💾 Guardar",id="n-save",variant="primary"); yield Button("Cancelar",id="n-cancel")
    def on_mount(self): self.query_one("#n-area",TextArea).focus()
    @on(Button.Pressed,"#n-save")
    def save(self):
        text=self.query_one("#n-area",TextArea).text.strip()
        if text: save_note(self.translation,self.book_id,self.chapter,self.verse,self.book_name,text)
        self.dismiss(True)
    @on(Button.Pressed,"#n-delete")
    def delete(self): delete_note(self.translation,self.book_id,self.chapter,self.verse); self.dismiss(True)
    @on(Button.Pressed,"#n-cancel")
    def cancel(self): self.dismiss(None)