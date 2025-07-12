import os

import requests
from dotenv import load_dotenv

from utils import currency_convertor

load_dotenv()
from datetime import datetime


def get_greeting(date_str: str) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    time = datetime.strptime(date_str, "%d-%m-%Y %H:%M:%S").time()
    if 5 <= time.hour < 12:
        return "Доброе утро"
    elif 12 <= time.hour < 17:
        return "Добрый день"
    elif 17 <= time.hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_card_stats(df) -> list[dict]:
    """
    Возвращает список словарей с информацией по каждой карте:
    последние 4 цифры, общая сумма, кешбэк.
    """
    grouped = df.groupby("Номер карты")["Сумма платежа"].sum().reset_index()

    result = []
    for column, row in grouped.iterrows():
        last_digits = str(row["Номер карты"])
        total_spent = round(row["Сумма платежа"], 2)
        cashback = round(total_spent / 100, 2)

        result.append({
            "last_digits": last_digits,
            "total_spent": total_spent,
            "cashback": cashback
        })

    return result


def get_top_transactions(df) -> list[dict]:
    """Возвращает топ-5 транзакций по убыванию суммы платежа."""
    df_sorted = df.sort_values(by="Сумма платежа", ascending=False).head(5)

    result = []
    for _, row in df_sorted.iterrows():
        result.append({
            "date": row["Дата операции"].strftime("%d.%m.%Y"),
            "amount": round(row["Сумма платежа"], 2),
            "category": row["Категория"],
            "description": row["Описание"]
        })

    return result

def get_currency_rates(symbols: str, base = "RUB") -> list[dict]:

    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols}&base={base}"

    payload = {}
    headers = {
        "apikey": os.getenv("API_KEY_LAYER")
    }

    response = requests.get(url, headers=headers, data=payload)
    result = response.json().get("rates")
    result_list =[]
    for i,v in result.items():
        result_dict = {"currency": i, "rates": round(1/v, 2)}
        result_list.append(result_dict)

    return result_list

# if __name__ == '__main__':
#     print(get_currency_rates("EUR, USD"))

def get_share_price(symbol: str) -> list[dict]:
    apikey = os.getenv("API_KEY_12")
    url = f"https://api.twelvedata.com/eod?symbol={symbol}&apikey={apikey}"

    payload = {}

    response = requests.get(url, data=payload)
    result = response.json()
    symbol_price = currency_convertor(result.get("currency"), result.get("close"))

    result_list =[]
    for i,v in result.items():
    result_dict = {"currency": i, "rates": round(1/v, 2)}
    result_list.append(result_dict)

    return result_list

if __name__ == '__main__':
    print(get_share_price("AAPL"))






