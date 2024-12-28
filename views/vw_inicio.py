from flet import Page, Container, Text
from .vmodels.view_factory import ViewFactory
from .vmodels.vmd_tabelas import TabelaAlunos


class Inicio:
    def __init__(self, page: Page):
        self.page = page

        self.tabela = TabelaAlunos(page, colunas=['id', 'série', 'nome', 'pontos', 'status'])

        self.get = ViewFactory.get_view(page, view_controls=[self.container_main()], view_name='Início')

    def container_main(self) -> Container:
        return Container(
            Text('inicio')
        )
