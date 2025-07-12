from unittest.mock import patch

from utils import reading_xlsx


@patch("pandas.read_excel")
def test_reading_xlsx(mock_get):
    mock_get.return_value.to_dict.return_value = [
        {
            "Дата операции": "2021-12-10",
            "Сумма операции": -1000.0,
            "Категория": "Супермаркеты",
            "Описание": "Пятёрочка"
        }
    ]
    assert reading_xlsx("") == [{
        "Дата операции": "2021-12-10",
        "Сумма операции": -1000.0,
        "Категория": "Супермаркеты",
        "Описание": "Пятёрочка"
    }]