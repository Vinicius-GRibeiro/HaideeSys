from flet import Page, Container, Text
from .vmodels.view_factory import ViewFactory
from .vmodels.vmd_botoes import BotaoTextoAdicionarSerie
from .vmodels.vmd_escolhas import EscolhaSerieEstatisticas
from .vmodels.vmd_tabelas import TabelaEstatisticaserie
from flet import Container, Row, Colors, Column, FontWeight


class Turmas:
    def __init__(self, page: Page):
        self.page = page

        self.tabela_estatisticas_series = TabelaEstatisticaserie(self.page)
        self.escolha_serie = EscolhaSerieEstatisticas(self.page, 'Séries disponíveis', largura=200, tabela_estatistica=self.tabela_estatisticas_series, altura=40)


        self.get = ViewFactory.get_view(page, view_controls=[self.container_main()], view_name='Turmas')

    def container_main(self) -> Container:
        return Container(
            bgcolor=Colors.with_opacity(.08, Colors.TERTIARY),
            padding=20,
            border_radius=10,
            content=Column(
                width=720,
                controls=[
                    Text('Séries', font_family='nunito', color=Colors.PRIMARY, weight=FontWeight.W_800,
                         size=17),
                    Row(
                        controls=[
                            self.escolha_serie.get,
                            self.tabela_estatisticas_series.get
                        ]
                    ),
                ]
            )
        )