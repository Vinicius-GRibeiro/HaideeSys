from peewee import DoesNotExist
from ._md_entities import db, Aluno, Pontuacao
from ._md_logger import Logger

def criar_aluno(serie: str, nome: str, laudo: str = None, obs: str = None) -> tuple[bool, int | None]:
    """
    Cria um novo aluno no banco de dados.
    :return: Tupla (sucesso, ID do aluno criado ou None em caso de falha).
    """
    if not serie or not nome:
        Logger.error("Série e nome são obrigatórios para criar um aluno.")
        return False, None

    try:
        with db:
            aluno = Aluno.create(serie=serie, nome=nome, laudo=laudo, obs=obs)
        Logger.info(f'Aluno criado ({aluno.id} - {aluno.serie_id} - {aluno.nome})')
        return True, aluno.id
    except Exception as e:
        Logger.error(f'Erro ao criar aluno: {e}')
        return False, None

def editar_aluno(id_: int, _serie: str = None, _nome: str = None, _laudo: str = None, _obs: str = None,
                 _status: bool = None, _pontos: int = None) -> bool:
    """
    Edita informações de um aluno existente.
    :return: True se a operação for bem-sucedida, False caso contrário.
    """
    try:
        if not Aluno.select().where(Aluno.id == id_).exists():
            Logger.error(f"Aluno com ID {id_} não encontrado.")
            return False

        dados_atualizados = {
            'serie': _serie,
            'nome': _nome,
            'laudo': _laudo,
            'obs': _obs,
            'status': _status,
            'pontos': _pontos
        }

        dados_atualizados = {key: value for key, value in dados_atualizados.items() if value is not None}

        if dados_atualizados:
            with db:
                Aluno.update(dados_atualizados).where(Aluno.id == id_).execute()
            Logger.info(f'Aluno {id_} alterado com sucesso: {dados_atualizados}')
            return True

        Logger.warning(f"Nenhuma alteração realizada para o aluno {id_}.")
        return True
    except Exception as e:
        Logger.error(f'Erro ao alterar aluno: {e}')
        return False


def ler_aluno(id_: int = None, serie: str = None, nome: str = None, ordenar_por: str = 'nome', somente_ativos: bool = None) -> tuple[bool, list[Aluno] | None]:
    """
    Lê registros de alunos do banco de dados, ordenados por nome.
    Permite filtrar por ID, série e/ou nome simultaneamente.
    :return: Tupla (sucesso, lista de alunos ou None).
    """
    try:
        with db:
            query = Aluno.select()

            if id_ is not None:
                query = query.where(Aluno.id == id_)

            if serie is not None:
                query = query.where(Aluno.serie == serie)

            if nome is not None:
                query = query.where(Aluno.nome.ilike(f"%{nome}%"))

            if somente_ativos is not None:
                query = query.where(Aluno.status == True)

            match ordenar_por:
                case 'nome':
                    query = query.order_by(Aluno.nome.asc())
                case 'serie':
                    query = query.order_by(Aluno.serie.asc())
                case 'pontos':
                    query = query.order_by(Aluno.pontos.asc())
                case 'status':
                    query = query.order_by(Aluno.status.asc())

            aluno = list(query)

        if aluno:
            return True, aluno
        Logger.warning("Nenhum aluno encontrado.")
        return True, []
    except DoesNotExist:
        Logger.warning(f"Aluno com ID {id_} não encontrado.")
        return False, []
    except Exception as e:
        Logger.error(f'Erro ao ler aluno: {e}')
        return False, None


def excluir_aluno(id_: int) -> tuple[bool, Aluno | None]:
    """
    Exclui um aluno do banco de dados.
    :return: Tupla (sucesso, instância do aluno ou None).
    """
    try:
        with db:
            aluno = Aluno.get(Aluno.id == id_)

        aluno.delete_instance()
        Logger.info(f'Aluno excluído ({aluno.id} - {aluno.nome} - {aluno.serie_id})')
        return True, aluno
    except DoesNotExist:
        Logger.warning(f"Aluno com ID {id_} não encontrado.")
        return False, None
    except Exception as e:
        Logger.error(f'Erro ao excluir aluno: {e}')
        return False, None

