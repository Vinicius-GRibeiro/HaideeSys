from _md_entities import db, Aluno, Pontuacao
from _md_logger import Logger

def criar_aluno(serie: str, nome: str, laudo: str = None, obs: str = None) -> tuple[bool, int | None]:
    """
    :return: Tupla, sendo o primeiro item, VERDADEIRO ou FALSO e o segundo item, o id do aluno criado ou None, caso algum erro ocorra
    """
    try:
        with db:
            aluno = Aluno.create(
                serie=serie,
                nome=nome,
                laudo=laudo,
                obs=obs,
            )
        Logger.info(f'Aluno criado ({aluno.id} - {aluno.serie_id} - {aluno.nome})')
        return True, aluno.id
    except Exception as e:
        Logger.error(f'Erro ao criar aluno: {e}')
        return False, None



def editar_aluno(id_: int, _serie: str = None, _nome: str = None, _laudo: str = None, _obs: str = None,
                 _status: bool = None, _pontos: int = None) -> bool:
    """
    Todos os parâmetros, exceto o id, são opcionais. Passe somente os parâmetros que deseja alterar.
    :return: VERDADEIRO ou FALSO, dependendo do sucesso da operação.
    """

    try:
        dados_atualizados = {
            'serie': _serie,
            'nome': _nome,
            'laudo': _laudo,
            'obs': _obs,
            'status': _status,
            'pontos': _pontos
        }

        # Filtrar campos não nulos
        dados_atualizados = {key: value for key, value in dados_atualizados.items() if value is not None}

        if dados_atualizados:  # Verifica se há algum campo para atualizar
            with db:
                Aluno.update(dados_atualizados).where(Aluno.id == id_).execute()

            Logger.info(f'Aluno {id_} alterado com sucesso')
            return True

        Logger.info(f'Aluno alterado')
        return True
    except Exception as e:
        Logger.error(f'Erro ao alterar aluno: {e}')
        return False


def ler_aluno(id_: int) -> tuple[bool, Aluno | None]:
    """
    :return: Retorna uma instância de Aluno. Para ler algum valor, leia os atributos desta instância. Ex.: Aluno.nome
    """
    try:
        with db:
            aluno = Aluno.get(Aluno.id == id_)
        if aluno:
            return True, aluno
    except Exception as e:
        Logger.error(f'Erro ao ler aluno: {e}')
        return False, None


def excluir_aluno(id_: int) -> tuple[bool, Aluno | None]:
    """
    :return: Tupla, sendo o primeiro item VERDADEIRO ou FALSO e o segundo item uma instância de Aluno ou None, dependendo do sucesso da operação.
    """
    try:
        with db:
            aluno = Aluno.get(Aluno.id == id_)

        if aluno:
            aluno.delete_instance()
            Logger.info(f'Aluno excluído ({aluno.id} - {aluno.nome} - {aluno.serie_id})')
            return True, aluno
    except Exception as e:
        Logger.error(f'Erro ao excluir aluno: {e}')
        return False, None


def adicionar_pontos(id_: int, qntd_pontos: int, descricao: str) -> bool:
    """
    :return: VERDADEIRO OU FALSO, dependendo do sucesso da operação
    """
    try:
        with db:
            aluno = Aluno.get(Aluno.id == id_)
            Pontuacao.create(aluno=aluno.id,serie=aluno.serie_id, tipo=True, descricao=descricao,
                             quantidade_pontos=qntd_pontos, total_antes=aluno.pontos,
                             total_apos=aluno.pontos + qntd_pontos)
            aluno.pontos += qntd_pontos
            aluno.save()
            Logger.info(f'Pontos (+{qntd_pontos}) adicionados para o aluno ({aluno.id} - {aluno.serie_id} - {aluno.nome})')
        return True
    except Exception as e:
        Logger.error(f'Erro ao adicionar_pontos: {e}')
        return False


def remover_pontos(id_: int, qntd_pontos: int, descricao: str) -> bool:
    """
    :return: VERDADEIRO OU FALSO, dependendo do sucesso da operação
    """
    try:
        with db:
            aluno = Aluno.get(Aluno.id == id_)
            Pontuacao.create(aluno=aluno.id,serie=aluno.serie_id, tipo=False, descricao=descricao,
                             quantidade_pontos=qntd_pontos, total_antes=aluno.pontos,
                             total_apos=aluno.pontos - qntd_pontos)
            aluno.pontos -= qntd_pontos
            aluno.save()
            Logger.info(f'Pontos (-{qntd_pontos}) removidos do aluno ({aluno.id} - {aluno.serie_id} - {aluno.nome})')
        return True
    except Exception as e:
        Logger.error(f'Erro ao remover pontos: {e}')
        return False
