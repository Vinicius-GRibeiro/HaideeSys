import os
from datetime import datetime
from flet import (TextButton, Row, Page, ButtonStyle, Colors, ControlState, RoundedRectangleBorder, ScrollMode, DataRow,
                  RadioGroup, Radio, IconButton, icons, Column, Text, FontWeight, TextAlign, ControlEvent, Container,
                  DataCell, MainAxisAlignment, SubmenuButton, MenuItemButton, Theme, Icon, MenuBar, MenuStyle)
from abc import ABC, abstractmethod

from flet.core.types import ThemeMode

from .vmd_ctexto import CTexto
from .vmd_escolhas import EscolhaSerie, EscolhaSerieEstatisticas, EscolhaAlunos, EscolhaSerieSincronizadoComEscolhaAluno, _Escolha
from models.md_aluno import criar_aluno, ler_aluno, editar_aluno, adicionar_pontos, remover_pontos, contar_alunos
from models.md_serie import criar_serie, ler_series
from models.md_chamada import criar_chamada, ler_chamada
from models.md_ocorrencia import criar_ocorrencia, ler_ocorrencia
from models.md_entrada_chamada import criar_entrada_chamada
from models.md_pontos import ler_pontos
from .vmd_tabelas import TabelaAlunos, TabelaChamadaAlunos, TabelaAlunosDaOcorrencia, TabelaOcorrencias, TabelaRegistrosPontos
from .vmd_notificacao import Notificacao
from .vmd_detalhes import DetalhesAdicionarChamada
import re
from fpdf import FPDF
from dotenv import load_dotenv, set_key

LARGURA_PADRAO = 135
TAMANHO_ICONE_BOTAO = 28

load_dotenv()


class _BotaoTexto(ABC):
    def __init__(self, page: Page, label: str, largura: int = LARGURA_PADRAO):
        self.page = page

        self.label = label
        self.largura = largura
        self.notificacao = Notificacao(page)

        self.get = self._get()

    def _get(self) -> TextButton:
        return TextButton(
            text=self.label,
            style=ButtonStyle(
                bgcolor={
                    ControlState.DEFAULT: Colors.PRIMARY,
                    ControlState.HOVERED: Colors.with_opacity(.8, Colors.PRIMARY),
                },
                color=Colors.ON_PRIMARY,
                shape=RoundedRectangleBorder(5)
            ),

            width=self.largura,
            on_click=lambda e: self._on_click(e)
        )

    @abstractmethod
    def _on_click(self, e: ControlState):
        ...


class _BotaoIcone(ABC):
    def __init__(self, page: Page, icone: str, tamanho: int = TAMANHO_ICONE_BOTAO):
        self.page = page

        self.icone = icone
        self.tamanho = tamanho

        self.get = self._get()

    def _get(self) -> IconButton:
        return IconButton(
            icon=self.icone,
            icon_color=Colors.PRIMARY,
            on_click=lambda e: self._on_click(e),
            icon_size=self.tamanho,
        )

    @abstractmethod
    def _on_click(self, e: ControlState):
        pass


class BotaoTextoSalvarAluno(_BotaoTexto):
    def __init__(self, page: Page, label: str, ctrl_serie: EscolhaSerie, ctrl_nome: CTexto, ctrl_laudo: CTexto, ctrl_obs: CTexto, ctrl_tabela: TabelaAlunos):
        super().__init__(page, label)
        self.ctrl_serie = ctrl_serie
        self.ctrl_nome = ctrl_nome
        self.ctrl_laudo = ctrl_laudo
        self.ctrl_obs = ctrl_obs
        self.ctrl_tabela = ctrl_tabela

    def _on_click(self, e: ControlState):
        serie = self.ctrl_serie.valor()
        nome = self.ctrl_nome.valor()
        laudo = self.ctrl_laudo.valor()
        obs = self.ctrl_obs.valor()

        if not serie or not nome:
            self.notificacao.notificar(msg='A série e nome do aluno não podem estar em branco', tipo='erro', icone=icons.ERROR)
            return

        op = criar_aluno(serie, nome, laudo, obs)

        if op[0]:
            self.ctrl_serie.get.value = ''
            self.ctrl_nome.get.value = ''
            self.ctrl_laudo.get.value = ''
            self.ctrl_obs.get.value = ''

            self.ctrl_tabela.populate_table()
            self.notificacao.notificar(msg=f'Aluno adicionado - ID do aluno: {op[1]}', icone=icons.THUMB_UP)
        else:
            self.notificacao.notificar(msg=f'Algo deu errado ao criar o aluno. Contate o desenvolvedor', icone=icons.ERROR, tipo='erro')


