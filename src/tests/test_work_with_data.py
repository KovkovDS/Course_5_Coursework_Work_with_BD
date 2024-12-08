# Импортируем фреймворк для тестирования кода
import pytest

# Строим пути к файлам с учетом особенностей ОС.
import os

# Модуль для работы с Excel файлами
import pandas as pd

# Импортируем классы объектов из файла classes_for_services.py
from src.work_with_files.work_with_data import INIManager, JSONManager

# Импортируем классы объектов из файла classes_for_services.py
from config import config


@pytest.fixture()
def example_class_json():
    example_json = JSONManager
    return example_json

@pytest.fixture()
def example_class_ini():
    example_ini = INIManager()
    return example_ini

@pytest.fixture()
def example_file_name_json():
    return 'vacancy'


@pytest.fixture()
def example_file_name_json_1():
    return 0


@pytest.fixture()
def example_file_name_json_2():
    return ''

@pytest.fixture()
def example_file_name_ini():
    return 'database'

@pytest.fixture()
def example_test_file_name_json():
    return 'test_file_with_data'


@pytest.fixture()
def example_file_name_json_def():
    return "file_with_data"

@pytest.fixture()
def example_write_params():
    example_tuple = 'host', 'user', 'password', 'port'
    return example_tuple

@pytest.fixture()
def example_params_dict():
    example_dict = {'host': 'host', 'user': 'user', 'password': 'password', 'port': 'port'}
    return example_dict

# @pytest.fixture()
# def example_config():
#     example_config_dict = config()
#     return example_config_dict

@pytest.fixture()
def example_write_file_name_json():
    return f'C:\SOFTSKILLS\Python_projects\sky_pro\Course_4_Coursework\data\\vacancy.json'


@pytest.fixture()
def example_write_file_name_json_1():
    return f'C:\SOFTSKILLS\Python_projects\sky_pro\Course_4_Coursework\data\\0.json'


@pytest.fixture()
def example_write_file_name_json_2():
    return f'C:\SOFTSKILLS\Python_projects\sky_pro\Course_4_Coursework\data\\test_file_with_data.json'


@pytest.fixture()
def example_write_file_name_ini():
    return f'C:\SOFTSKILLS\Python_projects\sky_pro\Course_4_Coursework\\database.ini'


@pytest.fixture()
def example_write_file_name_ini_1():
    return f'C:\SOFTSKILLS\Python_projects\sky_pro\Course_4_Coursework\data\\0.ini'


@pytest.fixture()
def example_write_file_name_ini_2():
    return f'C:\SOFTSKILLS\Python_projects\sky_pro\Course_4_Coursework\data\\.ini'



