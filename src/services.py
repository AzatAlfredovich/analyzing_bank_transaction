import re

#Функция "Простой поиск"
def simple_search(transactions, search_string):
    """ Функция возвращает список всех транзакций,
    содержащих заданную строку в описании или категории,
    используя регулярные выражения для нечувствительного к регистру поиска"""

    pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    # Фильтрация транзакций по регулярному выражению
    result = [
        transaction for transaction in transactions
        if (
                pattern.search(transaction.get('Описание', '')) or
                pattern.search(transaction.get('Категория', ''))
        )
    ]

    return result
