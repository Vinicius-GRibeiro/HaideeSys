from ._md_entities import db, EntradaChamada, Aluno
from ._md_logger import Logger

def criar_entrada_chamada(id_chamada: int, aluno_id: int, presenca: bool = True):
    try:
        with db:
            entrada = EntradaChamada.create(chamada=id_chamada, aluno=aluno_id, presenca=presenca)
            return True, entrada
    except Exception as e:
        Logger.error(f"Erro ao criar entrada de chamada: {e}")
        return False, None

def ler_entrada_chamada(id_chamada: int = None, id_aluno: int = None):
    try:
        with db:
            query = EntradaChamada.select()

            if id_chamada is not None:
                query = query.where(EntradaChamada.chamada == id_chamada)

            if id_aluno is not None:
                query = query.where(EntradaChamada.aluno == id_aluno)

            query = query.order_by(EntradaChamada.id)
            entrada = list(query)
            if entrada:
                return True, entrada
            Logger.warning(f"Nenhuma entrada de chamada encontrada com os parâmetros: chamada={id_chamada}, aluno={id_aluno}")
            return False, []
    except Exception as e:
        Logger.error(f"Erro ao ler entrada de chamada: {e}")
        return False, None
