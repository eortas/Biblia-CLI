from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual.containers import Center, Middle
from textual import work
import asyncio

CROSS = """\
          ███          
          ███          
          ███          
          ███          
  ████████████████████ 
  ████████████████████ 
          ███          
          ███          
          ███          
          ███          
          ███          
          ███          """

TITLE = """\
 ████   ████▄    ███    █████  █████    ████  
█       █   █     █    █         █     █    █ 
█       ████▀     █     ████     █     █    █ 
█       █  █      █         █    █     █    █ 
 ████   █   █    ███    █████    █      ████  """

TAGLINE = "La Palabra, al alcance de tu mano"


class SplashScreen(Screen):
    DEFAULT_CSS = """
    SplashScreen {
        align: center middle;
        background: #0d0d0d;
    }
    SplashScreen.theme-light {
        background: #f4f4f4;
    }
    #sp-cross {
        text-align: center;
        color: #888888;
        text-style: bold;
        padding-bottom: 1;
        width: auto;
    }
    .theme-light #sp-cross {
        color: #aaaaaa;
    }
    #sp-title {
        text-align: center;
        color: #ffffff;
        text-style: bold;
        width: auto;
    }
    .theme-light #sp-title {
        color: #1a5fa8;
    }
    #sp-tagline {
        text-align: center;
        color: #444444;
        padding-top: 1;
        width: auto;
    }
    .theme-light #sp-tagline {
        color: #666666;
    }
    """

    def compose(self) -> ComposeResult:
        with Center():
            with Middle():
                yield Static("", id="sp-cross")
                yield Static("", id="sp-title")
                yield Static("", id="sp-tagline")

    def on_mount(self) -> None:
        self.run_worker(self.play_splash_animation())

    async def play_splash_animation(self) -> None:
        cross_w  = self.query_one("#sp-cross",   Static)
        title_w  = self.query_one("#sp-title",   Static)
        tagline_w= self.query_one("#sp-tagline", Static)

        # 1. Fade-in de la cruz línea a línea
        cross_lines = CROSS.splitlines()
        for i in range(1, len(cross_lines) + 1):
            cross_w.update("\n".join(cross_lines[:i]))
            await asyncio.sleep(0.06)

        await asyncio.sleep(0.15)

        # 2. Aparece el título completo de golpe
        title_w.update(f"[bold white]{TITLE}[/bold white]")
        await asyncio.sleep(0.2)

        # 3. Tagline letra a letra
        for i in range(1, len(TAGLINE) + 1):
            tagline_w.update(f"[dim]{TAGLINE[:i]}[/dim]")
            await asyncio.sleep(0.03)

        await asyncio.sleep(2.5)
        self.dismiss()