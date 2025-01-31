from flet import Page, Container, Text, Row, Colors, Column, FontWeight, ExpansionTile, ScrollMode, TextAlign, MainAxisAlignment
from .vmodels.view_factory import ViewFactory
from .vmodels.vmd_botoes import BotaoTextoAdicionarSerie, BotaoGravarChamada, BotaoIconePesquisarChamada, BotaoIconeRelatorioChamada
from .vmodels.vmd_escolhas import EscolhaSerieEstatisticas, EscolhaSerieChamada, EscolhaSerieGerenciarChamada
from .vmodels.vmd_tabelas import TabelaEstatisticaserie, TabelaChamadaAlunos, TabelaChamadaRegistros
from .vmodels.vmd_ctexto import CTexto
from datetime import datetime


class Turmas:
    def __init__(self, page: Page):
        self.page = page

        self.serie = CTexto(self.page, label='Nova série', largura=100, altura=40)
        self.tabela_estatisticas_series = TabelaEstatisticaserie(self.page)
        self.escolha_serie = EscolhaSerieEstatisticas(self.page, 'Séries disponíveis', largura=200, tabela_estatistica=self.tabela_estatisticas_series, altura=40)
        self.btn_add_series = BotaoTextoAdicionarSerie(self.page, '+', largura=50, ctrl_serie=self.serie, ctrl_escolher_serie=self.escolha_serie)

        self.chamada_data = CTexto(self.page, label='Data', largura=150, altura=35)
        self.chamada_data.get.value = datetime.today().strftime('%d/%m/%Y')
        self.chamada_tabela_alunos = TabelaChamadaAlunos(self.page)
        self.chamada_escollha_serie = EscolhaSerieChamada(self.page, label='Série', ctrl_tabela=self.chamada_tabela_alunos)
        self.btn_gravar_chamada = BotaoGravarChamada(self.page, label='Gravar chamada', ctrl_tabela=self.chamada_tabela_alunos, ctrl_data=self.chamada_data, ctrl_serie=self.chamada_escollha_serie)

        self.tabela_gerenciar_chamadas = TabelaChamadaRegistros(self.page)
        self.escolha_gerenciar_serie = EscolhaSerieGerenciarChamada(self.page, 'Série', ctrl_tabela=self.tabela_gerenciar_chamadas, largura=300)
        self.btn_pesquisar_chamadas = BotaoIconePesquisarChamada(self.page, ctrl_serie=self.escolha_gerenciar_serie, ctrl_tabela=self.tabela_gerenciar_chamadas)
        self.btn_gerar_relatorio = BotaoIconeRelatorioChamada(self.page)

        self.get = ViewFactory.get_view(page, view_controls=[self.container_estatisticas(), self.container_chamada()], view_name='Turmas')

    def container_estatisticas(self) -> Container:
        return Container(
            bgcolor=Colors.with_opacity(.08, Colors.TERTIARY),
            padding=10,
            border_radius=10,
            width=920,
            content=Column(
                        width=920,
                        controls=[
                            Text('Séries', font_family='nunito', color=Colors.PRIMARY, weight=FontWeight.W_800, size=17),
                            Row(
                                controls=[
                                    self.serie.get,
                                    self.btn_add_series.get,
                                    Container(width=30, height=1),
                                    self.escolha_serie.get,
                                    Container(width=5, height=1),
                                    self.tabela_estatisticas_series.get
                                ]
                            ),
                        ]
                    )
        )

    def container_chamada(self) -> Container:
        return Container(
            bgcolor=Colors.with_opacity(.08, Colors.TERTIARY),
            padding=10,
            border_radius=10,
            width=920,
            content=Row(
                width=920,
                controls=[
                    Column(
                        width=450,
                        controls=[
                            Container(
                                content=Text('Realizar chamada',font_family='nunito', color=Colors.ON_PRIMARY, weight=FontWeight.W_700,
                                 width=440, text_align=TextAlign.CENTER),
                                bgcolor=Colors.PRIMARY
                            ),

                            Row(
                                controls=[
                                    self.chamada_escollha_serie.get,
                                    self.chamada_data.get,
                                    self.btn_gravar_chamada.get
                                ],
                                alignment=MainAxisAlignment.SPACE_EVENLY
                            ),

                            Column(
                                height=400,
                                controls=[
                                    self.chamada_tabela_alunos.get
                                ],
                                scroll=ScrollMode.AUTO
                            )
                        ]
                    ),

                    Column(
                        width=450,
                        controls=[
                            Container(
                                content=Text('Gerenciar chamadas', font_family='nunito', color=Colors.ON_PRIMARY,
                                             weight=FontWeight.W_700,
                                             width=440, text_align=TextAlign.CENTER),
                                bgcolor=Colors.PRIMARY
                            ),

                            Row(
                                alignment=MainAxisAlignment.SPACE_EVENLY,
                                width=440,
                                controls=[
                                    self.escolha_gerenciar_serie.get,
                                    self.btn_pesquisar_chamadas.get,
                                    self.btn_gerar_relatorio.get
                                ]
                            ),

                            Column(
                                height=400,
                                controls=[
                                    self.tabela_gerenciar_chamadas.get
                                ],
                                scroll=ScrollMode.AUTO
                            )
                        ]
                    )
                ]
            )
        )