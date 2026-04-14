# Pipeline ETL Bronze → Prata → Ouro com Apache Airflow e Docker

Pipeline de dados orquestrado com Apache Airflow e containerizado com Docker, implementando a arquitetura medallion (Bronze, Prata, Ouro) para processamento e transformação de dados de usuários.

---

## Arquitetura

raw_data.csv

Bronze  →  Ingestão dos dados brutos
    
Prata  →  Limpeza, correção e enriquecimento
    
Ouro  →  Agregação por faixa etária e status
```

---

## O que o pipeline faz

**Camada Bronze — `carregar_bronze`**
- Lê o arquivo CSV de dados brutos
- Carrega os dados sem transformação na camada Bronze

**Camada Prata — `transformar_prata`**
- Remove registros com campos críticos nulos (nome, email, data de nascimento)
- Corrige emails inválidos sem o caractere `@`
- Calcula a idade de cada usuário a partir da data de nascimento

**Camada Ouro — `carregar_ouro`**
- Classifica usuários em faixas etárias (0-10, 11-20, 21-30, 31-40, 41-50, 50+)
- Agrega o total de usuários por faixa etária e status (active/inactive)
- Gera dataset pronto para análise estratégica e dashboards

---

## Tecnologias utilizadas

- Apache Airflow 2.9
- Docker + Docker Compose
- Python 3.12
- Pandas / NumPy
- WSL2 (Ubuntu 24.04)

---

## Estrutura do projeto

```
dags/
│── pipeline_etapas.py       # DAG com as 3 tarefas do pipeline
data/
├── bronze/                  # Dados brutos ingeridos
├── prata/                   # Dados limpos e enriquecidos
│── ouro/                    # Dados agregados prontos para análise
base_externa/
|── raw_data.csv             # Fonte de dados fictícios de usuários
docker-compose.yaml          # Configuração do Airflow com LocalExecutor
requirements.txt
```

---

## Como executar

**Pré-requisitos:** Docker, Docker Compose e WSL2 instalados.

```bash
# Clone o repositório
git clone https://github.com/BrunoP93/pipeline-etl-airflow-docker.git
cd pipeline-etl-airflow-docker

# Ajusta permissões
sudo chmod -R 777 data/ logs/

# Inicializa o banco de dados do Airflow
docker-compose up airflow-init

# Sobe o ambiente
docker-compose up -d airflow-webserver airflow-scheduler
```

Acesse `http://localhost:8080` com usuário `airflow` e senha `airflow`.

Localize o DAG `pipeline_bronze_prata_ouro`, ative-o e clique em **Trigger DAG** para executar.

---

## Resultado

Após a execução, os arquivos gerados são:

| Camada | Arquivo | Conteúdo |

| Bronze | `subindo_dados.csv` | Dados brutos originais |
| Prata | `limpeza_e_tratamento.csv` | Dados limpos com coluna `age` calculada |
| Ouro | `usuarios_por_faixa_etaria.csv` | Total de usuários por faixa etária e status |

---

## Sobre

Projeto desenvolvido como parte da minha formação em Engenharia de Dados, simulando um ambiente de produção com orquestração real de pipeline via Airflow e isolamento de ambiente via Docker.
