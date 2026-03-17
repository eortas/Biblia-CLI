from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, TextArea
from .. import annotations as ann

class AnnotationReadModal(ModalScreen):
    DEFAULT_CSS="""
    AnnotationReadModal { align: center middle; }
    #ar-box { width: 70; height: auto; max-height: 30; background: $surface; border: thick $primary; padding: 1 2; }
    #ar-ref  { text-style: bold; color: $accent; margin-bottom: 1; }
    #ar-scroll { height: 1fr; margin-bottom: 1; overflow-y: auto; }
    #ar-body { color: $text; padding: 0 1; width: 100%; height: auto; }
    #ar-foot { height: 3; align: right middle; }
    """
    def __init__(self,book_name,chapter,verse,text):
        super().__init__(); self._ref=f"{book_name} {chapter}:{verse}"; self._text=text
    def compose(self) -> ComposeResult:
        from textual.containers import VerticalScroll
        import re
        with Vertical(id="ar-box"):
            yield Label(f"✦  {self._ref}",id="ar-ref")
            with VerticalScroll(id="ar-scroll"):
                yield Label(re.sub(r'\n+', '\n\n', self._text.strip()), id="ar-body", markup=False)
            with Horizontal(id="ar-foot"): yield Button("Cerrar",id="ar-close",variant="primary")
    @on(Button.Pressed,"#ar-close")
    def close(self): self.dismiss(None)

class AnnotationWriteModal(ModalScreen):
    DEFAULT_CSS="""
    AnnotationWriteModal { align: center middle; }
    #aw-box { width: 74; height: auto; background: $surface; border: thick $primary; padding: 1 2; }
    #aw-title { text-style: bold; color: $accent; text-align: center; width: 100%; margin-bottom: 1; }
    #aw-area { height: 12; border: solid $primary; margin-bottom: 1; }
    #aw-foot { height: 3; align: right middle; }
    #aw-del  { margin-right: 1; }
    """
    def __init__(self,translation,book_id,book_name,chapter,verse):
        super().__init__(); self.translation=translation; self.book_id=book_id
        self.book_name=book_name; self.chapter=chapter; self.verse=verse
        self._existing=ann.get_note_local(translation,book_id,chapter,verse) or ""
    def compose(self) -> ComposeResult:
        with Vertical(id="aw-box"):
            yield Label(f"✦  Nota de autor — {self.book_name} {self.chapter}:{self.verse}",id="aw-title")
            yield TextArea(self._existing,id="aw-area")
            with Horizontal(id="aw-foot"):
                if self._existing: yield Button("🗑 Eliminar",id="aw-del",variant="error")
                yield Button("💾 Publicar",id="aw-save",variant="primary"); yield Button("Cancelar",id="aw-cancel")
    def on_mount(self): self.query_one("#aw-area",TextArea).focus()
    @on(Button.Pressed,"#aw-save")
    def save(self):
        text=self.query_one("#aw-area",TextArea).text.strip()
        if text: ann.save_local(self.translation,self.book_id,self.chapter,self.verse,text)
        self.dismiss(True)
    @on(Button.Pressed,"#aw-del")
    def delete(self): ann.delete_local(self.translation,self.book_id,self.chapter,self.verse); self.dismiss(True)
    @on(Button.Pressed,"#aw-cancel")
    def cancel(self): self.dismiss(None)