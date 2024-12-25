import os
from dotenv import load_dotenv
from models._md_logger import Logger
from models._md_entities import ControleDeExcecoes
import flet_easy as fs

load_dotenv()
APP_FOLDER = os.path.join(os.getenv('APPDATA'), os.getenv('APPNAME'))
app = fs.FletEasy(route_init="/")

def init(data: fs.Datasy):
    # Criando pasta do sistema
    try:
        os.makedirs(APP_FOLDER, exist_ok=True)
    except Exception as e:
        Logger.error(f'Erro ao criar pasta no sistema: {e}')
        raise ControleDeExcecoes('Erro ao criar pasta do sistema', e)

    # Configurações da janela do aplicativo
    data.page.padding = 0
    data.page.spacing = 0
    data.page.window.center()
    data.page.window.maximizable = False
    data.page.window.resizable = False

@app.page(route="/", title="Início")
def home_page(data: fs.Datasy):
    return
