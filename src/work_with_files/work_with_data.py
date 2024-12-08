# Импортируем библиотеку json для взаимодействия с JSON-объектами
import json
# Строим пути к файлам с учетом особенностей ОС.
import os
# Импортируем библиотеку pandas для сохранения информации в Excel
import pandas as pd
# Импортируем класс вакансий из файла class_vacancy.py


class JSONManager:
    """Класс для работы с файлами формата JSON, хранящими данные о вакансиях."""

    def __init__(self, file_name='file_with_data') -> None:
        """Инициирует конструктор класса."""

        self._file_name = file_name

        root_path_src_dir = os.path.split(os.path.abspath(__file__))
        root_path_main_dir = os.path.split(os.path.split(root_path_src_dir[0])[0])[0]
        file_with_data = str(os.path.join(root_path_main_dir, 'data', self._file_name)) + '.json'
        if os.path.exists(file_with_data):
            if not os.path.abspath(file_with_data).endswith('.json'):
                raise ValueError('Файл должен быть формата JSON.')
        else:
            pass

    @property
    def file_name(self):
        """Геттер имени файла. Предоставляет доступ к атрибуту для изменения его значения."""
        return self._file_name

    @file_name.setter
    def file_name(self, user_file_name: str):
        """Сеттер имени файла. Изменяет значение атрибута."""
        if user_file_name == '':
            pass
        else:
            self._file_name = user_file_name

    def write_to_file(self, for_write_vacancies_list: list):
        """Добавляет список вакансий в JSON файл."""

        root_path_src_dir = os.path.split(os.path.abspath(__file__))
        root_path_main_dir = os.path.split(os.path.split(root_path_src_dir[0])[0])[0]
        file_with_data = str(os.path.join(root_path_main_dir, 'data', self._file_name)) + '.json'


        try:
            with open(file_with_data, "r", encoding="utf-8") as file_vac:
                json_content = json.load(file_vac)
                json_content.extend(for_write_vacancies_list)
                with open(file_with_data, "w", encoding="utf-8") as file_vac_for_update:
                    json.dump(json_content, file_vac_for_update, indent=2, ensure_ascii=False)
        except FileNotFoundError:
            with open(file_with_data, "w", encoding="utf-8") as file_vac_new:
                json.dump(for_write_vacancies_list, file_vac_new, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            with open(file_with_data, "w", encoding="utf-8") as file_vac_for_update:
                json.dump(for_write_vacancies_list, file_vac_for_update, indent=2, ensure_ascii=False)

    def load_from_file(self):
        """Получает данные из файла и преобразовывает их в словарь вакансий."""

        root_path_src_dir = os.path.split(os.path.abspath(__file__))
        root_path_main_dir = os.path.split(os.path.split(root_path_src_dir[0])[0])[0]
        file_with_data = str(os.path.join(root_path_main_dir, 'data', self._file_name)) + '.json'

        try:
            with open(file_with_data, "r", encoding="utf-8") as f:
                json_string = f.read()

            raw_vacancies = json.loads(json_string)
            return raw_vacancies
        except FileNotFoundError:
            list_for_write = []
            with open(file_with_data, "w", encoding="utf-8") as file_new:
                json.dump(list_for_write, file_new, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            list_for_write = []
            with open(file_with_data, "w", encoding="utf-8") as file_for_adjustment:
                json.dump(list_for_write, file_for_adjustment, indent=2, ensure_ascii=False)

    def delete_from_file(self):
        """Удаляет информацию о вакансиях."""

        root_path_src_dir = os.path.split(os.path.abspath(__file__))
        root_path_main_dir = os.path.split(os.path.split(root_path_src_dir[0])[0])[0]
        file_with_data = str(os.path.join(root_path_main_dir, 'data', self._file_name)) + '.json'

        with open(file_with_data, "w") as f:
            f.write('')

    def __str__(self):
        """Человеко читаемое отображение наименования файла."""

        return f'{self._file_name}'


class INIManager:
    """Класс для работы с файлами формата INI, хранящими данные для установки соединения с базами данных."""

    def __init__(self, file_name='database') -> None:
        """Инициирует конструктор класса."""

        self._file_name = file_name

        root_path_src_dir = os.path.split(os.path.abspath(__file__))
        root_path_main_dir = os.path.split(os.path.split(root_path_src_dir[0])[0])[0]
        file_with_data = str(os.path.join(root_path_main_dir, self._file_name)) + '.ini'
        if os.path.exists(file_with_data):
            if not os.path.abspath(file_with_data).endswith('.ini'):
                raise ValueError('Файл должен быть формата INI.')
        else:
            pass

    @property
    def file_name(self):
        """Геттер имени файла. Предоставляет доступ к атрибуту для изменения его значения."""
        return self._file_name

    @file_name.setter
    def file_name(self, user_file_name: str):
        """Сеттер имени файла. Изменяет значение атрибута."""
        if user_file_name == '':
            pass
        else:
            self._file_name = user_file_name

    def write_to_file(self, host: str, user: str, password: str, port: str):
        """Добавляет параметры для подключения в INI файл."""

        root_path_src_dir = os.path.split(os.path.abspath(__file__))
        root_path_main_dir = os.path.split(os.path.split(root_path_src_dir[0])[0])[0]
        file_with_data = str(os.path.join(root_path_main_dir, self._file_name)) + '.ini'

        str_for_write = f'[postgresql]\nhost={host}\nuser={user}\npassword={password}\nport={port}'

        with open(file_with_data, "w", encoding="utf-8") as file_ini:
            file_ini.write(str_for_write)
