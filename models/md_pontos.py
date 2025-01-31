from ._md_entities import db, Pontuacao
from ._md_logger import Logger

def ler_pontos(aluno_id: int):
    try:
        with db:



            query = Pontuacao.select(
                Pontuacao.data,
                Pontuacao.tipo,
                Pontuacao.descricao,
                Pontuacao.quantidade_pontos,
                Pontuacao.total_antes,
                Pontuacao.total_apos,
            ).where(Pontuacao.aluno == aluno_id)

            resultado = list(query)
            if resultado:
                return True, resultado
            else:
                return False, None
    except Exception as e:
        Logger.error(f'Erro ao ler pontos: {e}')
        return False, None
