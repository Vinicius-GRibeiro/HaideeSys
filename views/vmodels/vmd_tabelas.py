from abc import ABC, abstractmethod
from flet import (DataTable, DataRow, DataColumn, DataCell, Page, Text, colors, FontWeight, ControlEvent, ControlState,
                  Colors, Column, Container, TextAlign, CrossAxisAlignment, Row, padding, ButtonStyle, BorderSide, RoundedRectangleBorder, TextStyle)
from flet.core.types import MainAxisAlignment
from models.md_aluno import ler_aluno
from models.md_ocorrencia import ler_ocorrencia
from .vmd_detalhes import DetalhesAluno, DetalhesChamada
from .vmd_ctexto import CTexto
from .vmd_escolhas import EscolhaSerie
from models.md_aluno import contar_alunos
from models.md_serie import ler_series
from models.md_chamada import ler_chamada
from datetime import datetime
from models.md_entrada_chamada import ler_entrada_chamada

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

        # alunos = ler_aluno()
        # lista_alunos = []
        #
        # if alunos[0]:
        #     for aluno in alunos[1]:
        #         lista_alunos.append([aluno.id, aluno.serie, aluno.nome, aluno.pontos, 'ativo' if aluno.status else 'inativo'])
        #
        #     self.populate_table(lista_alunos)

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


class TabelaEstatisticaserie(_Tabela):
    def __init__(self, page: Page, serie: str = None):
        super().__init__(page, ['Alunos', 'Ativos', 'Inativos', 'Média'])


    def _on_row_click(self, e: ControlEvent):
        ...


class TabelaChamadaAlunos(_Tabela):
    def __init__(self, page: Page):
        super().__init__(page, ['ID', 'Aluno'])
        self.get.width = 440
        self.get.data_row_color = {
            ControlState.DEFAULT: Colors.RED_ACCENT_100,
            ControlState.SELECTED: Colors.LIGHT_GREEN_ACCENT_100
        }

        self.get.heading_row_color = Colors.with_opacity(.7, Colors.PRIMARY)


    def populate_table(self, valores: list[list | tuple]):
        self.get.rows.clear()
        for valor in valores:
            self.get.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(value=item)) for item in valor
                    ],
                    on_select_changed=lambda e: self._on_row_click(e),
                    selected=True
                )
            )

        self.page.update()

    def _on_row_click(self, e: ControlEvent):
        e.control.selected = False if e.control.selected else True
        self.page.update()


class _TabelaChamadaRegistrosRegistros(_Tabela):
    def __init__(self, page: Page):
        super().__init__(page, ['Aluno', 'Presença'])

    def populate_table(self, valores: list[list | tuple]):
        self.get.rows.clear()
        for valor in valores:
            self.get.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(value=item, color=Colors.GREEN if item == 'P' else Colors.RED if item == 'F' else None)) for item in valor
                    ],
                    on_select_changed=lambda e: self._on_row_click(e)
                )
            )

        self.page.update()

    def _on_row_click(self, e: ControlEvent):
        ...


class TabelaChamadaRegistros(_Tabela):
    def __init__(self, page: Page):
        super().__init__(page, ['ID', 'Série', 'Data'])
        self.get.width = 440
        self.get.heading_row_color = Colors.with_opacity(.7, Colors.PRIMARY)
        self.tabela_registro = _TabelaChamadaRegistrosRegistros(self.page)


    def _on_row_click(self, e: ControlEvent):
        chamada = ler_chamada(id_=e.control.cells[0].content.value)[1]
        entradas = ler_entrada_chamada(id_chamada=chamada[0].id)
        self.tabela_registro.populate_table([
            (entrada.aluno.nome, 'P' if entrada.presenca else 'F')
            for entrada in entradas[1]
        ])

        if entradas[0]:
            detalhes_chamada = DetalhesChamada(self.page).get
            detalhes_chamada.title = Text(f"{chamada[0].serie} - {datetime.strftime(chamada[0].data, '%d/%m/%Y')}", font_family='nunito', color=Colors.PRIMARY,
                                        weight=FontWeight.W_600, text_align=TextAlign.CENTER)

            detalhes_chamada.content = Column(
                spacing=10,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Container(height=1, bgcolor=Colors.PRIMARY),
                    Row(controls=[Text(f"Chamada do {chamada[0].serie}, realizada no dia {datetime.strftime(chamada[0].data, '%d/%m/%Y')}", font_family='nunito', color=Colors.PRIMARY, weight=FontWeight.W_700)], alignment=MainAxisAlignment.START),
                    Column(
                        controls=[
                            self.tabela_registro.get
                        ]
                    )
                ],
                # height=ALTURA_COLUNA,
                # width=LARGURA_COLUNA
            )

            self.page.open(detalhes_chamada)


