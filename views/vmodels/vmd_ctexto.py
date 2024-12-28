from flet import TextField, Page, Colors, FontWeight, TextStyle, InputBorder, padding
from abc import ABC, abstractmethod

ALTURA_PADRAO = 30
LARGURA_PADRAO = 400
RAIO_BORDA = 7
EXPESSURA_BORDA = 1
EXPESSURA_BORDA_FOCADA = 3

class _CTexto(ABC):
    def __init__(self, page: Page, label: str, altura: int = ALTURA_PADRAO, largura: int = LARGURA_PADRAO, senha: bool = False):
        self.page = page

        self.label = label
        self.altura = altura
        self.largura = largura
        self.senha= senha

        self.get = self._get()

    def _get(self) -> TextField:
        return TextField(
            label=self.label,
            width=self.largura,
            height=self.altura,
            text_style=TextStyle(font_family='nunito', color=Colors.PRIMARY, weight=FontWeight.W_500),
            label_style=TextStyle(font_family='nunito', color=Colors.PRIMARY, weight=FontWeight.W_700),
            border=InputBorder.UNDERLINE,
            border_radius=RAIO_BORDA,
            border_color=Colors.PRIMARY,
            border_width=EXPESSURA_BORDA,
            focused_border_width=EXPESSURA_BORDA_FOCADA,
            password=self.senha,
            can_reveal_password=self.senha,
            cursor_width=.6,
            bgcolor=Colors.with_opacity(opacity=.1, color=Colors.PRIMARY),
            content_padding=padding.only(bottom=15, left=5),

        )

class CTexto(_CTexto):
    def __init__(self, page: Page, label: str, altura: int = ALTURA_PADRAO, largura: int = LARGURA_PADRAO):
        super().__init__(page, label, altura, largura)
