# Analise Câmbio

Projeto simples de Teste (DAG) Airflow

## Requisitos
* Ter uma instância do postgres rodando
* Ter o Apache Airflow instalado (ou em alguma instância na nuvem)
* Se inscrever [nesta api](https://rapidapi.com/exchangerateapi/api/exchangerate-api/) do RappidAPI

## Como rodar

Para rodar basta baixar o arquivo dag.py e movê-lo para o diretório de DAGs na pasta do Airflow. Em seguida basta rodar o **webserver** e **scheduler** e ir até o dashboard.

Lá basta rodar o DAG normalmente. 

## Setup
Você pode alterar os nomes de banco de dados e tabelas no arquivo dag.py. Também é possível adicionar as credenciais da api direto no arquivo.

Do jeito que está, você precisará de uma **_variável de ambiente_** chamada **ENV_PATH** que direciona para o arquivo .env que contém as credenciais. No código abaixo (encontra-se no arquivo dag.py), caso você não queira utilizar a variável d eambiente, basta apagar as duas linhas subjacentes ao comentário 'setting up the environment variable' e substituir o valores do dicionário pelas credenciais diretamente.

```Python
# setting up the environment variable
env_path = os.environ.get("ENV_PATH")
load_dotenv(f"{env_path}/.env")

# API connection config
url = "https://exchangerate-api.p.rapidapi.com/rapid/latest/USD"
headers = {
	"X-RapidAPI-Key": os.getenv("X-RapidAPI-Key"),
	"X-RapidAPI-Host": os.getenv("X-RapidAPI-Host")
}
```

## Flow
O que o dag faz basicamente é buscar os dados na api, mais especificamente o câmbio entre o **dólar USA**  e o **real brasileiro** guardando as informações de dia, mês e ano de câmbio.

O banco de dados deve possuir a seguinte tabela

|    |   Id   | usd   | brl  | dia | mês | ano |
|----| ------ | ----  | ---- | --- | --- | --- |
|Tipo| serial | real  | real | int | int | int | 


### Operators
Os operadores utilizados são apenas dois **PythonOperators** com as **funções get_data_api** e **put_data_postgres**

## Configurações do ambiente
Para editar o arquivo e rodar no ambiente virtual, você precisará do **Anaconda** instalado. Depois, basta rodar (dentro da pasta do projeto)
```bash
conda env create --prefix ./env -f environment.yml
```

Após isso basta ativar o ambiente via o seguinte comando (dentro da pasta do projeto)
```
conda activate ./env
```

Após isso basta editar o arquivo. Você também pode editar sem precisar instalar o ambiente, já que o DAG vai rodar dentro do airflow. Isso é só por questão de Sintaxe que as IDEs vão necessitar.