class TabelaAlunosDaOcorrencia(_Tabela):
    def __init__(self, page: Page, largura: int):
        super().__init__(page, ['Id', 'Aluno', 'Série'], largura_tabela=largura)

    def _on_row_click(self, e: ControlEvent):
        self.get.rows.remove(e.control)
        self.page.update()


class TabelaOcorrencias(_Tabela):
    def __init__(self, page: Page, largura: int):
        super().__init__(page, ['Id', 'Data', 'Série', 'Aluno', 'Assunto'], largura_tabela=largura)
        # self.populate_table_all()

    def populate_table_all(self):
        ocorrencias = ler_ocorrencia()
        if ocorrencias is not None:
            if ocorrencias[0]:
                ocorrencias = [[ocorrencia.id, ocorrencia.data.strftime('%d/%m/%Y'), ocorrencia.serie. id, ocorrencia.aluno.nome, ocorrencia.assunto] for ocorrencia in ocorrencias[1]]
                self.get.rows.clear()
                for ocorrencia in ocorrencias:
                    self.get.rows.append(
                        DataRow(
                            cells=[
                                DataCell(Text(value=item)) for item in ocorrencia
                            ],
                            on_select_changed=lambda e: self._on_row_click(e)
                        )
                    )

                self.page.update()

    def _on_row_click(self, e: ControlEvent):
        id_ocorrencia = e.control.cells[0].content.value
        ocorrencia = ler_ocorrencia(_id=id_ocorrencia)
        if ocorrencia[0]:
            obj_ocorrencia = ocorrencia[1][0]

            aluno = CTexto(self.page, label='Aluno', largura=490, somente_leitura=True, valor_padrao=ler_aluno(id_=obj_ocorrencia.aluno)[1][0].nome)
            serie = CTexto(self.page, label='Serie', somente_leitura=True,largura=100, valor_padrao=ler_aluno(id_=obj_ocorrencia.aluno)[1][0].serie)
            txt_data = CTexto(page=self.page, label='Data', largura=295, somente_leitura=True, valor_padrao=obj_ocorrencia.data.strftime('%d/%m/%Y'))
            txt_oficina = CTexto(page=self.page, label='Oficina', largura=295, somente_leitura=True, valor_padrao=obj_ocorrencia.oficina)
            txt_assunto = CTexto(page=self.page, label='Assunto', largura=600, somente_leitura=True, valor_padrao=obj_ocorrencia.assunto)
            txt_descricao = CTexto(page=self.page, label='Descrição', largura=600, qntd_linhas=3, multilinha=True, somente_leitura=True, valor_padrao=obj_ocorrencia.descricao)


            detalhes_chamada = DetalhesChamada(self.page).get
            detalhes_chamada.title = Text(f"Ocorrência", font_family='nunito', color=Colors.PRIMARY,
                                          weight=FontWeight.W_600, text_align=TextAlign.CENTER)

            detalhes_chamada.content = Column(
                width=610,
                height=300,
                spacing=10,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Container(height=1, bgcolor=Colors.PRIMARY),

                    Column(
                        controls=[
                            Row(
                                controls=[
                                    serie.get, aluno.get
                                ]
                            ),

                            Row(
                                controls=[
                                    txt_data.get, txt_oficina.get
                                ]
                            ),

                            txt_assunto.get,
                            txt_descricao.get,
                        ]
                    )
                ],
            )

            self.page.open(detalhes_chamada)


class TabelaRegistrosPontos(_Tabela):
    def __init__(self, page: Page, largura: int):
        super().__init__(page, ['Data', 'Tipo', 'Descrição', 'Qntd.', 'Antes', 'Após'], largura_tabela=largura)

    def populate_table(self, valores: list[list | tuple]):
        self.get.rows.clear()
        for valor in valores:
            self.get.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(value=item, color=Colors.GREEN_900 if valor[1] == 'Adicionar' else Colors.RED_900, weight=FontWeight.W_500)) for item in valor
                    ],
                    on_select_changed=lambda e: self._on_row_click(e)
                )
            )

        self.page.update()

    def _on_row_click(self, e: ControlEvent):
        ...
