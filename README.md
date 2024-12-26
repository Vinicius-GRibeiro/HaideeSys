# Projeto HaideeSys

HaideeSys é um sistema de gerenciamento acadêmico desenvolvido com Python, utilizando o framework **Flet** para a interface gráfica e **Peewee** para o gerenciamento do banco de dados PostgreSQL.

## Funcionalidades

- **Gerenciamento de Alunos**:
  - Adicionar, editar, listar e buscar informações sobre alunos.
  - Registro de pontuações para alunos.

- **Gerenciamento de Séries**:
  - Criar e listar séries acadêmicas.

- **Controle de Ocorrências**:
  - Registro de eventos associados a alunos, incluindo assuntos e descrições detalhadas.
  - Consulta de ocorrências por ID, série ou aluno.

- **Controle de Presenças**:
  - Gerenciamento de chamadas e entradas associadas.

## Estrutura do Projeto

```plaintext
├── main.py                  # Ponto de entrada do sistema
├── .env                     # Variáveis de ambiente (configuração do banco de dados)
├── models/                  # Lógica e estrutura dos dados
│   ├── _md_entities.py      # Definição de entidades e conexão com o banco de dados
│   ├── _md_logger.py        # Sistema de log
│   ├── md_aluno.py          # Gerenciamento de alunos
│   ├── md_ocorrencia.py     # Gerenciamento de ocorrências
│   └── md_serie.py          # Gerenciamento de séries
├── views/                   # Camada de apresentação
│   ├── vw_inicio.py         # Tela inicial
│   └── vmodels/             # Componentes visuais
│       ├── view_factory.py  # Fábrica de visualizações
│       └── vmd_menu.py      # Menu de navegação
└── requirements.txt         # Dependências do projeto
```

## Tecnologias Utilizadas

- **Linguagem**: Python 3
- **Framework de Interface**: [Flet](https://flet.dev)
- **Banco de Dados**: PostgreSQL
- **ORM**: [Peewee](http://docs.peewee-orm.com/en/latest/)
- **Gerenciamento de Variáveis de Ambiente**: [python-dotenv](https://github.com/theskumar/python-dotenv)

## Configuração do Ambiente

1. **Pré-requisitos**:
   - Python 3.10+
   - PostgreSQL

2. **Configuração do Banco de Dados**:
   - Crie um banco de dados PostgreSQL.
   - Configure o arquivo `.env` com os seguintes parâmetros:
     ```plaintext
     DBNAME=nome_do_banco
     DBUSER=usuario
     DBPASSWORD=senha
     DBHOST=localhost
     DBPORT=5432
     APPDATA=caminho_do_appdata
     APPNAME=HaideeSys
     CLASSNAME=HaideeSys
     ```

3. **Instalação das Dependências**:
   - Execute o comando abaixo para instalar as bibliotecas necessárias:
     ```bash
     pip install -r requirements.txt
     ```

4. **Criação das Tabelas**:
   - Execute o arquivo `models/_md_entities.py` para criar as tabelas no banco de dados:
     ```bash
     python models/_md_entities.py
     ```

5. **Executando o Sistema**:
   - Execute o arquivo principal:
     ```bash
     python main.py
     ```

## Estrutura de Dados

- **Tabelas Principais**:
  - `Serie`: Representa séries acadêmicas.
  - `Aluno`: Alunos associados a séries, com atributos como nome, pontos e observações.
  - `Chamada`: Gerencia presenças por data e série.
  - `Ocorrencia`: Registra eventos relacionados a alunos.
  - `Pontuacao`: Histórico de pontuações atribuídas a alunos.

## Logs

O sistema registra logs em arquivos separados, localizados no diretório configurado em `APPDATA`:

- **info.log**: Informações gerais.
- **error.log**: Erros encontrados.
- **dev.log**: Mensagens para depuração.

