import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.decrepit.ciphers import algorithms

class SymmetricKey:
    """
    class for SymmetricKey
    @methods:
        serialize_key: Сериализует симметричный ключ в файл.
        deserialize_key: Десериализует симметричный ключ из файла.
        generate_key: Генерирует симметричный ключ.
        encrypt_symmetric: Шифрует текст симметричным ключом.
        decrypt_symmetric: Дешифрует текст симметричным ключом ключом.
    """

    def generate_key(self, number_of_bites: int) -> bytes:
        """
        Метод генерирует симметричный ключ с заданным количеством битов number_of_bites.
        @param number_of_bites: количество битов для симмитричного ключаю Тип int.
        @return symmetric_key: симметричный ключ. Тип bytes.
        """
        try:
            symmetric_key = bytes(os.urandom(int(number_of_bites / 8)))
            return symmetric_key
        except Exception as e:
            print(f"Произошла ошибка в функции generate_key: {e}")
        raise

    def encrypt_symmetric(self, text: bytes, symmetric_key: bytes, number_of_bites: int) -> bytes:
        """
        Метод шифрует текст(text) с помощью симметричного ключа(symmetric_key) с заданным
        количеством битов(number_of_bites). Возвращает зашифрованный текст.
        @param text: текст для шифрования. Тип bytes.
        @param symmetric_key: симмитричный ключ для шифрования. Тип bytes.
        @param number_of_bites: количество битов для шифрования. тип int.
        @return encrypted_text: зашифрованный текст.
        """
        try:
            padder = padding.PKCS7(number_of_bites).padder()
            padded_text = padder.update(text) + padder.finalize()
            iv = os.urandom(8)
            cipher = Cipher(algorithms.TripleDES(symmetric_key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            encrypted_text = encryptor.update(padded_text) + encryptor.finalize()
            encrypted_text = iv + encrypted_text
            return encrypted_text
        except Exception as e:
            print(f"Произошла ошибка в функции encrypt_symmetric: {e}")
            raise

    def decrypt_symmetric(self, encrypted_text: bytes, symmetric_key: bytes, number_of_bites: int) -> str:
        """
        Метод дешифрует зашифрованный текст(encrypted_text) с помощью симметричного ключа(symmetric_key)
        с заданным количеством битов(number_of_bites).
        @param encrypted_text: зашифрованный текст. Тип bytes.
        @param symmetric_key: симмитричный ключ для дешифрования. Тип bytes.
        @param number_of_bites: количество битов для дешифрования. Тип int.
        @return unpadded_decrypted_text.decode('UTF-8'): расшифрованный текст. Тип str.
        """
        try:
            iv = encrypted_text[: 8]
            encrypted_text = encrypted_text[8:]
            cipher = Cipher(algorithms.TripleDES(symmetric_key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            decrypted_text = decryptor.update(encrypted_text) + decryptor.finalize()
            unpadder = padding.PKCS7(number_of_bites).unpadder()
            unpadded_decrypted_text = unpadder.update(decrypted_text) + unpadder.finalize()
            return unpadded_decrypted_text.decode('UTF-8')
        except Exception as e:
            print(f"Произошла ошибка в функции decrypt_symmetric: {e}")
            raise
