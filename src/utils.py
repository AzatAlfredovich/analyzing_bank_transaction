import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


def reading_xlsx(file_path: str) -> list[dict]:
    """Функция, переводящая Excel-файл в список словарей"""
    df = pd.read_excel(file_path)
    result = df.to_dict(orient="records")
    return result

def currency_convertor(currency: str, amount: float) -> float:
    """Функция, которая обращается к API для получения текущего курса валюты и конвертации"""
    new_currency = "RUB"
    url = "https://api.apilayer.com/exchangerates_data/convert"

    payload: dict = {"to": new_currency, "from": currency, "amount": amount}
    headers = {"apikey": os.getenv("API_KEY_LAYER")}

    response = requests.get(url, headers=headers, params=payload)
    return float(response.json().get("result"))


