from dotenv import load_dotenv
from datetime import timedelta
from datetime import datetime

import requests
import os
import pytz
import json
import psycopg2

# airflow
from airflow import DAG
from airflow.operators.python import PythonOperator

# setting up the environment variable
env_path = os.environ.get("ENV_PATH")
load_dotenv(f"{env_path}/.env")

# API connection config
url = "https://exchangerate-api.p.rapidapi.com/rapid/latest/USD"
headers = {
	"X-RapidAPI-Key": os.getenv("X-RapidAPI-Key"),
	"X-RapidAPI-Host": os.getenv("X-RapidAPI-Host")
}

def get_data_api(task_instance):
    response = requests.get(url, headers=headers)
    resjson = response.json()

    # converting the string
    date_str_utc = resjson["time_last_update_utc"]
    date_format = "%a, %d %b %Y %H:%M:%S %z"

    # converting the data
    br_date = datetime.strptime(date_str_utc, date_format).replace(tzinfo=pytz.UTC).astimezone(
        pytz.timezone('America/Sao_Paulo')
    )

    # creating the data
    data = {
        "usd": float(resjson["rates"]["USD"]),
        "brl": float(resjson["rates"]["BRL"]),
        "day": int(br_date.day),
        "month": int(br_date.month),
        "year": int(br_date.year)
    }

    # small data - pass via XCom
    task_instance.xcom_push(key="currency_exchange", value=json.dumps(data))


def put_data_postgres(task_instance):
    # getting data via XCom
    xcom = task_instance.xcom_pull(key="currency_exchange", task_ids="get-api-data-task")
    data = json.loads(xcom)


    # creating connection
    conn = psycopg2.connect(
        database="currency",
        user="postgres",
        password="postgres",
        host="127.0.0.1",
        port="5432"
    )

    # creating cursor to make requests
    cur = conn.cursor()

    query = f"INSERT INTO EXCHANGES(usd, brl, day, month, year) VALUES({data['usd']}, {data['brl']}, {data['day']}, {data['month']}, {data['year']})"

    # executing query
    cur.execute(query)

    # commiting changes
    conn.commit()

    # closing the connection
    conn.close()




# setting up the dag
with DAG(
    "currency-exchange-dag",
    start_date=datetime.now(),
    schedule=timedelta(hours=24),
    catchup=False,
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=20)
    }
) as dag:
    
    # setting up tasks
    task_data_api = PythonOperator(
        task_id="get-api-data-task",
        python_callable=get_data_api
    )

    task_pgsql = PythonOperator(
        task_id="insert-into-postgres-task",
        python_callable=put_data_postgres
    )

    # setting up downstream and upstream
    task_data_api >> task_pgsql
    task_pgsql << task_data_api
