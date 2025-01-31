from flet import Page, Container, Text, Colors, Row, FontWeight, Column
from flet.core.types import ScrollMode

from .vmodels.view_factory import ViewFactory
from .vmodels.vmd_escolhas import EscolhaAlunos, EscolhaSerieSincronizadoComEscolhaAluno, EscolhaDescricaoPontos, EscolhaTipoSincronizadoComDescricaoPontos
from .vmodels.vmd_botoes import BotaoIconePesquisarPontosAluno, BotaoTextoMudarPontuacao, BotaoIconeRedefinirSerieAlunoPontos
from .vmodels.vmd_ctexto import CTexto
from .vmodels.vmd_tabelas import TabelaRegistrosPontos


class Pontos:
    def __init__(self, page: Page):
        self.page = page

        self.tabela_pontuacao = TabelaRegistrosPontos(self.page, largura=900)
        self.aluno = EscolhaAlunos(self.page, label='Aluno', largura=600)
        self.serie = EscolhaSerieSincronizadoComEscolhaAluno(self.page, label='Série', escolha_aluno=self.aluno, largura=200, somente_ativos=True)
        self.btn_pesquisar_pontos = BotaoIconePesquisarPontosAluno(self.page, serie=self.serie, aluno=self.aluno, tabela_pontucoes=self.tabela_pontuacao)
        self.btn_redefinir_serie_aluno = BotaoIconeRedefinirSerieAlunoPontos(self.page, serie=self.serie, aluno=self.aluno, tabela=self.tabela_pontuacao)

        self.txt_qntd_pontos = CTexto(self.page, label='Pontos', largura=100)
        self.escolha_descricao = EscolhaDescricaoPontos(self.page, 'Descrição', largura=500, pontos=self.txt_qntd_pontos)
        self.escolha_tipo = EscolhaTipoSincronizadoComDescricaoPontos(self.page, 'Tipo', escolha_descricao=self.escolha_descricao, largura=100)

        self.btn_mudar_pontos = BotaoTextoMudarPontuacao(self.page, label='Salvar', largura=150, serie=self.serie, aluno=self.aluno, tipo=self.escolha_tipo, descricao=self.escolha_descricao, pontos=self.txt_qntd_pontos)

        self.get = ViewFactory.get_view(page, view_controls=[self.container_main()], view_name='Pontos')

    def container_main(self) -> Container:
        return Container(
            bgcolor=Colors.with_opacity(.08, Colors.TERTIARY),
            padding=20,
            border_radius=10,
            width=950,
            content= Column(
                controls=[
                    Text('Adicionar ou remover pontos', font_family='nunito', color=Colors.PRIMARY, weight=FontWeight.W_800, size=17),
                    Row(
                        controls=[
                            self.serie.get, self.aluno.get, self.btn_pesquisar_pontos.get, self.btn_redefinir_serie_aluno.get
                        ]
                    ),

                    Row(
                        controls=[
                            self.escolha_tipo.get, self.escolha_descricao.get, self.txt_qntd_pontos.get, self.btn_mudar_pontos.get
                        ]
                    ),

                    Container(height=10, width=1),

                    Column(
                        height=450,
                        controls=[
                            self.tabela_pontuacao.get
                        ],
                        scroll=ScrollMode.AUTO
                    )
                ]
            )
        )
