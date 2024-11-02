import re
import pandas as pd
import json
import hashlib
from typing import List

from paths import PATH_TO_JSON_FILE, PATH_TO_CSV_FILE

"""
В этом модуле обитают функции, необходимые для автоматизированной проверки результатов ваших трудов.
"""


def calculate_checksum(row_numbers: List[int]) -> str:
    """
    Вычисляет md5 хеш от списка целочисленных значений.

    ВНИМАНИЕ, ВАЖНО! Чтобы сумма получилась корректной, считать, что первая строка с данными csv-файла имеет номер 0
    Другими словами: В исходном csv 1я строка - заголовки столбцов, 2я и остальные - данные.
    Соответственно, считаем что у 2 строки файла номер 0, у 3й - номер 1 и так далее.

    Надеюсь, я расписал это максимально подробно.
    Хотя что-то мне подсказывает, что обязательно найдется человек, у которого с этим возникнут проблемы.
    Которому я отвечу, что все написано в докстринге ¯\_(ツ)_/¯

    :param row_numbers: список целочисленных номеров строк csv-файла, на которых были найдены ошибки валидации
    :return: md5 хеш для проверки через github action
    """
    row_numbers.sort()
    return hashlib.md5(json.dumps(row_numbers).encode('utf-8')).hexdigest()


def serialize_result(variant: int, checksum: str) -> None:
    """
    Метод для сериализации результатов лабораторной пишите сами.
    Вам нужно заполнить данными - номером варианта и контрольной суммой - файл, лежащий в папке с лабораторной.
    Файл называется, очевидно, result.json.

    ВНИМАНИЕ, ВАЖНО! На json натравлен github action, который проверяет корректность выполнения лабораторной.
    Так что не перемещайте, не переименовывайте и не изменяйте его структуру, если планируете успешно сдать лабу.

    :param variant: номер вашего варианта
    :param checksum: контрольная сумма, вычисленная через calculate_checksum()
    """
    try:
        with open(PATH_TO_JSON_FILE, "r") as f:
            result_data = json.load(f)

        result_data["variant"] = variant
        result_data["checksum"] = checksum

        with open(PATH_TO_JSON_FILE, "w") as f:
            f.write(json.dumps(result_data))

    except Exception as e:
        print(f"Произошла ошибка при обновлении файла: {e}")


def process() -> None:
    parameters = {
        'telephone': r"^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$",
        'height': r"^[1-2]\.\d{2}$",
        'inn': r"^\d{12}$",
        'identifier': r"^\d{2}-\d{2}\/\d{2}$",
        'occupation': r"^[a-zA-Zа-яА-ЯёЁ\s-]+",
        'latitude': r"^[+-]?(90\.0|0\.0|[0-8]?\d\.\d{6})$",
        'blood_type': r"^(AB?|B|O)(\+|\-)$",
        'issn': r"^\d{4}-\d{4}$",
        'uuid': r"^[a-z0-9]{8}-([a-f0-9]{4}-){3}[a-z0-9]{12}$",
        'date': r"(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])"
    }

    try:
        data = pd.read_csv(PATH_TO_CSV_FILE, encoding='utf-16', sep=';', header=0)
    except Exception as e:
        print(f"Произошла ошибка при обновлении файла: {e}")

    data.columns = ["telephone", "height", "inn", "identifier", "occupation", "latitude", "blood_type", "issn",
                    "uuid", "date"]

    errors = []

    for index, row in data.iterrows():
        row_has_error = False
        for col, pattern in parameters.items():
            if not re.match(pattern, str(row[col])):
                row_has_error = True
                break
        if row_has_error:
            errors.append(index)

    print(errors)


if __name__ == "__main__":
    process()
