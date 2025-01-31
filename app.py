import os
from os import getenv

from dotenv import load_dotenv
from flet import Theme, Colors
from flet.core.types import ThemeMode

from models._md_logger import Logger
import flet_easy as fs
from views.vw_inicio import Inicio
from views.vw_alunos import Alunos
from views.vw_turmas import Turmas
from views.vw_ocorrencias import Ocorrencias
from views.vw_pontos import Pontos
from views.vw_config import Configuracoes

load_dotenv()
APP_FOLDER = os.path.join(os.getenv('APPDATA'), os.getenv('APPNAME'))
app = fs.FletEasy(route_init="/config")

def init(data: fs.Datasy):
    # Criando pasta do sistema
    try:
        os.makedirs(APP_FOLDER, exist_ok=True)
    except Exception as e:
        Logger.error(f'Erro ao criar pasta no sistema: {e}')

    # Configurações da janela do aplicativo
    data.page.padding = 0
    data.page.spacing = 0
    data.page.window.center()
    data.page.window.maximizable = False
    data.page.window.resizable = False
    data.page.theme = Theme(color_scheme_seed=getenv("THEMECOLOR"))
    data.page.theme_mode = ThemeMode.LIGHT if getenv("THEMEMODE") == '1' else ThemeMode.DARK
    data.page.fonts = {
        'logo_iniciais': '/fonts/logo_iniciais.ttf',
        'logo_nome': '/fonts/logo_nome.otf',
        'nunito': '/fonts/nunito.ttf',
    }

    # def handle_window_event(e):
    #     if e.data == "close":
    #         # TODO: Implementar confirmação de saída e rotinas de logout
    #         data.page.window.destroy()
    #
    # data.page.window.prevent_close = True
    # data.page.window.on_event = handle_window_event

@app.page(route="/", title="Início")
def home_page(data: fs.Datasy):
    init(data)
    return Inicio(page=data.page).get


@app.page(route="/alunos", title="Alunos")
def alunos_page(data: fs.Datasy):
    init(data)
    return Alunos(page=data.page).get


@app.page(route="/turmas", title="Turmas")
def turmas_page(data: fs.Datasy):
    init(data)
    return Turmas(page=data.page).get


@app.page(route="/ocorrencias", title="Ocorrências")
def ocorrencias_page(data: fs.Datasy):
    init(data)
    return Ocorrencias(page=data.page).get


@app.page(route="/pontos", title="Pontos")
def pontos_page(data: fs.Datasy):
    init(data)
    return Pontos(page=data.page).get


@app.page(route="/config", title="Configurações")
def config_page(data: fs.Datasy):
    init(data)
    return Configuracoes(page=data.page).get

app.run(assets_dir='assets')
