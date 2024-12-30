from flet import Dropdown, Page, Colors, dropdown, TextStyle, InputBorder, FontWeight, ControlEvent, padding, alignment
from abc import ABC, abstractmethod
from models.md_serie import ler_series
from models.md_aluno import ler_aluno

ALTURA_PADRAO = 35
LARGURA_PADRAO = 100
RAIO_BORDA = 7
EXPESSURA_BORDA = 1
EXPESSURA_BORDA_FOCADA = 3


class _Escolha(ABC):
    def __init__(self, page: Page, label: str, altura: int = ALTURA_PADRAO, largura: int = LARGURA_PADRAO):
        self.page = page
        self.label = label
        self.altura = altura
        self.largura = largura

        self.get = self._get()


    def valor(self):
        return self.get.value

    def populate_dropdown(self, options: list[str]):
        for option in options:
            self.get.options.append(
                dropdown.Option(option)
            )
        self.page.update()

    def _get(self):
        return Dropdown(
            label=self.label,
            height=self.altura,
            width=self.largura,
            text_style=TextStyle(font_family='nunito', color=Colors.PRIMARY, weight=FontWeight.W_500),
            label_style=TextStyle(font_family='nunito', color=Colors.PRIMARY, weight=FontWeight.W_700),
            fill_color=Colors.with_opacity(opacity=.1, color=Colors.PRIMARY),
            icon_enabled_color=Colors.PRIMARY,
            border=InputBorder.UNDERLINE,
            border_radius=RAIO_BORDA,
            border_color=Colors.PRIMARY,
            border_width=EXPESSURA_BORDA,
            focused_border_width=EXPESSURA_BORDA_FOCADA,
            on_change=lambda e: self._on_change(e),
            content_padding=padding.only(bottom=13, left=5),
        )

    @abstractmethod
    def _on_change(self, e: ControlEvent):
        ...


class EscolhaSerie(_Escolha):
    def __init__(self, page: Page, label: str, altura: int = ALTURA_PADRAO, largura: int = LARGURA_PADRAO):
        super().__init__(page, label, altura, largura)
        self.populate_dropdown(ler_series()[1])  # type: ignore

    def _on_change(self, e):
        pass


class EscolhaAlunos(_Escolha):
    def __init__(self, page: Page, label: str, altura: int = ALTURA_PADRAO, largura: int = LARGURA_PADRAO*3):
        super().__init__(page, label, altura, largura)

    def populate_dropdown(self, serie: str):
        alunos = ler_aluno(serie=serie)

        self.get.options.clear()
        for aluno in alunos[1]:
            self.get.options.append(dropdown.Option(aluno.nome))
        self.page.update()

    def _on_change(self, e):
        pass


class EscolhaSerieSincronizadoComEscolhaAluno(_Escolha):
    def __init__(self, page: Page, label: str, escolha_aluno: EscolhaAlunos, altura: int = ALTURA_PADRAO, largura: int = LARGURA_PADRAO):
        super().__init__(page, label, altura, largura)
        self.populate_dropdown(ler_series()[1])  # type: ignore
        self.escolha_aluno = escolha_aluno

    def _on_change(self, e):
        self.escolha_aluno.populate_dropdown(serie=self.get.value)
