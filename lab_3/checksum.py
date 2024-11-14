import re
import os
import pandas as pd
import json
import hashlib

from typing import List

from constants import PATH_TO_JSON_FILE, PATH_TO_CSV_FILE, VARIANT


def calculate_checksum(row_numbers: List[int]) -> str:
    """
    Вычисляет md5 хеш от списка целочисленных значений.

    :param row_numbers: список целочисленных номеров строк csv-файла, на которых были найдены ошибки валидации
    :return: md5 хеш для проверки через github action
    """
    row_numbers.sort()
    return hashlib.md5(json.dumps(row_numbers).encode('utf-8')).hexdigest()


def serialize_result(variant: int, checksum: str) -> None:
    """
    Метод для сериализации результатов лабораторной.
    :param variant: номер вашего варианта
    :param checksum: контрольная сумма, вычисленная через calculate_checksum()
    """
    try:
        absolute_path_to_json = os.path.abspath(os.getcwd()) + PATH_TO_JSON_FILE
        with open(absolute_path_to_json, "r") as f:
            result_data = json.load(f)

        result_data["variant"] = variant
        result_data["checksum"] = checksum

        with open(absolute_path_to_json, "w") as f:
            f.write(json.dumps(result_data))

    except Exception as e:
        print(f"Произошла ошибка в функции serialize_result: {e}")


def read_csv(file_name: str) -> pd.DataFrame:
    """
    Функция считывает данные из CSV-файла по ссылке file_name и возвращяет данные в виде pd.DataFrame
    :param file_name: ссылка на CSV-файл
    :return pd.DataFrame: данные в виде таблицы Pandas
    """
    try:
        data = pd.read_csv(file_name, encoding='utf-16', sep=';', header=0)
        return data
    except Exception as e:
        print(f"Произошла ошибка в функции process: {e}")


def process(csv_file: str) -> List[int]:
    """
    Функция обрабатывает значения из csv-файла, а именно ищет несоответствия шаблону,
    а затем записывает номер строки, в которой присутствует несоответствие.
    :param csv_file: ссылка на csv-файл
    :return errors_index: список индексов строк с ошибками
    """
    parameters = {
        'telephone': r"^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$",
        'height': r"^[1-2]\.\d{2}$",
        'inn': r"^\d{12}$",
        'identifier': r"^\d{2}-\d{2}\/\d{2}$",
        'occupation': r"^[a-zA-Zа-яА-ЯёЁ\s-]+",
        'latitude': r"^[+-]?(90\.0|0\.0|[0-8]?\d\.\d{,6})$",
        'blood_type': r"^(AB?|B|O)(\+|\u2212)$",
        'issn': r"^\d{4}-\d{4}$",
        'uuid': r"^[a-z0-9]{8}-([a-f0-9]{4}-){3}[a-z0-9]{12}$",
        'date': r"(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])"
    }

    data = read_csv(csv_file)

    data.columns = ["telephone", "height", "inn", "identifier", "occupation", "latitude", "blood_type", "issn",
                    "uuid", "date"]

    errors_index = []

    for index, row in data.iterrows():
        row_has_error = False
        for column, pattern in parameters.items():
            if not re.match(pattern, str(row[column])):
                row_has_error = True
                break
        if row_has_error:
            errors_index.append(index)

    return errors_index


def main() -> None:
    """
    Эта функция выполняет все действия согласно заданию лабораторой работы,
    а именно получает список индексов строк с ошибками, подсчитывает контрольную сумму
    и сериализует результаты в JSON-файл.
    Ничего не возвращает.
    :return:
    """
    absolute_path_to_csv = os.path.abspath(os.getcwd()) + PATH_TO_CSV_FILE
    rows_index = process(absolute_path_to_csv)
    checksum = calculate_checksum(rows_index)
    serialize_result(VARIANT, checksum=checksum)


if __name__ == "__main__":
    main()