class BotaoRadio:
    def __init__(self, page: Page, opcoes: dict[str, str], valor_padrao: str = None):
        self.page = page

        self.opcoes = opcoes
        self.valor_padrao = valor_padrao

        self.get = self._get()

    def _get(self) -> RadioGroup:
        return RadioGroup(
            content=Row(
                controls=[Radio(value=item[0], label=item[1]) for item in self.opcoes.items()]
            ),

        )


class BotaoIconePesquisarAluno(_BotaoIcone):
    def __init__(self, page: Page, icone: str, ctrl_serie: EscolhaSerie, ctrl_nome: CTexto, ctrl_ordenar_por: BotaoRadio, ctrl_tabela: TabelaAlunos, tamanho: int = TAMANHO_ICONE_BOTAO):
        super().__init__(page, icone, tamanho)
        self.ctrl_serie = ctrl_serie
        self.ctrl_nome = ctrl_nome
        self.ctrl_ordenar_por = ctrl_ordenar_por
        self.ctrl_tabela = ctrl_tabela

    def _on_click(self, e: ControlState):
        serie = self.ctrl_serie.valor()
        nome = self.ctrl_nome.valor() if self.ctrl_nome.valor() != '' else None
        ordenar_por = self.ctrl_ordenar_por.get.value

        alunos = ler_aluno(serie=serie, nome=nome, ordenar_por=ordenar_por)

        if alunos[0]:
            self.ctrl_tabela.populate_table(
                [
                    [aluno.id, aluno.serie, aluno.nome, aluno.pontos, 'ativo' if aluno.status else 'inativo']
                    for aluno in alunos[1]
                ]
            )


class BotaoIconeLimparFiltros(_BotaoIcone):
    def __init__(self, page: Page, icone: str, ctrl_tabela: TabelaAlunos, controles: list, controle_radio: BotaoRadio, tamanho: int = TAMANHO_ICONE_BOTAO):
        super().__init__(page, icone, tamanho)
        self.ctrl_tabela = ctrl_tabela
        self.controles = controles
        self.controle_radio = controle_radio

    def _on_click(self, e: ControlState):
        for controle in self.controles:
            controle.get.value = None
        self.controle_radio.get.value = 'nome'
        self.ctrl_tabela.populate_table()
        self.page.update()


class BotaoTextoSalvarAlteracoesAluno(_BotaoTexto):
    def __init__(self, page: Page, label: str, ctrl_nome, ctrl_serie, ctrl_laudo, ctrl_obs, ctrl_id):
        super().__init__(page, label)
        self.ctrl_nome = ctrl_nome
        self.ctrl_serie = ctrl_serie
        self.ctrl_laudo = ctrl_laudo
        self.ctrl_obs = ctrl_obs
        self.ctrl_id = ctrl_id

    def _on_click(self, e: ControlState):
        nome = self.ctrl_nome.valor()
        serie = self.ctrl_serie.valor()
        laudo = self.ctrl_laudo.valor()
        obs = self.ctrl_obs.valor()
        id_ = self.ctrl_id.valor()

        if editar_aluno(id_=id_, _nome=nome, _serie=serie, _laudo=laudo, _obs=obs):
            self.notificacao.notificar('Alterações salvas')


class BotaoTextoInativarAluno(_BotaoTexto):
    def __init__(self, page: Page, label: str, ctrl_obs, ctrl_id):
        super().__init__(page, label)
        self.ctrl_obs = ctrl_obs
        self.ctrl_id = ctrl_id

    def _on_click(self, e: ControlState):
        obs = self.ctrl_obs.valor()
        id_ = self.ctrl_id.valor()

        if obs is not None and obs != '':
            if editar_aluno(id_=id_, _status=False, _obs=obs):
                self.notificacao.notificar(msg=f'O aluno foi inativado. Motivo: {obs}')
                return True
        self.notificacao.notificar(msg=f"Preencha o campo 'observações', com o motivo pelo qual o aluno está sendo inativado", tipo='erro')


