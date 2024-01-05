from datetime import datetime
from dotenv import load_dotenv
import requests
import os
import pytz

# setting up the environment variable
env_path = os.environ.get("ENV_PATH")
load_dotenv(f"{env_path}/.env")

# API connection config
url = "https://exchangerate-api.p.rapidapi.com/rapid/latest/USD"
headers = {
	"X-RapidAPI-Key": os.getenv("X-RapidAPI-Key"),
	"X-RapidAPI-Host": os.getenv("X-RapidAPI-Host")
}

def get_data_api():
    """
    Makes a request to the XRapid api and return the data received

    Returns\n
    dict {
        usd: float,
        brl: float,
        day: int,
        month: int,
        year: int
    }
    """

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

    return data

def put_data_postgres():
    pass


# setting up the dag
with Dag(

) as dag:
    task_data_apit = Pytho

get_data_api()