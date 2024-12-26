from _md_entities import db, Ocorrencia
from _md_logger import Logger
from datetime import datetime


def criar_ocorrencia(id_aluno: int, id_serie: str, oficina: str, assunto: str,
                     descricao: str, data: datetime.date = datetime.today().date()) -> tuple[bool, int | None]:
    """
    Todos os parâmetros, exceto data, são obrigatórios.
    :param id_aluno:
    :param id_serie:
    :param oficina:
    :param assunto:
    :param descricao:
    :param data:
    :return: Tupla, sendo o primeiro valor VERDADEIRO ou FALSO e o segundo valor, o id da ocorrência adicionada ou None caso algum erro tenha acontecido.
    """
    try:
        with db:
            ocorrencia = Ocorrencia(aluno=id_aluno, serie=id_serie, data=data,oficina=oficina, assunto=assunto,
                                    descricao=descricao)
            ocorrencia.save()

        Logger.info(f'Ocorrência criada para o aluno ({ocorrencia.aluno} - {ocorrencia.serie})')
        return True, ocorrencia.id
    except Exception as e:
        Logger.error(f'Erro ao criar ocorrência para o aluno ({id_aluno}): {e}')
        return False, None


def ler_ocorrencia(_id: int = None, _serie: str = None, _aluno: int = None) -> tuple[bool, list[Ocorrencia] | None]:
    """
    Caso nenhum parâmetro seja passado, todas as ocorrências serão retornadas.
    :param _id:
    :param _serie:
    :param _aluno:
    :return: Tuple, sendo o primeiro item VERDADEIRO ou FALSO, dependendo do sucesso da consulta e o segundo item, uma lista de instâncias de Ocorrência. Acesse os atributos da instância para obter o valor desejado. Ex.: Ocorrencia.assunto
     """
    try:
        with db:
            query = Ocorrencia.select()

            if _id is not None:
                query = query.where(Ocorrencia.id == _id)

            if _serie is not None:
                query = query.where(Ocorrencia.serie==_serie)

            if _aluno is not None:
                query = query.where(Ocorrencia.aluno==_aluno)

            resultado = list(query)
            if resultado:
                return True, resultado
    except Exception as e:
        Logger.error(f'Erro ao ler ocorrência: {e}')
        return False, None
