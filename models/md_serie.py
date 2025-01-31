from ._md_entities import db, Serie
from ._md_logger import Logger

def criar_serie(serie: str) -> bool:
    """

    :param serie: série no formato XY - Sendo X um número e Y uma letra
    :return: Verdadeiro ou falso
    """
    try:
        with db:
            Serie.create(id=serie)
        Logger.info(f'Série criada ({serie})')
        return True
    except Exception as e:
        Logger.error(f'Erro ao criar série ({serie}): {e}')
        return False


def ler_series() -> tuple[bool, tuple]:
    """
    :return: Tupla, sendo o primeiro item VERDADEIRO ou FALSO e o segundo item, uma tupla com as séries retornadas
    """

    try:
        with db:
            series = Serie.select()

        series = tuple(str(s.id) for s in series)
        Logger.info(f'Séries lidas ({series})')
        return True, series
    except Exception as e:
        Logger.error(f'Erro ao ler séries: {e}')
        return False, ()
