from typing import Tuple, List, Any

from ._md_entities import db, DescricaoPontos
from ._md_logger import Logger


def criar_descricao_pontos(tipo: bool, descricao: str, pontos: int) -> bool:
    """

    :param tipo: True para adicionar ou False para remover
    :param descricao: descrição dos pontos
    :return: Verdadeiro ou falso
    """
    try:
        with db:
            DescricaoPontos.create(tipo=tipo, descricao=descricao, pontos=pontos)
        Logger.info(f'Descrição criada. Tipo: {tipo}, descrição: {descricao}')
        return True
    except Exception as e:
        Logger.error(f'Erro ao criar descrição. Tipo: {tipo}, descrição: {descricao}. Erro: {e}')
        return False

def excluir_descricao_pontos(tipo: bool, descricao: str) -> bool:
    try:
        with db:
            descricao = DescricaoPontos.get(DescricaoPontos.tipo == tipo, DescricaoPontos.descricao == descricao)
        descricao.delete_instance()
        Logger.info(f'Descrição de pontos excluída. Tipo: {tipo}, descrição = {descricao}')
        return True
    except Exception as e:
        Logger.error(f'Erro ao excluir descrição. Tipo: {tipo}, descrição: {descricao}. Erro: {e}')
        return False

def ler_descricao(tipo: bool = None, retornar_ponto: bool = False, descricao: str = None) -> tuple[bool, list[Any]] | tuple[bool, None]:
    try:
        if retornar_ponto and descricao is not None:
            with db:
                query = DescricaoPontos.select().where(DescricaoPontos.descricao == descricao)
            pontos = list(query)[0].pontos
            return pontos

        with db:
            query = DescricaoPontos.select().where(DescricaoPontos.tipo == tipo).order_by(DescricaoPontos.descricao.asc())
        descricao = list(query)

        if descricao:
            return True, descricao
        else:
            return False, None
    except Exception as e:
        Logger.error(f'Erro ao ler descrições: {e}')
        return False, None