def adicionar_pontos(id_: int, qntd_pontos: int, descricao: str) -> bool:
    if int(qntd_pontos) <= 0:
        Logger.error("Quantidade de pontos deve ser maior que zero.")
        return False

    try:
        with db:
            aluno = Aluno.get(Aluno.id == id_)
            Pontuacao.create(
                aluno=aluno.id,
                serie=aluno.serie_id,
                tipo=True,
                descricao=descricao,
                quantidade_pontos=int(qntd_pontos),
                total_antes=aluno.pontos,
                total_apos=aluno.pontos + int(qntd_pontos)
            )
            aluno.pontos += int(qntd_pontos)
            aluno.save()
        Logger.info(f'Pontos (+{qntd_pontos}) adicionados ao aluno {aluno.nome}.')
        return True
    except Exception as e:
        Logger.error(f'Erro ao adicionar pontos: {e}')
        return False

def remover_pontos(id_: int, qntd_pontos: int, descricao: str) -> bool:
    if int(qntd_pontos) <= 0:
        Logger.error("Quantidade de pontos deve ser maior que zero.")
        return False

    try:
        with db:
            aluno = Aluno.get(Aluno.id == id_)
            Pontuacao.create(
                aluno=aluno.id,
                serie=aluno.serie_id,
                tipo=False,
                descricao=descricao,
                quantidade_pontos=int(qntd_pontos),
                total_antes=aluno.pontos,
                total_apos=aluno.pontos - int(qntd_pontos)
            )
            aluno.pontos -= int(qntd_pontos)
            aluno.save()
        Logger.info(f'Pontos (-{qntd_pontos}) removidos do aluno {aluno.nome}.')
        return True
    except Exception as e:
        Logger.error(f'Erro ao remover pontos: {e}')
        return False

def contar_alunos(serie: str, status: bool = None) -> int:
    try:
        with db:
            alunos = Aluno.select().where(Aluno.serie == serie)

            if status is not None:
                alunos = alunos.where(Aluno.status == status)

            return alunos.count()
    except Exception as e:
        Logger.error(f'Erro ao contar alunos: {e}')
        return 0

# alunos = [
#     ["Ana Clara", "1A", None, None],
#     ["Bruno Henrique", "1B", "Dislexia", "Precisa de acompanhamento especial"],
#     ["Camila Souza", "1C", None, None],
#     ["Diego Martins", "1A", None, None],
#     ["Eduarda Oliveira", "1B", None, None],
#     ["Felipe Santos", "1C", "Déficit de atenção", "Monitoramento semanal recomendado"],
#     ["Gabriel Costa", "1A", None, None],
#     ["Heloísa Lima", "1B", None, None],
#     ["Igor Monteiro", "1C", "Autismo leve", "Recomenda-se apoio pedagógico adicional"],
#     ["Joana Silva", "1A", None, None],
#     ["Lucas Pereira", "1B", None, None],
#     ["Mariana Almeida", "1C", "Hiperatividade", "Dificuldade em manter o foco"],
#     ["Nicolas Ferreira", "1A", None, None],
#     ["Olivia Mendes", "1B", None, None],
#     ["Pedro Rocha", "1C", None, None],
#     ["Quésia Matos", "1A", None, None],
#     ["Rafael Dias", "1B", "Transtorno de ansiedade", "Monitoramento psicológico necessário"],
#     ["Sophia Santos", "1C", None, None],
#     ["Thiago Moreira", "1A", None, None],
#     ["Ursula Correia", "1B", None, None],
#     ["Victor Nogueira", "1C", "Dislexia", "Precisa de acompanhamento especial"],
#     ["Wesley Ribeiro", "1A", None, None],
#     ["Ximena Lopes", "1B", None, None],
#     ["Yasmin Cruz", "1C", None, None],
#     ["Zeca Oliveira", "1A", None, None],
#     ["Arthur Ramos", "1B", "Déficit de atenção", "Monitoramento semanal recomendado"],
#     ["Beatriz Castro", "1C", None, None],
#     ["Caio Cunha", "1A", None, None],
#     ["Daniela Ribeiro", "1B", None, None],
#     ["Eduardo Farias", "1C", None, None],
# ]
#
#
# for aluno in alunos:
#     criar_aluno(aluno[1], aluno[0], aluno[2], aluno[3])
