from flet import Page, Container, Text, padding, Row
from .vmodels.view_factory import ViewFactory
from .vmodels.vmd_tabelas import TabelaAlunos
from .vmodels.vmd_escolhas import EscolhaSerieSincronizadoComEscolhaAluno, EscolhaAlunos


class Alunos:
    def __init__(self, page: Page):
        self.page = page

        self.escolha_aluno = EscolhaAlunos(page=page, label='Aluno')
        self.escolha_serie = EscolhaSerieSincronizadoComEscolhaAluno(page=page, label='Série', escolha_aluno=self.escolha_aluno)

        self.tabela = TabelaAlunos(page, colunas=['id', 'série', 'nome', 'pontos', 'status'])

        self.get = ViewFactory.get_view(page, view_controls=[self.container_adicionar_aluno(),
                                                             self.container_lista_de_alunos(),], view_name='Alunos')

    def container_adicionar_aluno(self) -> Container:
        return Container(
            Row(controls=[self.escolha_serie.get, self.escolha_aluno.get]),
            padding=padding.only(top=10)
        )

    def container_lista_de_alunos(self) -> Container:
        return Container(
            self.tabela.get
        )
