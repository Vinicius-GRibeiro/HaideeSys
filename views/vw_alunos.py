from flet import Page, Container, Text, padding, Row, Column, Colors, FontWeight, ScrollMode, MainAxisAlignment, icons
from .vmodels.view_factory import ViewFactory
from .vmodels.vmd_tabelas import TabelaAlunos
from .vmodels.vmd_escolhas import EscolhaSerie
from .vmodels.vmd_ctexto import CTexto
from .vmodels.vmd_botoes import BotaoTextoSalvarAluno, BotaoRadio, BotaoIconePesquisarAluno, BotaoIconeLimparFiltros


class Alunos:
    def __init__(self, page: Page):
        self.page = page

        self.tabela = TabelaAlunos(page, colunas=['id', 'série', 'nome', 'pontos', 'status'], largura_tabela=870)

        self.escolha_serie = EscolhaSerie(page=page, label='Série')
        self.escolha_serie_pesquisa = EscolhaSerie(page=page, label='Série')
        self.nome = CTexto(page=self.page, label='Nome', largura=450)
        self.nome_pesquisa = CTexto(page=self.page, label='Nome', largura=350)
        self.laudo = CTexto(page=self.page, label='Laudo', largura=300)
        self.obs = CTexto(page=self.page, label='Observações', largura=720)

        self.btn_salvar_aluno = BotaoTextoSalvarAluno(page=self.page, label='Salvar', ctrl_serie=self.escolha_serie,
                                                      ctrl_nome=self.nome, ctrl_laudo=self.laudo, ctrl_obs=self.obs, ctrl_tabela=self.tabela,)
        self.btn_radio_filtros = BotaoRadio(page=self.page, opcoes={'nome': 'Nome', 'serie': 'Série', 'pontos': 'Pontos', 'status': 'Status'})
        self.btn_radio_filtros.get.value = 'nome'
        self.btn_pesquisar_aluno = BotaoIconePesquisarAluno(page=self.page, icone=icons.SEARCH_ROUNDED, ctrl_serie=self.escolha_serie_pesquisa, ctrl_nome=self.nome_pesquisa, ctrl_ordenar_por=self.btn_radio_filtros, ctrl_tabela=self.tabela)
        self.btn_limpar_filtros = BotaoIconeLimparFiltros(page=self.page, icone=icons.REFRESH_ROUNDED, ctrl_tabela=self.tabela, controles=[self.escolha_serie_pesquisa, self.nome_pesquisa], controle_radio=self.btn_radio_filtros)

        self.get = ViewFactory.get_view(page, view_controls=[
            self.container_adicionar_aluno(),
            self.container_pesquisar_alunos(),],
        view_name='Alunos')

    def container_adicionar_aluno(self) -> Container:
        return Container(
            bgcolor=Colors.with_opacity(.08, Colors.TERTIARY),
            padding=20,
            border_radius=10,
            content= Column(
                controls=[
                    Text('Adicionar aluno', font_family='nunito', color=Colors.PRIMARY, weight=FontWeight.W_800, size=17),
                    Row(controls=[self.escolha_serie.get, self.nome.get, self.laudo.get]),
                    Row(controls=[self.obs.get, self.btn_salvar_aluno.get]),
                ]
            )
        )

    def container_pesquisar_alunos(self) -> Container:
        return Container(
            content=Column(
                controls=[
                    Column(
                        spacing=0,
                        controls=[
                            Row(
                                controls=[
                                    Container(
                                        content=Text('Ordenar por', font_family='nunito', color=Colors.PRIMARY, weight=FontWeight.W_500),
                                        padding=padding.only(left=470)
                                    )
                                ],
                                alignment=MainAxisAlignment.END
                            ),

                            Row(
                                controls=[
                                    self.escolha_serie_pesquisa.get,
                                    self.nome_pesquisa.get,
                                    self.btn_radio_filtros.get,
                                    Row(
                                        spacing=0,
                                        controls=[
                                            self.btn_pesquisar_aluno.get,
                                            self.btn_limpar_filtros.get
                                        ]
                                    )
                                ]
                            ),
                        ]
                    ),

                    Column(
                        height=390,
                        scroll=ScrollMode.AUTO,
                        controls=[
                            self.tabela.get
                        ]
                    )

                ]
            ),
            bgcolor=Colors.with_opacity(.08, Colors.TERTIARY),
            padding=20,
            border_radius=10,
        )
