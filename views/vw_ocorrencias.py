from flet import Page, Container, Column, Colors, Row
from flet.core.types import MainAxisAlignment, ScrollMode
from .vmodels.view_factory import ViewFactory
from .vmodels.vmd_ctexto import CTexto
from .vmodels.vmd_tabelas import TabelaAlunosDaOcorrencia, TabelaOcorrencias
from .vmodels.vmd_botoes import BotaoIconeAdicionarAlunoNaOcorrencia, BotaoIconePesquisarOcorrencia, BotaoTextoAdicionarOcorrencia, BotaoIconeRedefinirOcorrencias
from .vmodels.vmd_escolhas import EscolhaAlunos, EscolhaSerieSincronizadoComEscolhaAluno, EscolhaSerie


class Ocorrencias:
    def __init__(self, page: Page):
        self.page = page

        self.consultar_nome = EscolhaAlunos(self.page, label='Nome', largura=400)
        self.consultar_serie = EscolhaSerieSincronizadoComEscolhaAluno(self.page, label='Serie', largura=200, escolha_aluno=self.consultar_nome)
        self.tabela_ocorrencias = TabelaOcorrencias(self.page, 900)
        self.btn_pesquisar_ocorrencias = BotaoIconePesquisarOcorrencia(self.page, serie=self.consultar_serie, aluno=self.consultar_nome, tabela_ocorrencias=self.tabela_ocorrencias)
        self.btn_adicionar_ocorrencia = BotaoTextoAdicionarOcorrencia(self.page, label='+ Nova ocorrência', largura=150, tabela_ocorrencias=self.tabela_ocorrencias)
        self.btn_redefinir_ocorrencias = BotaoIconeRedefinirOcorrencias(self.page, tabela_ocorrencias=self.tabela_ocorrencias, serie=self.consultar_serie, aluno=self.consultar_nome)

        self.get = ViewFactory.get_view(page, view_controls=[self.container_add_ocorrencia(), self.container_tabela_ocorrencias()], view_name='Ocorrências')

    def container_add_ocorrencia(self) -> Container:
        return Container(
            bgcolor=Colors.with_opacity(.08, Colors.TERTIARY),
            padding=10,
            border_radius=10,
            width=920,
            content=Column(
                controls=[
                    Row(
                        controls=[
                            Row([self.consultar_serie.get, self.consultar_nome.get, self.btn_pesquisar_ocorrencias.get, self.btn_redefinir_ocorrencias.get]), self.btn_adicionar_ocorrencia.get
                        ],
                        width=900,
                        alignment=MainAxisAlignment.SPACE_BETWEEN
                    ),
                ]
            )
        )

    def container_tabela_ocorrencias(self) -> Container:
        return Container(
            bgcolor=Colors.with_opacity(.08, Colors.TERTIARY),
            padding=10,
            border_radius=10,
            width=920,
            content=Column(
                controls=[
                    self.tabela_ocorrencias.get
                ],
                height=550,
                scroll=ScrollMode.AUTO
            )
        )
