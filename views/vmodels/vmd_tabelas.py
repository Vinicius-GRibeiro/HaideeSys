from abc import ABC, abstractmethod
from flet import (DataTable, DataRow, DataColumn, DataCell, Page, Text, colors, FontWeight, ControlEvent,
                  Colors, Column, Container, TextAlign, CrossAxisAlignment, Row, padding, ButtonStyle, BorderSide, RoundedRectangleBorder)
from flet.core.types import MainAxisAlignment
from models.md_aluno import ler_aluno
from .vmd_detalhes import DetalhesAluno
from .vmd_ctexto import CTexto
from .vmd_escolhas import EscolhaSerie

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

    def populate_table(self, valores: list[list | tuple] = None):
        self.get.rows.clear()

        if valores is None:
            alunos = ler_aluno()
            lista_alunos = []

            if alunos[0]:
                for aluno in alunos[1]:
                    lista_alunos.append(
                        [aluno.id, aluno.serie, aluno.nome, aluno.pontos, 'ativo' if aluno.status else 'inativo'])

                self.populate_table(lista_alunos)
            self.page.update()
            return

        for valor in valores:
            self.get.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(value=item)) for item in valor
                    ],
                    on_select_changed=lambda e: self._on_row_click(e),
                    color=Colors.ERROR_CONTAINER if valor[-1] == 'inativo' else Colors.with_opacity(
                        opacity=.05, color=Colors.PRIMARY_CONTAINER),
                )
            )

        self.page.update()

    def _on_row_click(self, e: ControlEvent):
        from .vmd_botoes import BotaoTextoSalvarAlteracoesAluno, BotaoTextoInativarAluno

        ALTURA_COLUNA = 500
        LARGURA_COLUNA = 600

        detalhes_aluno = DetalhesAluno(self.page).get
        id_aluno = e.control.cells[0].content.value

        aluno = ler_aluno(id_=id_aluno)
        if aluno[0]:
            aluno_obj = aluno[1][0]

            id_ = CTexto(self.page, 'Id.', largura=80, somente_leitura=True, valor_padrao=id_aluno)
            nome_ = CTexto(self.page, 'Nome', largura=390, valor_padrao=aluno_obj.nome)
            serie_ = EscolhaSerie(self.page, label='Série', valor_padrao=aluno_obj.serie.id)
            laudo_ = CTexto(self.page, label='Laudo', largura=LARGURA_COLUNA-10, valor_padrao=aluno_obj.laudo)
            obs_ = CTexto(self.page, label='Observações', largura=LARGURA_COLUNA-10, valor_padrao=aluno_obj.obs)

            # TODO: Query e cálculo das estatísticas. Atribuição do parâmetro 'valor padrão'.
            pontos_ = CTexto(self.page, label='Pontos', largura=140, valor_padrao=aluno_obj.pontos, somente_leitura=True)
            faltas_ = CTexto(self.page, label='Faltas', largura=140, valor_padrao='0', somente_leitura=True)
            presencas_ = CTexto(self.page, label='Presenças', largura=140, valor_padrao='0', somente_leitura=True)
            ocorrencias_ = CTexto(self.page, label='Ocorrências', largura=140, valor_padrao='0', somente_leitura=True)
            atividades_atribuidas_ = CTexto(self.page, label='Atividades atribuídas', largura=140, valor_padrao='0', somente_leitura=True)
            atividades_entregues_ = CTexto(self.page, label='Atividades entregues', largura=140, valor_padrao='0', somente_leitura=True)
            media_ = CTexto(self.page, label='Média', largura=140, valor_padrao='0', somente_leitura=True)
            aluno_nota_ = CTexto(self.page, label='Aluno nota', largura=140, valor_padrao='0', somente_leitura=True)

            criado_em_ = CTexto(self.page, label='Criado em', largura=LARGURA_COLUNA-10, valor_padrao=aluno_obj.created_at, somente_leitura=True)
            alterado_em_ = CTexto(self.page, label='Alterado em', largura=LARGURA_COLUNA-10, valor_padrao=aluno_obj.updated_at, somente_leitura=True)

            btn_salvar_alteracoes = BotaoTextoSalvarAlteracoesAluno(page=self.page, label='Salvar alterações', ctrl_nome=nome_, ctrl_serie=serie_, ctrl_laudo=laudo_, ctrl_obs=obs_, ctrl_id=id_)
            btn_inativar_aluno = BotaoTextoInativarAluno(page=self.page, label='Inativar aluno', ctrl_obs=obs_, ctrl_id=id_)
            btn_inativar_aluno.get.style = ButtonStyle(
                color=Colors.PRIMARY,
                bgcolor='transparent',
                side=BorderSide(width=1, color=Colors.PRIMARY),
                shape=RoundedRectangleBorder(10)
            )
            btn_inativar_aluno.get.tooltip = "Coloque o motivo da mudança de status do aluno no campo 'observações'"

            detalhes_aluno.title =Text(aluno_obj.nome, font_family='nunito', color=Colors.PRIMARY, weight=FontWeight.W_600,
                 width=LARGURA_COLUNA - 100, text_align=TextAlign.CENTER)
            detalhes_aluno.content = Column(
                spacing=10,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Container(height=1, width=LARGURA_COLUNA-50, bgcolor=Colors.PRIMARY),
                    Row(controls=[Text('Informações gerais', font_family='nunito', color=Colors.PRIMARY, weight=FontWeight.W_700)], width=LARGURA_COLUNA-10, alignment=MainAxisAlignment.START),
                    Row(
                        width=LARGURA_COLUNA-10,
                        controls=[
                            id_.get, nome_.get, serie_.get
                        ]
                    ),
                    laudo_.get, obs_.get,

                    Container(
                        content=Row(controls=[Text('Estatísticas', font_family='nunito', color=Colors.PRIMARY,
                                       weight=FontWeight.W_700)], width=LARGURA_COLUNA - 10,
                        alignment=MainAxisAlignment.START),
                        padding=padding.only(top=15)
                    ),

                    Row(
                        width=LARGURA_COLUNA - 10,
                        controls=[
                            pontos_.get, faltas_.get, presencas_.get, ocorrencias_.get
                        ]
                    ),

                    Row(
                        width=LARGURA_COLUNA - 10,
                        controls=[
                            atividades_atribuidas_.get, atividades_entregues_.get, media_.get, aluno_nota_.get
                        ]
                    ),

                    Container(
                        content=Row(controls=[Text('Banco de dados', font_family='nunito', color=Colors.PRIMARY,
                                                   weight=FontWeight.W_700)], width=LARGURA_COLUNA - 10,
                                    alignment=MainAxisAlignment.START),
                        padding=padding.only(top=15)
                    ),

                    criado_em_.get, alterado_em_.get,

                    Container(
                        content=Row(
                            controls=[
                                btn_inativar_aluno.get, btn_salvar_alteracoes.get
                            ],
                            width=LARGURA_COLUNA - 10,
                            alignment=MainAxisAlignment.SPACE_BETWEEN),
                        padding=padding.only(top=25)
                    ),
                ],

                height=ALTURA_COLUNA,
                width=LARGURA_COLUNA
            )

            self.page.open(detalhes_aluno)
