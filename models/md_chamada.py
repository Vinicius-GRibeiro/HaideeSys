from ._md_entities import db, Chamada, Serie
from ._md_logger import Logger
from datetime import datetime
from .md_entrada_chamada import ler_entrada_chamada


def criar_chamada(data: datetime.date, serie: Serie):
    try:
        with db:
            chamada = Chamada.create(data=data, serie=serie)
        Logger.info(f'Chamada criada. ID {chamada.id}')
        return True, chamada
    except Exception as e:
        Logger.error(f'Erro ao criar chamada: {e}')
        return False, None

def ler_chamada(id_: int = None, serie: str = None):
    try:
        with db:
            query = Chamada.select()

            if id_ is not None:
                query = query.where(Chamada.id == id_)

            if serie is not None:
                query = query.where(Chamada.serie == serie)

            query.order_by(Chamada.data)

            chamadas = list(query)

            if chamadas:
                return True, chamadas
            Logger.warning(f'Nenhuma chamada encontrada com os parâmetros: id={id_}, serie={serie}')
            return False, []
    except Exception as e:
        Logger.error(f'Erro ao ler chamada: {e}')
        return False, None
