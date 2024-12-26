import os
from dotenv import load_dotenv
from models._md_logger import Logger
import flet_easy as fs
from views.vw_inicio import Inicio


load_dotenv()
APP_FOLDER = os.path.join(os.getenv('APPDATA'), os.getenv('APPNAME'))
app = fs.FletEasy(route_init="/")

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
    data.page.fonts = {
        'logo_iniciais': '/fonts/logo_iniciais.ttf',
        'logo_nome': '/fonts/logo_nome.otf',
        'nunito': '/fonts/nunito.ttf',
    }

@app.page(route="/", title="Início")
def home_page(data: fs.Datasy):
    init(data)
    return Inicio(page=data.page).get

app.run(assets_dir='assets')
