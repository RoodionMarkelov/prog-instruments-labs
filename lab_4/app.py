import sys
import os
import logging

from PyQt5.QtWidgets import (
    QMainWindow,
    QToolTip,
    QPushButton,
    QApplication,
    QDesktopWidget,
    QFileDialog,
    QLabel,
    QMessageBox, QComboBox,
)
from PyQt5.QtGui import QFont

from cryptosystem import Cryptosystem
from serialization_deserialitation_and_text import read_json_file
from constants import PATH


class Window(QMainWindow):
    """
    Class for Window:
    @methods:
        __init__: конуструктор
        center: расположение окна в центре экрана
        get_file: получение пути для файла
        load_default_files: загружает файлы из json файла
        create_cryptosystem: создание криптосистемы
        UiComponents: создание виджета для выбора числа битов.
        find: получение числа битов из окна с выбором числа битов
        generate_keys_for_cryptosystem: создание ключей для криптосистемы
        encrypt_text: шифрование текста с помощью криптосистемы
        decrypt_text: дешифрование сообщения с помощью криптосистемы
        generate_keys_for_user: генерирует ключи в пользовательские файлы.
        encrypt_user_text: шифрует пользовательсктй текст.
        decrypt_user_text: дешифрует пользовательсктй текст.
        _quit: выход из приложения
    """

    def __init__(self):
        """
        Конструктор для окна. Содержит поля:
            text - текстовый файл для шифрования
            encrypted_file - зашифрованный текстовый файл
            decrypted_file - дешифрованный текстовый файл
            symmetric_key - путь для файла с симметричным путем
            public_key - путь для файла с публичным ключом
            private_key - путь для файла с приватным ключом
            cryptosystem - криптосистема
        """
        super().__init__()

        self.logger = self.create_logger()
        self.logger.info("Пользователь вошел в систему")

        self.cryptosystem = None

        QToolTip.setFont(QFont("SansSerif", 14))
        self.setToolTip("Это <b>QWidget</b> виджет")

        self.messagelabel = QLabel(self)
        self.messagelabel.setText("Привет пользователь!")
        self.messagelabel.adjustSize()
        self.messagelabel.move(100, 50)

        self.label_number_of_bits = QLabel(self)
        self.label_number_of_bits.setText("Количество битов:")
        self.label_number_of_bits.adjustSize()
        self.label_number_of_bits.move(290, 20)
        self.UiComponents()

        self.load_default_files()

        btn1 = QPushButton("Инициализация криптосистемы", self)
        btn1.setToolTip(
            "Нажмите на кнопку для создание файлов для ключей криптосистемы по умолчанию."
        )
        btn1.clicked.connect(self.create_cryptosystem)
        btn1.resize(btn1.sizeHint())
        btn1.move(50, 100)

        btn2 = QPushButton("Создание ключей", self)
        btn2.setToolTip(
            "Нажмите на кнопку для создание ключей криптосистемы."
        )
        btn2.clicked.connect(self.generate_keys_for_cryptosystem)
        (btn2
         .resize(btn2.sizeHint()))
        btn2.move(50, 150)

        btn3 = QPushButton("Зашифровать текст", self)
        btn3.setToolTip(
            "Нажмите на кнопку для шифрования текста."
        )
        btn3.clicked.connect(self.encrypt_text)
        btn3.resize(btn3.sizeHint())
        btn3.move(50, 200)

        btn4 = QPushButton("Дешифровать текст", self)
        btn4.setToolTip(
            "Нажмите на кнопку для дешифрования текста."
        )
        btn4.clicked.connect(self.decrypt_text)
        btn4.resize(btn4.sizeHint())
        btn4.move(50, 250)

        btn5 = QPushButton("Создание ключей в пользовательские файлы", self)
        btn5.setToolTip(
            "Нажмите на кнопку для создание ключей криптосистемы в пользовательские файлы."
        )
        btn5.clicked.connect(self.generate_keys_for_user)
        btn5.resize(btn5.sizeHint())
        btn5.move(200, 150)

        btn6 = QPushButton("Зашифровать пользовательский текст", self)
        btn6.setToolTip(
            "Нажмите на кнопку для шифрования пользовательского текста."
        )
        btn6.clicked.connect(self.encrypt_user_text)
        btn6.resize(btn6.sizeHint())
        btn6.move(200, 200)

        btn7 = QPushButton("Дешифровать пользовательский текст", self)
        btn7.setToolTip(
            "Нажмите на кнопку для дешифрования пользовательского текста."
        )
        btn7.clicked.connect(self.decrypt_user_text)
        btn7.resize(btn7.sizeHint())
        btn7.move(200, 250)

        qbtn = QPushButton("Выход", self)
        qbtn.setToolTip("Нажмите для кнопки для выхода.")
        qbtn.clicked.connect(self._quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(350, 400)
        self.resize(500, 450)
        self.center()
        self.setWindowTitle("app")

        self.show()

    def create_logger(self):
        logger = logging.getLogger("Event")
        logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger

    def load_default_files(self) -> None:
        """
        Метод загружает текстовые файлы из json файла.
        """
        try:
            absolute_path = os.path.abspath(os.getcwd())
            json_data = read_json_file(absolute_path + PATH)
            if json_data:
                text = json_data.get("text", "")
                encrypted_file = json_data.get("encrypted_file", "")
                decrypted_file = json_data.get("decrypted_file", "")
                symmetric_key = json_data.get("symmetric_key", "")
                public_key = json_data.get("public_key", "")
                private_key = json_data.get("private_key", "")
            if text and encrypted_file and decrypted_file and symmetric_key and private_key and public_key:
                self.text = absolute_path + text
                self.encrypted_file = absolute_path + encrypted_file
                self.decrypted_file = absolute_path + decrypted_file
                self.symmetric_key = absolute_path + symmetric_key
                self.public_key = absolute_path + public_key
                self.private_key = absolute_path + private_key
                self.messagelabel.adjustSize()
        except FileNotFoundError:
            print("Один из файлов не найден.")
            raise
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            raise

    def center(self) -> None:
        """
        Метод перемещает окно в центр экрана.
        """
        location = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        location.moveCenter(center)
        self.move(location.topLeft())
        return

    def get_file(self) -> str:
        """
        Метод возвращает путь до файла, выбранным пользователем.
        @return file_name: путь до выбранного файла.
        """
        logging.info("Пользователь выбрал файл")
        folderpath = QFileDialog.getExistingDirectory(self, "Выберете папку")
        file_name = QFileDialog.getOpenFileName(
            self, "Выберете файл", folderpath
        )
        return file_name[0]

    def create_cryptosystem(self) -> None:
        """
        Метод инициализирует криптосистему для класса.
        """
        try:
            self.logger.info("Пользователь инициализировал криптосистему")
            number_of_bits = int(self.find())
            self.cryptosystem = Cryptosystem(number_of_bits)
            self.messagelabel.setText("Система создана.")
            self.messagelabel.adjustSize()
            return
        except Exception as e:
            logging.warning("Произошла ошибка в создании криптосистемы")
            print(f"Произошла ошибка: {e}")
            raise

    def UiComponents(self) -> None:
        """
        Метод создает виджет для выбора числа битов для шифрования.
        """
        self.combo_box = QComboBox(self)

        self.combo_box.setGeometry(400, 10, 50, 30)

        list_of_number_of_bits = ["64", "128", "192"]

        self.combo_box.addItems(list_of_number_of_bits)

    def find(self) -> str:
        """
        Метод возвращает содержимое виджета для числа битов.
        @return content: содержимое виджета для числа битов. Тип str.
        """
        content = self.combo_box.currentText()
        return content

    def generate_keys_for_cryptosystem(self) -> None:
        """
        Метод генерирует ключи для криптосистемы.
        """
        if not self.cryptosystem:
            self.logger.info("Пользователь попытался сгенерировать ключи для несуществующей криптосистемы")
            self.messagelabel.setText("Для начала создайте криптосистему!")
            self.messagelabel.adjustSize()
            return
        self.logger.info("Пользователь сгенерировал ключи для криптосистемы")
        self.cryptosystem.generate_keys(self.symmetric_key, self.public_key, self.private_key)
        self.messagelabel.setText("Ключи созданы.")
        self.messagelabel.adjustSize()
        return

    def encrypt_text(self) -> None:
        """
        Метод шифрует текст с помомщью криптосистемы.
        """
        if not self.cryptosystem:
            self.logger.info("Пользователь попытался зашифровать текст без криптосистемы")
            self.messagelabel.setText("Для начала создайте криптосистему!")
            self.messagelabel.adjustSize()
            return
        self.logger.info("Пользователь зашифровал текст")
        self.cryptosystem.encrypt(self.text, self.symmetric_key, self.private_key, self.encrypted_file)
        self.messagelabel.setText("Текст зашифрован.")
        self.messagelabel.adjustSize()
        return

    def decrypt_text(self) -> None:
        """
        Метод дешифрует тест с помощью криптосистемы.
        """
        if not self.cryptosystem:
            self.logger.info("Пользователь попытался дешифровать текст без криптосистемы")
            self.messagelabel.setText("Для начала создайте криптосистему!")
            self.messagelabel.adjustSize()
            return
        self.logger.info("Пользователь дешифровал зашифрованный текст")
        self.cryptosystem.decrypt(self.encrypted_file, self.symmetric_key, self.private_key, self.decrypted_file)
        self.messagelabel.setText("Текст дешифрован.")
        return

    def generate_keys_for_user(self):
        """
        Метод генерирует ключи в пользовательские файлы.
        """
        if not self.cryptosystem:
            self.logger.info("Пользователь попытался сгенерировать ключи для несуществующей криптосистемы")
            self.messagelabel.setText("Для начала создайте криптосистему!")
            self.messagelabel.adjustSize()
            return
        user_symmetric_key = self.get_file()
        user_public_key = self.get_file()
        user_private_key = self.get_file()
        if user_symmetric_key and user_public_key and user_private_key:
            self.logger.info("Пользователь сгенерировал ключи в свои файлы")
            self.cryptosystem.generate_keys(user_symmetric_key, user_public_key, user_private_key)
            self.messagelabel.setText("Ключи созданы.")
            self.messagelabel.adjustSize()
        else:
            self.logger.info("Пользователь попытался сгенерировать ключи в свои файлы, однако выбраны не все файлы")
            self.messagelabel.setText("Ключи не созданы! Укажите все файлы.")
            self.messagelabel.adjustSize()
        return

    def encrypt_user_text(self):
        """
        Метод шифрует пользовательсктй текст.
        """
        if not self.cryptosystem:
            self.logger.info("Пользователь попытался зашифровать свой текст без криптосистемы")
            self.messagelabel.setText("Для начала создайте криптосистему!")
            self.messagelabel.adjustSize()
            return
        user_text = self.get_file()
        user_symmetric_key = self.get_file()
        user_private_key = self.get_file()
        user_save_text = self.get_file()
        if user_text and user_symmetric_key and user_private_key and user_save_text:
            self.logger.info("Пользователь зашифровал свой текст")
            self.cryptosystem.encrypt(user_text, user_symmetric_key, user_private_key, user_save_text)
            self.messagelabel.setText("Текст зашифрован.")
            self.messagelabel.adjustSize()
        else:
            self.logger.info("Пользователь попытался зашифровать свой текст, однако выбраны не все файлы")
            self.messagelabel.setText("Выберите все файлы.")
            self.messagelabel.adjustSize()
        return

    def decrypt_user_text(self) -> None:
        """
        Метод дешифрует пользовательсктй текст.
        """
        if not self.cryptosystem:
            self.logger.info("Пользователь попытался дешифровать текст без криптосистемы")
            self.messagelabel.setText("Для начала создайте криптосистему!")
            self.messagelabel.adjustSize()
            return
        user_encrypted_text = self.get_file()
        user_symmetric_key = self.get_file()
        user_private_key = self.get_file()
        user_save_text = self.get_file()
        if user_encrypted_text and user_symmetric_key and user_private_key and user_save_text:
            self.logger.info("Пользователь дешифровал свой текст")
            self.cryptosystem.decrypt(user_encrypted_text, user_symmetric_key, user_private_key, user_save_text)
            self.messagelabel.setText("Текст разшифрован.")
            self.messagelabel.adjustSize()
        else:
            self.logger.info("Пользователь попытался дешифровать свой текст, однако не все файлы были выбраны")
            self.messagelabel.setText("Выберите все файлы.")
            self.messagelabel.adjustSize()
        return

    def _quit(self) -> None:
        """Получение MessageBox для выхода"""
        reply = QMessageBox.question(
            self,
            "Сообщение",
            "Вы уверены, что хотите выйти?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.logger.info("Пользователь вышел из приложения")
            QApplication.instance().quit()
        else:
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