@pytest.fixture()
def example_list_dicts():
    return [{'name': 'Учитель информатики',
             'link': 'https://zheleznodorozhniy.superjob.ru/vakansii/uchitel-informatiki-36344427.html',
             'city': 'Железнодорожный', 'salary_from': 50000, 'salary_to': 0, 'currency': 'rub',
             'experience': 'Без опыта',
             'requirements': 'С 1 сентября 2024 года. \nОбязанности:\n• Осуществляет обучение и воспитание обучающихся '
                             'с учетом специфики преподаваемого предмета, проводит уроки и другие занятия в '
                             'соответствии с расписанием.\n• В своей работе по предмету использует разнообразные '
                             'приемы, методы и средства обучения.\n• Реализует образовательные программы.\n• Подготовка'
                             ' обучающихся к сдаче ГИА и участию в олимпиадах и конкурсах.\n• Ведение дополнительных '
                             'занятий и факультативов. \n• Программирование: Перволого/Логомиры, Scratch, Кумир, '
                             'Паскаль/Дельфи, C/C++, Python\nСАПР: Компас, AutoCAD CorelDRAW и др.\nВеб-дизайн и '
                             'разработка: JavaScript, Adobe Photoshop, Flash.\nАдминистрирование: Windows, '
                             'Linux\nУсловия:\n• Выплата компенсации за аренду жилья (при отсутствии недвижимости в '
                             'Московской области)\n• Помощь в устройстве детей в дошкольные или школьные учреждения '
                             'города.', 'duties': 'None'},
            {'name': 'Педагог на направление Программирование на языке Java / С# / Python',
             'link': 'https://novokuznetsk.superjob.ru/vakansii/pedagog-na-napravlenie-programmirovanie-na-yazyke'
                     '-java-43502923.html', 'city': 'Новокузнецк', 'salary_from': 25000, 'salary_to': 50000,
             'currency': 'rub', 'experience': 'Без опыта',
             'requirements': 'Обязанности:\nпедагоги-наставники на направления: Python, Java, С#:\n• обучение детей и '
                             'молодежи по программам дополнительного образования;\n• помощь и поддержка обучающихся в '
                             'освоении языка программирования;\n• разработка совместных проектов с учащимися;\n• '
                             'оформление готовых продуктов;\n• участие в массовых мероприятиях с учащимися.\n '
                             'Требования:\n• образование высшее или средне-специальное (рассматриваются студенты '
                             'начиная с 4-го курса);\n• опыт работы приветствуется (рассматриваются начинающие '
                             'специалисты);\n• умение доводить дело до логического завершения.\nУсловия:\n• соблюдение'
                             ' правил внутреннего распорядка;\n• исполнительская дисциплина;\n• справка об отсутствии '
                             'судимости;\n• наличие санитарной книжки (ежегодный медосмотр, санминимум для работников '
                             'сферы образования).\nДля вас:\n• полный социальный пакет;\n• стабильная з/п два раза в '
                             'месяц;\n• дружный коллектив;\n• ежегодный отпуск 42 дня;\n• оформление по ТК РФ.',
             'duties': 'None'},
            {'name': 'Учитель по программированию',
             'link': 'https://mo.superjob.ru/vakansii/uchitel-po-programmirovaniyu-45698486.html', 'city': 'Ржавки',
             'salary_from': 0, 'salary_to': 60000, 'currency': 'rub', 'experience': 'Без опыта',
             'requirements': 'Обязанности:\n• \nОбучение детей (4-14 лет) в группах программированию \n• '
                             '\nФормирование у учеников логического системного мышления и развитие технических '
                             'творческих способностей \n\n• Обучение детей основам проектной работы в IT\n• '
                             'Поддержание интереса и мотивации учеников \nТребования:\n• \nОпыт работы с детьми '
                             '(аниматор, репетитор, воспитатель, вожатый, учитель, опытный родитель или старший '
                             'брат/сестра\n• Уверенное владение компьютером. В идеале, знание основ алгоритмического '
                             'языка и программирования. (Предпочтительно: Scratch JR, Scratch, Snap, Stencyl, Tynker, '
                             'Blockly, Перволого, Пиктомир)\n• Умение объяснять сложное простыми (иногда детскими) '
                             'словами \n• Любовь к детям и умение направить их энергию в нужное русло \n\n• Знание '
                             'текстовых языков программирования Python, Java и прочее - желательно \n\nУсловия:\n• '
                             '\nУдобный график (очень многое можно скорректировать совместно с администратором) \n• '
                             'Возможность обучать мотивированных детей, которые стремятся узнать все о современных '
                             'технологиях и не только \n• Увлеченная команда преподавателей \n\n• Интересные и '
                             'амбициозные задачи\n• Профессия квалифицированного детского IT тренера - одна из самых '
                             'востребованных на рынке труда', 'duties': 'None'}]


def test_file_name_json(example_class_json, example_file_name_json, example_file_name_json_1, example_file_name_json_2):
    example_class_json._file_name = example_file_name_json
    assert example_class_json._file_name == 'vacancy'
    example_class_json._file_name = example_file_name_json_1
    assert example_class_json._file_name == 0
    example_class_json._file_name = example_file_name_json_2
    assert example_class_json._file_name == ''


def test_file_name_ini(example_class_ini, example_file_name_json, example_file_name_json_1, example_file_name_json_2,
                       example_file_name_ini):
    example_class_ini._file_name = example_file_name_json
    assert example_class_ini._file_name == 'vacancy'
    example_class_ini._file_name = example_file_name_json_1
    assert example_class_ini._file_name == 0
    example_class_ini._file_name = example_file_name_json_2
    assert example_class_ini._file_name == ''
    example_class_ini._file_name = example_file_name_ini
    assert example_class_ini._file_name == example_file_name_ini

def test_write_file_json(example_file_name_json_def, example_test_file_name_json,
                         example_list_dicts):
    json_file = JSONManager(example_file_name_json_def)
    json_file.file_name = example_test_file_name_json
    json_file.write_to_file(example_list_dicts)
    data_load = json_file.load_from_file()
    assert example_list_dicts[0] and example_list_dicts[1] and example_list_dicts[2] in data_load
    json_file.delete_from_file()

# def test_write_file_ini(example_class_ini, example_file_name_json_2,
#                         example_write_params, example_params_dict):
#     example_class_ini.file_name = example_file_name_json_2
#     example_class_ini.write_to_file(*example_write_params)
#     example_params_conn = config()
#     assert example_params_conn == example_params_dict

# example_params_conn_ = config()
# print(example_params_conn_)