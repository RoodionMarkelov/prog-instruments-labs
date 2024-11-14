from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

from serialization_deserialitation_and_text import deserialize_private


class AsymmetricKey:
    """
    class for AsymmetricKey
    @methods:
        serialize_private: Сериализует приватный ключ в файл.
        serialize_public: Сериализует публичный ключ в файл.
        serialize_keys: Сериализует приватный и публичный ключи в файлы.
        deserialize_private: Десериализует приватный ключ из файла.
        deserialize_public: Десериализует публичный ключ из файла.
        generate_keys: Генерирует приватный и публичный ключи.
        encrypt_text: Шифрует текст публичным ключом.
        decrypt_text: Дешифрует текст приватныи ключом.
    """

    def generate_keys(self) -> tuple:
        """
        Метод генерирует два ключа: приватный(private_key) и публичный(public_key), после чего возвращает их в виде списка.
        @return private_key, public_key:
        """
        try:
            keys = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            private_key = keys
            public_key = keys.public_key()
            return private_key, public_key
        except Exception as e:
            print(f"Произошла ошибка generate_keys: {e}")
            raise

    def encrypt_text(self, text: bytes, public_key: rsa.RSAPublicKey) -> bytes:
        """
        Метод шифрует текст(text) с помощью публичного ключа, после чего возвращает
        зашифрованый текст(encrypted_text).
        @param text: текст, который нужно зашифровать. Тип bytes
        @param public_key: публичный ключ, с помощью которого шифруется текст. Тип rsa.RSAPublicKey
        @return encrypted_text: зашифрованный текст. Тип bytes
        """
        try:
            encrypted_text = public_key.encrypt(text,
                                                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                             algorithm=hashes.SHA256(),
                                                             label=None))
            return encrypted_text
        except Exception as e:
            print(f"Произошла ошибка encrypt_text: {e}")
            raise

    def decrypt_text(self, path_to_private_key: str, encrypted_text: bytes) -> bytes:
        """
        Метод дешифрует текст(encrypted_text) с помощью приватного ключа, который
        десиарилизуется из файла(path_to_private_key), после чего возвращает
        разшифрованный текст(decrypted_text).
        @param path_to_private_key: файл с приватным ключом str
        @param encrypted_text: зашифрованный текст. Тип bytes
        @return decrypted_text: разсшифрованный текстю Тип bytes
        """
        try:
            private_key = deserialize_private(path_to_private_key)
            decrypted_text = private_key.decrypt(encrypted_text,
                                                 padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                              algorithm=hashes.SHA256(), label=None))
            return decrypted_text
        except Exception as e:
            print(f"Произошла ошибка decrypt_text: {e}")
            raise
