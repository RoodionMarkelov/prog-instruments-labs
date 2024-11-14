import json

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key


def deserialize_private(path_to_private_key: str) -> rsa.RSAPrivateKey:
    """
    Функция десиарилизует приватный ключ из указанного файла(path_to_private_key).
    @param path_to_private_key: путь до файла с сохранненым приватным ключом. Тип str.
    @return d_private_key: приватный ключ. Тип rsa.RSAPrivateKey.
    """
    try:
        with open(path_to_private_key, 'rb') as pem_in:
            private_bytes = pem_in.read()
        d_private_key = load_pem_private_key(private_bytes, password=None, )
        return d_private_key
    except FileNotFoundError:
        print("Файл не найден.")
        raise
    except Exception as e:
        print(f"Произошла ошибка deserialize_private: {e}")
        raise


def deserialize_public(path_to_public_key: str) -> rsa.RSAPublicKey:
    """
    Функция десиарилизует публичный ключ из указанного файла(path_to_public_key).
    @param path_to_public_key: путь до файла с сохранненым публичным ключом. Тип str.
    @return d_public_key: публичный ключ. Тип rsa.RSAPublicKey.
    """
    try:
        with open(path_to_public_key, 'rb') as pem_in:
            public_bytes = pem_in.read()
        d_public_key = load_pem_public_key(public_bytes)
        return d_public_key
    except FileNotFoundError:
        print("Файл не найден.")
        raise
    except Exception as e:
        print(f"Произошла ошибка deserialize_public: {e}")
        raise


def serialize_private(path_to_private_key: str, private_key: rsa.RSAPrivateKey) -> None:
    """
    Функция сериализует приватный ключ(private_key) по заданному пути(path_to_private_key).
    @param path_to_private_key: путь до файла для сохранения приватного ключа. Тип str.
    @param private_key: приватный ключ, который нужно сериализовать. Тип rsa.RSAPrivateKey.
    """
    try:
        with open(path_to_private_key, 'wb') as private_out:
            private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                        encryption_algorithm=serialization.NoEncryption()))
    except FileNotFoundError:
        print("Файл не найден.")
        raise
    except Exception as e:
        print(f"Произошла ошибка serialize_private: {e}")
        raise


def serialize_public(path_to_public_key: str, public_key: rsa.RSAPublicKey) -> None:
    """
    Функция сериализует публичный ключ(public_key) по заданному пути(path_to_public_key).
    @param path_to_public_key: путь до файла для сохранения публичного ключа. Тип str.
    @param public_key: публичный ключ, который нужно сериализовать. Тип rsa.RSAPublicKey.
    """
    try:
        with open(path_to_public_key, 'wb') as public_out:
            public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                     format=serialization.PublicFormat.SubjectPublicKeyInfo))
    except FileNotFoundError:
        print("Файл не найден.")
        raise
    except Exception as e:
        print(f"Произошла ошибка serialize_public: {e}")
        raise


def serialize_asymmetric_keys(path_to_private_key: str, path_to_public_key: str, private_key: rsa.RSAPrivateKey,
                              public_key: rsa.RSAPublicKey) -> None:
    """
    Функция сериализует приватный ключ(private_key) и публичный ключ(public_key) по заданным путям
    (path_to_private_key) и (path_to_public_key).
    @param path_to_private_key: путь до файла для сохранения приватного ключа. Тип str.
    @param path_to_public_key: приватный ключ, который нужно сериализовать. Тип str.
    @param private_key: приватный ключ, который нужно сериализовать. Тип rsa.RSAPrivateKey.
    @param public_key: публичный ключ, который нужно сериализовать. Тип rsa.RSAPublicKey.
    """
    serialize_private(path_to_private_key, private_key)

    serialize_public(path_to_public_key, public_key)


def serialize_symmetric_key(path_to_symmetric_key: str, symmetric_key: bytes) -> None:
    """
    Функция сериализует симметричный ключ(symmetric_key) в файл path_to_symmetric_key.
    @param path_to_symmetric_key: путь до файла для симмитричного ключа. Тип str.
    @param symmetric_key: симметричный ключ. Тип bytes.
    """
    try:
        with open(path_to_symmetric_key, 'wb') as file:
            file.write(symmetric_key)
    except FileNotFoundError:
        print("Файл не найден.")
        raise
    except Exception as e:
        print(f"Произошла ошибка serialize_key: {e}")
        raise


def deserialize_symmetric_key(path_to_symmetric_key: str) -> bytes:
    """
    Функция десериализует симметричный ключ из файла path_to_symmetric_key.
    @param path_to_symmetric_key: путь до файла с симметричным ключом. Тип str.
    @return symmetric_key: симметричный ключ. Тип bytes.
    """
    try:
        with open(path_to_symmetric_key, mode='rb') as key_file:
            symmetric_key = key_file.read()
        return symmetric_key
    except FileNotFoundError:
        print("Файл не найден.")
        raise
    except Exception as e:
        print(f"Произошла ошибка deserialize_key: {e}")
        raise


def save_text(file_name: str, text: bytes):
    """
    Функция записывает текст (text) в файл с названием file_name.
    @param file_name: название файла для записи текста. Тип str.
    @param text: текст для сохранения  в байтах. Тип bytes.
    """
    try:
        with open(file_name, 'wb') as file:
            file.write(text)
    except FileNotFoundError:
        print("Файл не найден.")
        raise
    except Exception as e:
        print(f"Произошла ошибка save_text: {e}")
        raise


def save_text_str(file_name: str, text: str):
    """
    Функция записывает текст (text) в файл с названием file_name.
    @param file_name: название файла для записи текста. Тип str.
    @param text: текст для сохранения  в.виде строки Тип str.
    """
    try:
        with open(file_name, 'w') as file:
            file.write(text)
    except FileNotFoundError:
        print("Файл не найден.")
        raise
    except Exception as e:
        print(f"Произошла ошибка save_text_str: {e}")
        raise


def read_text(file_name: str):
    """
    Функция считывает текст из файла с названием file_name. Затем возвращает считанный текст.
    @param file_name: название файла для считывания.Тип str.
    @return content: содержимое файла. Тип str.
    """
    try:
        with open(file_name, mode='rb') as key_file:
            content = key_file.read()
        return content
    except FileNotFoundError:
        print("Файл не найден.")
        raise
    except Exception as e:
        print(f"Произошла ошибка read_text: {e}")
        raise


def read_json_file(file_path: str) -> dict:
    """
    Функция считывает данные из JSON файла.
    :param file_path: указывает на расположение JSON файла.
    :return dict:
    """
    try:
        with open(file_path, "r", encoding="UTF-8") as file:
            json_data = json.load(file)
            return json_data
    except FileNotFoundError:
        print("Файл не найден.")
        raise
    except json.JSONDecodeError:
        print("Ошибка при считывании JSON-данных.")
        raise
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        raise
