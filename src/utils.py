import os

import finnhub
import pandas as pd
import requests
from dotenv import load_dotenv
from pandas import DataFrame

load_dotenv()


def reading_xlsx(file_path: str) -> DataFrame:
    """Функция, переводящая Excel-файл в список словарей"""
    df = pd.read_excel(file_path)
    return df


def filter_by_date(df: DataFrame, end_date_str: str) -> pd.DataFrame:
    """
    Возвращает данные с начала месяца до переданной даты включительно.
    """
    df = df.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    end_date = pd.to_datetime(end_date_str)

    start_date = end_date.replace(day=1)
    return df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]


def get_currency_rates(symbols: list[str], base="RUB") -> list[dict]:
    """Получает текущие курсы указанных валют с помощью API Finnhub"""
    result_list = []
    for symbol in symbols:

        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={base}&base={symbol}"

        payload = {}
        headers = {"apikey": os.getenv("API_KEY_LAYER")}

        response = requests.get(url, headers=headers, data=payload)
        result = response.json().get("rates")
        result_dict = {"currency": symbol, "rate": result.get(base)}
        result_list.append(result_dict)

    return result_list


if __name__ == "__main__":
    print(get_currency_rates(["EUR", "USD"]))
    # [{'currency': 'EUR', 'rate': 91.210065}, {'currency': 'USD', 'rate': 78.021461}]


def get_stock_prices(stocks: list[str]) -> list[dict]:
    """Получает текущие цены указанных акций с помощью API APIlayer"""
    finnhub_key = os.getenv("FINNHUB_API_KEY")

    client = finnhub.Client(api_key=finnhub_key)
    results = []

    for stock in stocks:
        try:
            quote = client.quote(stock)
            price = quote.get("c")  # текущая цена
            if price:
                results.append({"stock": stock, "price": round(price, 2)})
        except Exception as e:
            results.append({"stock": stock, "price": 0.0})
            print(f"Ошибка при получении цены для {stock}: {e}")

    return results


# if __name__ == '__main__':
#     print(get_stock_prices(["AAPL", "TSLA"]))
