from flet import (TextButton, Row, Page, ButtonStyle, Colors, ControlState, RoundedRectangleBorder,
                  RadioGroup, Radio, IconButton)
from abc import ABC, abstractmethod


LARGURA_PADRAO = 135
TAMANHO_ICONE_BOTAO = 28


class _BotaoTexto(ABC):
    def __init__(self, page: Page, label: str, largura: int = LARGURA_PADRAO):
        self.page = page

        self.label = label
        self.largura = largura

        self.get = self._get()

    def _get(self) -> TextButton:
        return TextButton(
            text=self.label,
            style=ButtonStyle(
                bgcolor={
                    ControlState.DEFAULT: Colors.PRIMARY,
                    ControlState.HOVERED: Colors.with_opacity(.8, Colors.PRIMARY),
                },
                color=Colors.ON_PRIMARY,
                shape=RoundedRectangleBorder(5)
            ),

            width=self.largura,
            on_click=lambda e: self._on_click(e)
        )

    @abstractmethod
    def _on_click(self, e: ControlState):
        ...


class _BotaoIcone(ABC):
    def __init__(self, page: Page, icone: str, tamanho: int = TAMANHO_ICONE_BOTAO):
        self.page = page

        self.icone = icone
        self.tamanho = tamanho

        self.get = self._get()

    def _get(self) -> IconButton:
        return IconButton(
            icon=self.icone,
            icon_color=Colors.PRIMARY,
            on_click=lambda e: self._on_click(e),
            icon_size=self.tamanho,
        )

    @abstractmethod
    def _on_click(self, e: ControlState):
        pass


class BotaoTextoSalvarAluno(_BotaoTexto):
    def __init__(self, page: Page, label: str):
        super().__init__(page, label)

    def _on_click(self, e: ControlState):
        ...


class BotaoIconePesquisarAluno(_BotaoIcone):
    def __init__(self, page: Page, icone: str, tamanho: int = TAMANHO_ICONE_BOTAO):
        super().__init__(page, icone, tamanho)

    def _on_click(self, e: ControlState):
        ...


class BotaoIconeLimparFiltros(_BotaoIcone):
    def __init__(self, page: Page, icone: str, tamanho: int = TAMANHO_ICONE_BOTAO):
        super().__init__(page, icone, tamanho)

    def _on_click(self, e: ControlState):
        ...


class BotaoRadio:
    def __init__(self, page: Page, opcoes: dict[str, str], valor_padrao: str = None):
        self.page = page

        self.opcoes = opcoes
        self.valor_padrao = valor_padrao

        self.get = self._get()

    def _get(self) -> RadioGroup:
        return RadioGroup(
            content=Row(
                controls=[Radio(value=item[0], label=item[1]) for item in self.opcoes.items()]
            ),

        )

