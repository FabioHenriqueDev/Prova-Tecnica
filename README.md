# Company Intelligence

Aplicacao em Python para extrair informacoes estruturadas de empresas do setor de saude a partir do conteudo de seus sites. O sistema combina scraping, um modelo de linguagem da OpenAI, validacao tipada e persistencia em banco relacional.

## Objetivo

O usuario informa a URL de um site corporativo e a aplicacao:

1. baixa e limpa o HTML da pagina;
2. converte o conteudo para Markdown;
3. envia o texto para um agente de IA;
4. extrai dados institucionais, segmentos medicos, produtos e certificacoes;
5. valida a resposta com Pydantic;
6. salva os dados no SQLite;
7. exibe as empresas cadastradas em uma interface Streamlit.

## Arquitetura da solucao

O projeto segue uma separacao em camadas, com responsabilidades organizadas da seguinte forma:

```text
Interface Streamlit
	|
	v
Fluxo de extracao
	|
	+--> Scraping HTTP e conversao HTML para Markdown
	|
	+--> Agente OpenAI com resposta estruturada
	|
	+--> Schema Pydantic
	|
	+--> Entidades de dominio
	|
	+--> Servicos de aplicacao
	|
	+--> Repositories
	|
	+--> SQLAlchemy / SQLite
```

### Interface

- `main.py`: ponto de entrada da aplicacao e navegacao lateral.
- `extrair_dados.py`: formulario para entrada da URL e acompanhamento do processamento.
- `empresas_cadastradas.py`: consulta e exibicao das empresas, produtos, segmentos e certificacoes.

### Scraping

`src/scraping/scrap.py` usa `requests`, `BeautifulSoup` e `markdownify` para:

- requisitar o site informado;
- remover tags `script` e `style`;
- converter o HTML restante para Markdown;
- salvar o resultado em `site.md`.

### Agente de IA

`src/agent/agent.py` usa a API da OpenAI com o modelo `gpt-4o-mini`. O prompt em `src/prompt/prompt.py` orienta a extracao de:

- dados institucionais;
- classificacao do tipo de negocio;
- segmentos medicos;
- produtos e imagens;
- certificacoes.

O retorno e convertido para `CompanyExtraction`, definido em `src/schemas/schema.py`. Isso reduz o risco de a aplicacao trabalhar com uma resposta livre e sem estrutura.

### Dominio e servicos

- `src/domain/entities`: entidades `Company` e `CompanyProducts`, com validacoes de dominio.
- `src/services/company_services.py`: coordena a extracao, transforma os dados da IA em entidades e persiste os relacionamentos.
- `src/errors`: excecoes especificas para empresa e produto.

### Persistencia

`src/database/database.py` configura o SQLAlchemy e o banco SQLite em `db/companies.db`.

As entidades persistidas em `src/model/models.py` sao:

- `companies`: dados principais da empresa;
- `company_products`: produtos associados;
- `company_medical_segments`: segmentos medicos associados;
- `company_certifications`: certificacoes associadas.

Os repositories em `src/repositories` encapsulam a criacao e a consulta desses registros.

## Tecnologias utilizadas

| Tecnologia | Uso |
|---|---|
| Python | Linguagem principal |
| Streamlit | Interface web interativa |
| Requests | Requisicoes HTTP |
| BeautifulSoup | Parsing e limpeza do HTML |
| Markdownify | Conversao de HTML para Markdown |
| OpenAI API | Extracao e classificacao com IA |
| Pydantic | Validacao e tipagem da resposta da IA |
| SQLAlchemy | ORM e mapeamento relacional |
| SQLite | Persistencia local |
| python-dotenv | Carregamento de configuracoes do ambiente |
| SQLAlchemy Utils | Tipo de escolha para o tipo de negocio |

## Estrutura de diretorios

```text
.
|-- main.py                         # Entrada da aplicacao
|-- extrair_dados.py                # Tela e fluxo de extracao
|-- empresas_cadastradas.py         # Tela de consulta
|-- create_table.py                 # Criacao das tabelas
|-- site.md                         # Snapshot do ultimo site processado
|-- dados.json                      # Ultima resposta bruta salva da IA
|-- db/companies.db                 # Banco SQLite local
|-- src/
    |-- agent/                      # Integracao com OpenAI
    |-- database/                   # Engine e sessoes SQLAlchemy
    |-- domain/entities/            # Entidades e regras de dominio
    |-- errors/                     # Excecoes de negocio
    |-- model/                      # Modelos ORM
    |-- prompt/                     # Prompt do agente
    |-- repositories/               # Acesso aos dados
    |-- schemas/                    # Schemas Pydantic
    |-- scraping/                   # Coleta e conversao do site
    |-- services/                   # Orquestracao da aplicacao
```

## Como executar

### Pre-requisitos

- Python 3.10 ou superior;
- uma chave da API da OpenAI;
- acesso a internet para scraping e chamada da API.

### Configuracao

