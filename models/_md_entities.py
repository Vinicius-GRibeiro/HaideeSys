from dotenv import load_dotenv
from ._md_logger import Logger
import os
from datetime import datetime
from peewee import (
    PostgresqlDatabase, Model, CharField, AutoField, IntegerField,
    BooleanField, ForeignKeyField, TextField, DateField, DateTimeField
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
    created_at = DateTimeField(default=datetime.now, index=True)
    updated_at = DateTimeField(default=datetime.now, index=True)

    class Meta:
        database = db

    @classmethod
    def criar_tabela_com_gatilhos(cls):
        """
        Cria a tabela e adiciona triggers para os campos created_at e updated_at no PostgreSQL.
        """
        # Criar a tabela normalmente
        db.create_tables([cls])

        # Nome da tabela e campo atualizado
        table_name = cls._meta.table_name
        updated_at_field = 'updated_at'

        # SQL para criar a função de trigger
        trigger_function_sql = f"""
        CREATE OR REPLACE FUNCTION {table_name}_updated_at_trigger()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.{updated_at_field} = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """

        # SQL para criar o trigger condicionalmente
        trigger_sql = f"""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_trigger
                WHERE tgname = '{table_name}_update_trigger'
            ) THEN
                CREATE TRIGGER {table_name}_update_trigger
                BEFORE UPDATE ON {table_name}
                FOR EACH ROW
                EXECUTE FUNCTION {table_name}_updated_at_trigger();
            END IF;
        END;
        $$;
        """

        # Executar os comandos SQL
        db.execute_sql(trigger_function_sql)  # Criar/atualizar a função de trigger
        db.execute_sql(trigger_sql)  # Criar o trigger, se não existir


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


# Tabela: Pontuacao
class DescricaoPontos(BaseModel):
    id = AutoField(primary_key=True)
    tipo = BooleanField(null=False, default=True)
    descricao = TextField(null=False)
    pontos = IntegerField(null=False)

    class Meta:
        table_name = 'descricao_pontos'

# Função para criar as tabelas
def criar_tabelas():
    try:
        with db:
            # Serie.criar_tabela_com_gatilhos()
            # Aluno.criar_tabela_com_gatilhos()
            # Chamada.criar_tabela_com_gatilhos()
            # EntradaChamada.criar_tabela_com_gatilhos()
            # Ocorrencia.criar_tabela_com_gatilhos()
            # Pontuacao.criar_tabela_com_gatilhos()
            DescricaoPontos.criar_tabela_com_gatilhos()
            Logger.info('Tabelas criada com sucesso!')
    except Exception as e:
            Logger.error(f'Erro ao criar tabelas: {e}')

if __name__ == '__main__':
    criar_tabelas()
