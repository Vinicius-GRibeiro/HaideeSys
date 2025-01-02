from flet import (TextButton, Row, Page, ButtonStyle, Colors, ControlState, RoundedRectangleBorder,
                  RadioGroup, Radio, IconButton, icons)
from abc import ABC, abstractmethod
from .vmd_ctexto import CTexto
from .vmd_escolhas import EscolhaSerie
from models.md_aluno import criar_aluno, ler_aluno, editar_aluno
from .vmd_tabelas import TabelaAlunos
from .vmd_notificacao import Notificacao


LARGURA_PADRAO = 135
TAMANHO_ICONE_BOTAO = 28


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