Crie um ambiente virtual e instale as dependencias do projeto. Como o repositorio ainda nao possui um arquivo de dependencias versionado, os pacotes utilizados atualmente incluem:

```bash
pip install streamlit requests beautifulsoup4 markdownify openai python-dotenv sqlalchemy sqlalchemy-utils pydantic email-validator
```

Crie um arquivo `.env` local:

```env
OPENAI_API_KEY=sua-chave-aqui
```

Nunca versione esse arquivo nem compartilhe a chave. Caso uma chave real tenha sido exposta ou enviada ao Git, ela deve ser revogada e substituida imediatamente.

### Banco de dados

Execute uma vez:

```bash
python create_table.py
```

### Aplicacao

```bash
streamlit run main.py
```

## Logica aplicada

O sistema usa uma abordagem de pipeline:

```text
URL
 -> requisicao HTTP
 -> HTML limpo
 -> Markdown
 -> prompt + conteudo do site
 -> CompanyExtraction
 -> entidades de dominio
 -> modelos SQLAlchemy
 -> banco de dados
 -> exibicao no Streamlit
```

O agente deve retornar somente dados encontrados no site. Campos textuais ausentes devem ser `null` e listas sem resultados devem ser vazias. O schema Pydantic tambem restringe `business_type` aos valores `MANUFACTURER`, `DISTRIBUTOR` e `SERVICE PROVIDER`.

## Limitações conhecidas

### Robustez

- O scraping nao define timeout, nao chama `raise_for_status()` e possui tratamento limitado de falhas de rede.
- O sistema processa essencialmente uma pagina por vez e nao navega de forma controlada por links internos.
- Sites renderizados principalmente por JavaScript podem retornar pouco conteudo.
- O conteudo inteiro e enviado ao modelo, sem limite, resumo ou controle de tokens.
- O fluxo possui pausas fixas com `sleep`, aumentando o tempo de processamento.

### Concorrencia e estado

- `site.md` e `dados.json` sao arquivos compartilhados pelo processo.
- Duas execucoes simultaneas podem sobrescrever os arquivos uma da outra.
- SQLite e adequado para uso local, mas nao e a melhor opcao para varias instancias ou alta concorrencia.

### Dados e transacoes

- Nao existe migration versionada; as tabelas sao criadas diretamente com `create_all`.
- Nao ha tratamento dedicado para empresa duplicada, apesar de `name` ser unico no banco.
- A responsabilidade de persistencia dos repositories nao e totalmente uniforme.
- A tela de consulta carrega e filtra dados em Python, o que pode degradar com muitos registros.

### Validacao e erros

- Algumas validacoes de dominio existem, mas nao sao chamadas em todos os fluxos.
- Campos opcionais do schema podem entrar em conflito com restricoes das entidades ou do banco.
- A interface pode exibir sucesso mesmo depois de uma falha capturada no processamento.
- Nao ha logs estruturados, monitoramento ou rastreabilidade por execucao.

### Seguranca

- A URL informada pelo usuario e requisitada diretamente, sem protecoes contra SSRF.
- A chave da OpenAI deve permanecer somente em secret manager ou variavel de ambiente local.
- Nao existe autenticacao ou autorizacao para acessar os dados cadastrados.
- O texto coletado de sites externos e enviado a um modelo de terceiros, o que exige avaliacao de privacidade e compliance.

### Qualidade do projeto

- Ainda nao ha testes automatizados.

## Melhorias futuras

### Prioridade alta

1. Revogar qualquer chave da OpenAI exposta e garantir que `.env` nunca seja versionado.
2. Criar testes unitarios para entidades, schemas e repositories.
3. Criar testes de integracao para o fluxo completo de scraping, IA e persistencia.
4. Adicionar `requirements.txt` ou `pyproject.toml` com versoes fixadas.

### Prioridade media

1. Adotar migrations com Alembic (Não implementado por falta de tempo).
2. Substituir `sleep` fixo por controle adequado de timeout, retry e backoff.
3. Adicionar deduplicacao por website e tratamento de conflitos de unicidade.
4. Melhorar o carregamento de dados usando consultas filtradas e relacionamentos SQLAlchemy.
5. Criar uma camada de configuracao para modelo, limites, banco e parametros de scraping (Não implementado por falta de tempo).
6. Registrar logs com identificador de cada processamento.

### Evolucao arquitetural

1. Criar uma API com FastAPI para desacoplar backend e interface (Não implementado por falta de tempo).
2. Usar uma fila de tarefas para processamentos demorados.
3. Migrar para PostgreSQL em ambientes compartilhados (Não implementado por falta de tempo).
4. Adicionar cache de sites e controle de versao das extracoes.
5. Implementar busca, filtros e paginação para empresas e produtos.
6. Adicionar autenticação, autorizacao e auditoria.
7. Criar pipeline de CI com lint, type checking, testes e verificacao de segredos.

## Estado atual

O projeto e um prototipo funcional de inteligencia de mercado. Ele demonstra a integracao entre coleta de dados, IA generativa, validacao estruturada e persistencia relacional. 
