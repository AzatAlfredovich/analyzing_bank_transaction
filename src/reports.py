import pandas as pd
import json
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Optional, Callable


def save_report(func: Optional[Callable] = None, *, filename: Optional[str] = None):
    """
    Декоратор для сохранения результата функции-отчета в JSON-файл.
    Работает только если аргумент save_to_file=True
    """
    def decorator(inner_func):
        @wraps(inner_func)
        def wrapper(*args, **kwargs):
            result = inner_func(*args, **kwargs)
            if kwargs.get("save_to_file"):
                report_filename = filename or f"logs/report_{inner_func.__name__}.json"
                try:
                    with open(report_filename, "w", encoding="utf-8") as f:
                        json.dump(result, f, ensure_ascii=False, indent=2)
                except Exception as e:
            return result
        return wrapper

    if callable(func):
        return decorator(func)
    return decorator


@save_report
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None, save_to_file: bool = False) -> list[dict]:
    """Возвращает траты по заданной категории за последние три месяца от указанной даты."""
    if date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, "%d.%m.%Y")

    start_date = end_date - timedelta(days=90)

    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce", dayfirst=True)
    df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]

    filtered = df[df["Категория"].astype(str).str.lower() == category.lower()]
    expenses = filtered[filtered["Сумма платежа"] < 0]

    result = [
        {
            "date": row["Дата операции"].strftime("%d.%m.%Y"),
            "amount": round(row["Сумма платежа"], 2),
            "description": row.get("Описание", "")
        }
        for columns, row in expenses.iterrows()
    ]
    return result