from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd

# Funções que simulam cada camada
def upload_raw_data_to_bronze():
    print("Carregando dados na Bronze...")
    # Simulando importação de dados externos
    df = pd.read_csv("/opt/airflow/base_externa/raw_data.csv")

    # Adicionando os dados na camada Bronze
    df.to_csv("/opt/airflow/data/bronze/subindo_dados.csv", index=False)
    print(df)

def process_bronze_to_silver():
    print("Transformando dados para Prata...")
    df = pd.read_csv("/opt/airflow/data/bronze/subindo_dados.csv")

    # Removendo linhas com valores nulos em colunas críticas
    df.dropna(subset=['name', 'email', 'date_of_birth'], inplace=True)

    # Corrigindo formatação de emails
    df['email'] = df['email'].str.replace('example.', '@example.', regex=False)

    # Calculando idade a partir da data de nascimento
    df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce')
    today = datetime.now()

    df['age'] = df['date_of_birth'].apply(
        lambda dob: today.year - dob.year - (
            (today.month, today.day) < (dob.month, dob.day)
            )
        )

    # Adicionando os dados limpos para a camada Prata
    df.to_csv("/opt/airflow/data/prata/limpeza_e_tratamento.csv", index=False)
    print(df)

def process_silver_to_gold():
    print("Carregando dados na Ouro...")
    df = pd.read_csv("/opt/airflow/data/prata/limpeza_e_tratamento.csv")
    
    bins = [0, 10, 20, 30, 40, 50, 100]
    labels = ["0-10", "11-20", "21-30", "31-40", "41-50", "50+"]

    df["faixa_etaria"] = pd.cut(df["age"], bins=bins, labels=labels)

    gold_df = (
        df.groupby(["faixa_etaria", "subscription_status"])
          .size()
          .reset_index(name="total_usuarios")
    )

    gold_df.to_csv(
        "/opt/airflow/data/ouro/usuarios_por_faixa_etaria.csv",
        index=False
    )

# Definindo o DAG
with DAG(
    dag_id="pipeline_bronze_prata_ouro",
    start_date=datetime(2026, 1, 30),
    schedule=None,
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="carregar_bronze",
        python_callable=upload_raw_data_to_bronze
    )

    t2 = PythonOperator(
        task_id="transformar_prata",
        python_callable=process_bronze_to_silver 
    )

    t3 = PythonOperator(
        task_id="carregar_ouro",
        python_callable=process_silver_to_gold
    )

    # Definindo a sequência das tarefas
    t1 >> t2 >> t3
