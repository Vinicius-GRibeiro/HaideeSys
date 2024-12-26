from dotenv import load_dotenv
from _md_logger import Logger
import os
from datetime import datetime
from peewee import (
    PostgresqlDatabase, Model, CharField, AutoField, IntegerField,
    BooleanField, ForeignKeyField, TextField, DateField
)

# Carregar variáveis do arquivo .env
load_dotenv()

# Conexão com o banco
db = PostgresqlDatabase(
    database=os.getenv('DBNAME', 'haydeedb'),
    user=os.getenv('DBUSER', 'postgres'),
    password=os.getenv('DBPASSWORD', '123'),
    host=os.getenv('DBHOST', 'localhost'),
    port=int(os.getenv('DBPORT', 5432))
)


# Classe base
class BaseModel(Model):
    class Meta:
        database = db


# Tabela: Serie
class Serie(BaseModel):
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'serie'


# Tabela: Aluno
class Aluno(BaseModel):
    id = AutoField(primary_key=True)
    serie = ForeignKeyField(Serie, backref='alunos', null=False, on_delete='SET NULL', on_update='CASCADE')
    nome = CharField(max_length=100, null=False)
    laudo = TextField(null=True)
    obs = TextField(null=True)
    status = BooleanField(null=False, default=True)
    pontos = IntegerField(default=0)

    class Meta:
        table_name = 'aluno'


# Tabela: Chamada
class Chamada(BaseModel):
    id = AutoField(primary_key=True)
    data = DateField(null=False, default=datetime.today().date())
    serie = ForeignKeyField(Serie, backref='chamadas', on_delete='CASCADE')

    class Meta:
        table_name = 'chamada'


# Tabela: EntradaChamada
class EntradaChamada(BaseModel):
    id = AutoField(primary_key=True)
    chamada = ForeignKeyField(Chamada, backref='entradas', on_delete='CASCADE')
    aluno = ForeignKeyField(Aluno, backref='presencas', on_delete='CASCADE')
    presenca = BooleanField(null=False, default=True)

    class Meta:
        table_name = 'entradachamada'


# Tabela: Ocorrencia
class Ocorrencia(BaseModel):
    id = AutoField(primary_key=True)
    aluno = ForeignKeyField(Aluno, backref='ocorrencias', on_delete='CASCADE')
    serie = ForeignKeyField(Serie, backref='ocorrencias_serie', on_delete='CASCADE')
    data = DateField(null=False, default=datetime.today().date())
    oficina = CharField(max_length=100, null=False)
    assunto = CharField(max_length=100, null=False)
    descricao = TextField(null=False)

    class Meta:
        table_name = 'ocorrencia'


# Tabela: Pontuacao
class Pontuacao(BaseModel):
    id = AutoField(primary_key=True)
    aluno = ForeignKeyField(Aluno, backref='pontuacoes', on_delete='CASCADE')
    serie = ForeignKeyField(Serie, backref='pontuacoes_serie', on_delete='CASCADE')
    data = DateField(null=False, default=datetime.today().date())
    tipo = BooleanField(null=False)
    descricao = TextField(null=False)
    quantidade_pontos = IntegerField(null=False)
    total_antes = IntegerField(null=False)
    total_apos = IntegerField(null=False)

    class Meta:
        table_name = 'pontuacao'


# Função para criar as tabelas
def criar_tabelas():
    try:
        with db:
            db.create_tables([Serie, Aluno, Chamada, EntradaChamada, Ocorrencia, Pontuacao])
            Logger.info('Tabelas criada com sucesso!')
    except Exception as e:
            Logger.error(f'Erro ao criar tabelas: {e}')

if __name__ == '__main__':
    criar_tabelas()
