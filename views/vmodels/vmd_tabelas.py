from abc import ABC, abstractmethod
from flet import DataTable, DataRow, DataColumn, DataCell, Page, Text, colors, FontWeight, ControlEvent, Colors
from models.md_aluno import ler_aluno


ALTURA_CABECALHO = 30
ALTURA_LINHA = 30


class _Tabela(ABC):
    def __init__(self, page: Page, colunas: list[str], altura_cabecalho: int = ALTURA_CABECALHO,
                 altura_linha: int = ALTURA_LINHA, largura_tabela: int = None):
        self.page = page
        self.colunas = colunas
        self.altura_cabecalho = altura_cabecalho
        self.altura_linha = altura_linha
        self.largura_tabela = largura_tabela

        self.get = self._get()

    @abstractmethod
    def _on_row_click(self, e: ControlEvent):
        pass

    def populate_table(self, valores: list[list | tuple]):
        self.get.rows.clear()
        for valor in valores:
            self.get.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(value=item)) for item in valor
                    ],
                    on_select_changed=lambda e: self._on_row_click(e)
                )
            )

        self.page.update()

    def _get(self) -> DataTable:
        return DataTable(
            heading_row_color=colors.PRIMARY,
            heading_row_height=self.altura_cabecalho,
            columns=[
                DataColumn(
                    Text(value=coluna.capitalize(), font_family='nunito', color=colors.ON_PRIMARY, weight=FontWeight.BOLD),
                )
                for coluna in self.colunas
            ],
            rows=[],
            data_row_min_height=self.altura_linha,
            data_row_max_height=self.altura_linha,
            width=self.largura_tabela,
        )


class TabelaAlunos(_Tabela):
    def __init__(self, page: Page, colunas: list[str], altura_cabecalho: int = ALTURA_CABECALHO,
                 altura_linha: int = ALTURA_LINHA, largura_tabela: int = None):
        super().__init__(page=page, colunas=colunas, altura_cabecalho=altura_cabecalho, altura_linha=altura_linha, largura_tabela=largura_tabela)

        alunos = ler_aluno()
        lista_alunos = []

        if alunos[0]:
            for aluno in alunos[1]:
                lista_alunos.append([aluno.id, aluno.serie, aluno.nome, aluno.pontos, 'ativo' if aluno.status else 'inativo'])

            self.populate_table(lista_alunos)

    def populate_table(self, valores: list[list | tuple]):
        self.get.rows.clear()
        for valor in valores:
            self.get.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(value=item)) for item in valor
                    ],
                    on_select_changed=lambda e: self._on_row_click(e),
                    color=Colors.with_opacity(opacity=.1, color=Colors.SHADOW) if valor[-1] == 'inativo' else Colors.with_opacity(
                        opacity=.05, color=Colors.PRIMARY_CONTAINER),
                )
            )

        self.page.update()

    def _on_row_click(self, e: ControlEvent):
        # TODO: Implementar o DialogAlert com informações do aluno selecionado
        pass