class BotaoTextoAdicionarSerie(_BotaoTexto):
    def __init__(self, page: Page, label: str, largura: int, ctrl_serie: CTexto, ctrl_escolher_serie: EscolhaSerieEstatisticas):
        super().__init__(page, label)
        self.largura = largura
        self.get.width = largura
        self.get.tooltip = "Informe a série com somente um número e uma letra, exemplo: 1A"
        self.ctrl_serie = ctrl_serie
        self.ctrl_escolher_serie = ctrl_escolher_serie

    def _on_click(self, e: ControlState):
        serie = self.ctrl_serie.valor().upper()

        if serie is not None and serie != '':
            if not bool(re.match(r"^\d{1}[A-Z]{1}$", serie)):
                self.notificacao.notificar("A série precisa conter SOMENTE um número e uma letra, exemplo: 1A", tipo='erro')
                return

            if criar_serie(serie):
                self.ctrl_serie.get.value = ''
                self.ctrl_escolher_serie.populate_dropdown(ler_series()[1])  # type: ignore
                self.notificacao.notificar(f"{serie} adicionado")
                self.page.update()


class BotaoGravarChamada(_BotaoTexto):
    def __init__(self, page: Page, label: str, ctrl_tabela: TabelaChamadaAlunos, ctrl_serie, ctrl_data):
        super().__init__(page, label)
        self.ctrl_tabela = ctrl_tabela
        self.ctrl_data = ctrl_data
        self.ctrl_serie = ctrl_serie

    def _on_click(self, e: ControlState):
        if self.ctrl_serie.valor() == '' or self.ctrl_serie.valor() is None:
            self.notificacao.notificar(msg='Escolha uma série para fazer a chamada', tipo='erro')
            return

        if not bool(re.match(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$", self.ctrl_data.valor())):
            self.notificacao.notificar(msg='Algo está errado com a data. Certifique-se de que ela está no formato DD/MM/AAAA', tipo='erro')
            return

        self.notificacao.notificar(msg="Aguarde...")
        chamada = criar_chamada(data=self.ctrl_data.valor(), serie=self.ctrl_serie.valor())
        if chamada[0]:
            chamada = chamada[1].id
            linhas = self.ctrl_tabela.get.rows

            for linha in linhas:
                id_aluno = linha.cells[0].content.value
                presenca = linha.selected
                if criar_entrada_chamada(id_chamada=chamada, aluno_id=id_aluno, presenca=presenca):
                    continue
                self.notificacao.notificar(msg=f"Ocorreu um erro ao gravar a chamada", tipo='erro')
                break

            self.notificacao.notificar(msg="Chamada realizada")
            self.ctrl_serie.get.value = ''
            self.ctrl_data.get.value = datetime.today().strftime('%d/%m/%Y')
            self.ctrl_tabela.get.rows.clear()
            self.page.update()


class BotaoIconePesquisarChamada(_BotaoIcone):
    def __init__(self, page: Page, ctrl_serie, ctrl_tabela, icone: str = icons.SEARCH):
        super().__init__(page, icone)
        self.get.scale = .8
        self.ctrl_serie = ctrl_serie
        self.ctrl_tabela = ctrl_tabela

    def _on_click(self, e: ControlState):
        serie = None if self.ctrl_serie.valor() == '' or self.ctrl_serie.valor() is None else self.ctrl_serie.valor()
        chamadas=ler_chamada(serie=serie)
        if chamadas[0]:
            self.ctrl_tabela.populate_table([
                (chamada.id, chamada.serie, chamada.data.strftime('%d/%m/%Y'))
                for chamada in chamadas[1]
            ])


class BotaoIconeRelatorioChamada(_BotaoIcone):
    def __init__(self, page: Page, icone: str = icons.BOOK):
        super().__init__(page, icone)
        self.get.scale = .8

    def _on_click(self, e: ControlState):
        ...


class BotaoIconeAdicionarAlunoNaOcorrencia(_BotaoIcone):
    def __init__(self, page: Page, tabela: TabelaAlunosDaOcorrencia, serie: EscolhaSerieSincronizadoComEscolhaAluno, aluno: EscolhaAlunos, icone: str = icons.ADD):
        super().__init__(page, icone)
        self.get.scale = .8
        self.tabela = tabela
        self.serie = serie
        self.aluno = aluno

    def _on_click(self, e: ControlState):
        serie = self.serie.valor()
        aluno = self.aluno.valor()
        aluno_id = ler_aluno(serie=serie, nome=aluno)

        if aluno is not None and aluno != '' and serie is not None and serie != '':
            self.tabela.get.rows.append(
                DataRow(
                    cells=[
                        DataCell(content=Text(aluno_id[1][0].id)),
                        DataCell(content=Text(serie)),
                        DataCell(content=Text(aluno)),
                    ]
                )
            )

            self.page.update()


class BotaoIconePesquisarOcorrencia(_BotaoIcone):
    def __init__(self, page: Page, serie:EscolhaSerie, aluno: CTexto, tabela_ocorrencias: TabelaOcorrencias, icone: str = icons.SEARCH):
        super().__init__(page, icone)
        self.get.scale = .8

        self.serie = serie
        self.aluno = aluno
        self.tabela_ocorrencias = tabela_ocorrencias

    def _on_click(self, e: ControlState):
        if (self.serie.valor() == '' or self.serie.valor() is None) and (self.aluno.valor() == '' or self.aluno.valor() is None):
            self.tabela_ocorrencias.populate_table_all()
            return

        serie = self.serie.valor() if self.serie.valor() != '' else None
        aluno = ler_aluno(serie=self.serie.valor(), nome=self.aluno.valor())[1][0] if self.aluno.valor() != '' else None

        ocorrencias = ler_ocorrencia(_serie=serie, _aluno=aluno)
        if ocorrencias[0]:
            valores = [[ocorrencia.id, ocorrencia.data.strftime('%d/%m/%Y'), ocorrencia.serie.id, ocorrencia.aluno.nome, ocorrencia.assunto] for ocorrencia in ocorrencias[1]]
            self.tabela_ocorrencias.populate_table(valores)


class BotaoIconeRedefinirOcorrencias(_BotaoIcone):
    def __init__(self, page: Page, serie:EscolhaSerie, aluno: CTexto, tabela_ocorrencias: TabelaOcorrencias, icone: str = icons.REFRESH):
        super().__init__(page, icone)
        self.get.scale = .8

        self.serie = serie
        self.aluno = aluno
        self.tabela_ocorrencias = tabela_ocorrencias

    def _on_click(self, e: ControlState):
        self.serie.get.value = None
        self.aluno.get.value = None
        self.get.focus()
        self.tabela_ocorrencias.populate_table_all()



class BotaoTextoAdicionarOcorrencia(_BotaoTexto):
    def __init__(self, page: Page, label: str, largura: int, tabela_ocorrencias):
        super().__init__(page, label, largura=largura)
        self.largura = largura
        self.get.width = largura
        self.tabela_ocorrencias = tabela_ocorrencias

        self.tabela_alunos_ocorrencia = TabelaAlunosDaOcorrencia(self.page, largura=600)
        self.aluno = EscolhaAlunos(self.page, label='Aluno', largura=450)
        self.serie = EscolhaSerieSincronizadoComEscolhaAluno(self.page, label='Serie', escolha_aluno=self.aluno, somente_ativos=True)
        self.add_aluno = BotaoIconeAdicionarAlunoNaOcorrencia(self.page, tabela=self.tabela_alunos_ocorrencia, serie=self.serie, aluno=self.aluno)

        self.txt_data = CTexto(page=self.page, label='Data', largura=295)
        self.txt_data.get.value = datetime.now().strftime('%d/%m/%Y')
        self.txt_oficina = CTexto(page=self.page, label='Oficina', largura=295)
        self.txt_oficina.get.value = os.getenv("CLASSNAME").capitalize()
        self.txt_assunto = CTexto(page=self.page, label='Assunto', largura=600)
        self.txt_descricao = CTexto(page=self.page, label='Descrição', largura=600, qntd_linhas=3, multilinha=True)
        self.salvar_ocorrencia = BotaoTextoSalvarOcorrencia(self.page, 'Salvar ocorrência', 200, data=self.txt_data, oficina=self.txt_oficina, assunto=self.txt_assunto, descricao=self.txt_descricao, tabela=self.tabela_alunos_ocorrencia,
                                                            serie=self.serie, aluno=self.aluno, tabela_ocorrencias=self.tabela_ocorrencias)

    def _on_click(self, e: ControlEvent):
        detalhe_nova_ocorrencia = DetalhesAdicionarChamada(self.page).get
        detalhe_nova_ocorrencia.title = Text(f"Nova ocorrência", font_family='nunito', color=Colors.PRIMARY,
                                        weight=FontWeight.W_600, text_align=TextAlign.CENTER)
        detalhe_nova_ocorrencia.content = Column(
            controls=[
                Container(
                    bgcolor=Colors.with_opacity(.08, Colors.TERTIARY),
                    padding=10,
                    border_radius=10,
                    width=620,
                    content=Column(
                        width=920,
                        controls=[
                            Row(
                                controls=[
                                    self.serie.get, self.aluno.get, self.add_aluno.get
                                ]
                            ),

                            Row(
                                controls=[
                                    self.txt_data.get, self.txt_oficina.get
                                ]
                            ),

                            self.txt_assunto.get,
                            self.txt_descricao.get,
                            Column(
                                controls=[
                                    self.tabela_alunos_ocorrencia.get
                                ],
                                height=150,
                                scroll=ScrollMode.AUTO
                            ),
                            Container(height=10, width=1),
                            Row([self.salvar_ocorrencia.get], width=910, alignment=MainAxisAlignment.END)
                        ]
                    )
                )
            ]
        )

        self.page.open(detalhe_nova_ocorrencia)


class BotaoTextoSalvarOcorrencia(_BotaoTexto):
    def __init__(self, page: Page, label: str, largura: int, data: CTexto, oficina: CTexto, assunto: CTexto, descricao: CTexto, tabela: TabelaAlunosDaOcorrencia,
                 serie, aluno, tabela_ocorrencias):
        super().__init__(page, label, largura=largura)
        self.data = data
        self.oficina = oficina
        self.assunto = assunto
        self.descricao = descricao
        self.tabela = tabela
        self.serie = serie
        self.aluno = aluno
        self.tabela_ocorrencias = tabela_ocorrencias

    def gerar_pdf_ocorrencia(self, professor, oficina, data, alunos, assunto, descricao):
        class PDF(FPDF):
            def header(self):
                app_data = os.getenv('APPDATA', '.')
                app_name = os.getenv('APPNAME', 'app')
                _caminho_programa = os.path.join(app_data, app_name, 'assets')
                _imagem_path = os.path.join(_caminho_programa, 'brasao_braganca.png')

                self.set_font('Arial', 'B', 12)
                if os.path.exists(_imagem_path):
                    self.image(name=_imagem_path, x=10, y=10, w=30)
                self.ln(5)
                self.cell(0, 10, 'Escola Haidée Marçal Serbin', 0, 1, 'C')
                self.set_font('Arial', size=12)
                self.cell(0, 10, 'OCORRÊNCIA', 0, 1, 'C')
                self.ln(5)

        # Verificar variáveis de ambiente
        app_data = os.getenv('APPDATA', '.')
        app_name = os.getenv('APPNAME', 'app')
        caminho_programa = os.path.join(app_data, app_name, 'Ocorrências')
        os.makedirs(caminho_programa, exist_ok=True)


        # Criação do documento PDF
        pdf = PDF()
        pdf.add_page()
        pdf.set_font('Arial', '', 12)

        # Adiciona um espaçamento inicial
        pdf.ln(5)

        # Cabeçalhos da Tabela
        pdf.set_font('Arial', 'B', size=10)
        pdf.cell(64, 5, 'Professor', 1, align='C')
        pdf.cell(63, 5, 'Oficina', 1, align='C')
        pdf.cell(63, 5, 'Data', 1, align='C')
        pdf.ln(5)

        # Conteúdos da Tabela
        pdf.set_font('Arial', '', 10)
        pdf.cell(64, 5, professor, 1, align='C')
        pdf.cell(63, 5, oficina, 1, align='C')
        pdf.cell(63, 5, data, 1, align='C')
        pdf.ln()

        # Espaçamento
        pdf.ln(5)

        # Cabeçalhos da Tabela Aluno
        pdf.set_font('Arial', 'B', size=10)
        pdf.cell(40, 5, 'Série', 1, align='C')
        pdf.cell(150, 5, 'Aluno', 1, align='C')
        pdf.ln()

        # Conteúdos da Tabela Aluno
        pdf.set_font('Arial', '', 10)

        for aluno in alunos:
            pdf.cell(40, 5, aluno[0], 1, align='C')
            pdf.cell(150, 5, aluno[1], 1, align='C')
            pdf.ln()

        # Espaçamento
        pdf.ln(5)

        # Cabeçalhos do Assunto e Descrição
        pdf.set_font('Arial', 'B', size=10)
        pdf.cell(190, 5, 'Assunto', 1)
        pdf.ln()

        # Conteúdo do Assunto
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(w=190, txt=assunto, border=1, align='L', h=10)
        pdf.ln()

        # Cabeçalhos da Descrição
        pdf.set_font('Arial', 'B', size=10)
        pdf.cell(190, 5, 'Descrição', 1)
        pdf.ln()

        # Conteúdo da Descrição
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(w=190, txt=descricao, border=1, align='L', h=10)
        pdf.ln()

        # Espaçamento antes dos campos de assinatura
        pdf.ln(5)

        pdf.set_font('Arial', 'B', size=10)
        pdf.cell(95, 5, 'ALUNO', 1, align='C')
        pdf.cell(95, 5, 'ASSINATURA', 1, align='C')
        pdf.ln()

        pdf.set_font('Arial', '', size=10)
        for aluno in alunos:
            pdf.cell(95, 7, aluno[1], 1, align='C')
            pdf.cell(95, 7, ' ', 1, align='C')
            pdf.ln()

        pdf.ln(30)

        # Adiciona linhas para assinatura
        largura_linha = 100
        x_inicial = 10
        y_atual = pdf.get_y()

        pdf.line(x1=x_inicial, y1=y_atual, x2=x_inicial + largura_linha,
                 y2=y_atual)  # Linha para assinatura do professor

        # Adiciona rótulos abaixo das linhas
        pdf.set_font('Arial', 'B', 12)
        pdf.ln(2)  # Adiciona espaço abaixo das linhas

        # Adiciona rótulo do professor
        pdf.set_x(x_inicial)
        pdf.cell(largura_linha, 10, 'Professor', 0, 0, 'C')

        n_data = datetime.strptime(data, '%d/%m/%Y').strftime('%d-%m-%Y')
        output_path = os.path.join(caminho_programa, f"{n_data} - {aluno[0]} - {aluno[1]}.pdf")
        pdf.output(output_path)

    def _on_click(self, e: ControlState):
        nao_vazios = True
        controles = [self.data, self.oficina, self.assunto, self.descricao]
        for controle in controles:
            nao_vazios = controle.valor() is not None and controle.valor() != ''
        if not nao_vazios:
            self.notificacao.notificar('Todos os campos precisam estar preenchidos', 'erro')
            return

        if not len(self.tabela.get.rows) > 0:
            self.notificacao.notificar('Pelo menos um aluno precisa estar na ocorrência', 'erro')
            return

        alunos_ids = [[row.cells[0].content.value, row.cells[1].content.value] for row in self.tabela.get.rows]

        ocorrencias_estao_corretas = True

        for id_e_serie in alunos_ids:
            ocorrencias_estao_corretas = criar_ocorrencia(
                id_aluno=id_e_serie[0],
                id_serie=id_e_serie[1],
                oficina=self.oficina.valor(),
                assunto=self.assunto.valor(),
                descricao=self.descricao.valor(),
            )

        if not ocorrencias_estao_corretas[0]:
            self.notificacao.notificar('Um erro ocorreu ao criar a ocorrência', 'erro')
            return

        self.gerar_pdf_ocorrencia(professor=os.getenv("TEACHERNAME"), oficina=self.oficina.valor(), data=self.data.valor(),
                                  alunos=[[id_e_serie[1], ler_aluno(id_=id_e_serie[0])[1][0].nome] for id_e_serie in alunos_ids], assunto=self.assunto.valor(), descricao=self.descricao.valor())

        self.notificacao.notificar('Ocorrência adicionada')
        self.serie.get.value = ''
        self.aluno.get.value = ''
        self.data.get.value = datetime.now().strftime('%d/%m/%Y')
        self.oficina.get.value = os.getenv("CLASSNAME").capitalize()
        self.assunto.get.value = ''
        self.descricao.get.value = ''
        self.tabela.get.rows.clear()
        self.tabela_ocorrencias.populate_table_all()
        self.page.update()


class BotaoIconePesquisarPontosAluno(_BotaoIcone):
    def __init__(self, page: Page, serie:_Escolha = None, aluno: _Escolha = None, tabela_pontucoes: TabelaRegistrosPontos = None, icone: str = icons.SEARCH):
        super().__init__(page, icone)
        self.get.scale = .8

        self.serie = serie
        self.aluno = aluno
        self.tabela_pontucoes = tabela_pontucoes

    def _on_click(self, e: ControlState):
        serie = self.serie.valor()
        aluno = self.aluno.valor()

        if serie is not None and aluno is not None:
            aluno_id = ler_aluno(serie=serie, nome=aluno)[1][0].id
            registros = ler_pontos(aluno_id=aluno_id)
            if registros[0]:
                lista_registros = []
                for registro in registros[1]:
                    lista_registros.append([registro.data.strftime('%d/%m/%Y'), 'Adicionar' if registro.tipo else 'Remover', registro.descricao, registro.quantidade_pontos, registro.total_antes, registro.total_apos])

                self.tabela_pontucoes.populate_table(lista_registros)

class BotaoTextoMudarPontuacao(_BotaoTexto):
    def __init__(self, page: Page, label: str, largura: int, serie: _Escolha, aluno: _Escolha, tipo: _Escolha, descricao: _Escolha, pontos: CTexto):
        super().__init__(page, label)
        self.largura = largura
        self.get.width = largura

        self.serie = serie
        self.aluno = aluno
        self.tipo = tipo
        self.descricao = descricao
        self.pontos = pontos


    def _on_click(self, e: ControlState):
        serie = self.serie.valor()
        aluno = self.aluno.valor()
        tipo = self.tipo.valor()
        descricao = self.descricao.valor()
        pontos = self.pontos.valor()

        if tipo is None or descricao is None or serie is None or len(str(pontos)) < 1:
            self.notificacao.notificar(msg="Os campos 'série', 'tipo', 'aluno' e 'pontos' não podem ficar vazios", tipo='erro')
            return


        if aluno is not None:
            aluno_obj = ler_aluno(serie=serie, nome=aluno)[1][0]

            if tipo == 'Adicionar':
                adicionar_pontos(id_=aluno_obj.id, qntd_pontos=int(pontos), descricao=descricao)
                self.notificacao.notificar(msg=f"Pontos adicionados para o(a) aluno(a) {aluno_obj.nome}.\nTotal: {aluno_obj.pontos + int(pontos)}")
            else:
                remover_pontos(id_=aluno_obj.id, qntd_pontos=int(pontos), descricao=descricao)
                self.notificacao.notificar(msg=f"Pontos removidos  do(a) aluno(a) {aluno_obj.nome}\nTotal: {aluno_obj.pontos - int(pontos)}")

            self.serie.get.value = None
            self.aluno.get.value = None
            self.descricao.get.value = None
            self.tipo.get.value = None
            self.pontos.get.value = ''
            self.page.update()
            return

        alunos = ler_aluno(serie=serie, somente_ativos=True)[1]
        if tipo == 'Adicionar':
            for aluno_obj in alunos:
                adicionar_pontos(id_=aluno_obj.id, qntd_pontos=pontos, descricao=descricao)
            self.notificacao.notificar(msg=f"Pontos adicionados para os(as) alunos(as) do {serie}")
        else:
            for aluno_obj in alunos:
                remover_pontos(id_=aluno_obj.id, qntd_pontos=pontos, descricao=descricao)
            self.notificacao.notificar(msg=f"Pontos removidos dos(as) alunos(as) do {serie}")

        self.serie.get.value = None
        self.aluno.get.value = None
        self.descricao.get.value = None
        self.tipo.get.value = None
        self.pontos.get.value = ''
        self.page.update()


class BotaoIconeRedefinirSerieAlunoPontos(_BotaoIcone):
    def __init__(self, page: Page, serie:_Escolha, aluno: _Escolha, tabela: TabelaRegistrosPontos, icone: str = icons.REFRESH):
        super().__init__(page, icone)
        self.get.scale = .8

        self.serie = serie
        self.aluno = aluno
        self.tabela = tabela

    def _on_click(self, e: ControlState):
        self.aluno.get.value = None
        self.aluno.get.options.clear()
        self.serie.get.value = None
        self.tabela.get.rows.clear()
        self.get.focus()
        self.page.update()


class BotaoEscolhaCores:
    def __init__(self, page: Page):
        self.page = page
        self.notificacao = Notificacao(page)
        self.get = self._get()

    def _on_change_colors(self, e: ControlEvent):
        cor = e.control.content.controls[0].color
        self.page.theme.color_scheme_seed = cor
        set_key('.env', "THEMECOLOR", cor)
        self.page.update()

    def _on_change_mode(self, e: ControlEvent):
        icone_name = e.control.content.controls[0].name
        if icone_name == icons.LIGHT_MODE:
            set_key('.env', "THEMEMODE", '1')
        else:
            set_key('.env', "THEMEMODE", '0')
        self.notificacao.notificar('Feche o programa e abra-o novamente para aplicar as alterações.')



    def _get(self):
        return MenuBar(
            controls=[
                SubmenuButton(
                    content=Row(
                        controls=[
                            Text('Cor padrão')
                        ]
                    ),
                    controls=[
                        MenuItemButton(
                            content=Row([Icon(name=icons.COLOR_LENS, color=Colors.RED), Text('Vermelho')]),
                            on_click=lambda e: self._on_change_colors(e),
                        ),

                        MenuItemButton(
                            content=Row([Icon(name=icons.COLOR_LENS, color=Colors.PURPLE), Text('Roxo')]),
                            on_click=lambda e: self._on_change_colors(e),
                        ),

                        MenuItemButton(
                            content=Row([Icon(name=icons.COLOR_LENS, color=Colors.INDIGO), Text('Indigo')]),
                            on_click=lambda e: self._on_change_colors(e),
                        ),

                        MenuItemButton(
                            content=Row([Icon(name=icons.COLOR_LENS, color=Colors.BLUE), Text('Azul')]),
                            on_click=lambda e: self._on_change_colors(e),
                        ),

                        MenuItemButton(
                            content=Row([Icon(name=icons.COLOR_LENS, color=Colors.CYAN), Text('Ciano')]),
                            on_click=lambda e: self._on_change_colors(e),
                        ),

                        MenuItemButton(
                            content=Row([Icon(name=icons.COLOR_LENS, color=Colors.TEAL), Text('Teal')]),
                            on_click=lambda e: self._on_change_colors(e),
                        ),

                        MenuItemButton(
                            content=Row([Icon(name=icons.COLOR_LENS, color=Colors.GREEN), Text('Verde')]),
                            on_click=lambda e: self._on_change_colors(e),
                        ),

                        MenuItemButton(
                            content=Row([Icon(name=icons.COLOR_LENS, color=Colors.LIGHT_GREEN), Text('Verde claro')]),
                            on_click=lambda e: self._on_change_colors(e),
                        ),

                        MenuItemButton(
                            content=Row([Icon(name=icons.COLOR_LENS, color=Colors.YELLOW), Text('Amarelo')]),
                            on_click=lambda e: self._on_change_colors(e),
                        ),

                        MenuItemButton(
                            content=Row([Icon(name=icons.COLOR_LENS, color=Colors.ORANGE), Text('Laranja')]),
                            on_click=lambda e: self._on_change_colors(e),
                        ),
                    ]
                ),

                SubmenuButton(
                    content=Row(
                        controls=[
                            Text('Modo')
                        ]
                    ),
                    controls=[
                        MenuItemButton(
                            content=Row([Icon(name=icons.LIGHT_MODE), Text('Modo claro')]),
                            on_click=lambda e: self._on_change_mode(e),
                        ),

                        MenuItemButton(
                            content=Row([Icon(name=icons.DARK_MODE), Text('Modo escuro')]),
                            on_click=lambda e: self._on_change_mode(e),
                        ),

                    ]
                )
            ]
        )