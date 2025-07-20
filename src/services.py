import logging
import re


# Функция "Простой поиск"
def simple_search(transactions: list[dict], search_string: str) -> list[dict]:
    """Функция возвращает список всех транзакций,
    содержащих заданную строку в описании или категории,
    используя регулярные выражения для нечувствительного к регистру поиска"""

    pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    # Фильтрация транзакций по регулярному выражению
    result = [
        transaction
        for transaction in transactions
        if isinstance(transaction.get("Описание", ""), str)
        and pattern.search(transaction.get("Описание", ""))
        or isinstance(transaction.get("Категория", ""), str)
        and pattern.search(transaction.get("Категория", ""))
    ]
    logging.info(f"Возвращаем список транзакций, в категории или описании которых есть -  {search_string}")
    return result
