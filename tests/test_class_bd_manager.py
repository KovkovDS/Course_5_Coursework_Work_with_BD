# Импортируем фреймворк для тестирования кода
from decimal import Decimal

import pytest

from unittest.mock import patch, MagicMock

import psycopg2
# Импортируем классы объектов из файла classes_for_services.py
from src.management_bd.class_bd_manager import DBManager

@pytest.fixture()
def example_class_db_m():
    params = {'user': 'postgres', 'password': '1711postgres2024', 'host': 'localhost'}
    example_bd_m = DBManager('postgres',params)
    return example_bd_m

@pytest.fixture()
def example_class_user_db_m():
    params = {'user': 'postgres', 'password': '1711postgres2024', 'host': 'localhost'}
    example_bd_m = DBManager('user_vacancies_hh',params)
    return example_bd_m

@pytest.fixture()
def example_class_test_db_m():
    params = {'user': 'postgres', 'password': '1711postgres2024', 'host': 'localhost', 'port': '5432'}
    example_bd_m = DBManager('test_bd', params)
    return example_bd_m

@pytest.fixture()
def example_test_db_name():
    return 'test_bd'

@pytest.fixture()
def part_response_for_request_hh2_comp():
    return   {
    "name": "Российский Фонд Образовательных Программ Экономика и управление",
    "link": "https://hh.ru/employer/1417021",
    "id": "1417021",
    "open_vacancies": 13
  }
@pytest.fixture()
def part_response_for_request_hh2_vac():
    return {
    "id": "112545045",
    "name": "Руководитель образовательных программ юридического направления",
    "employer_id": "1417021",
    "employer_name": "Российский Фонд Образовательных Программ Экономика и управление",
    "employer_url": "https://hh.ru/employer/1417021",
    "link": "https://hh.ru/vacancy/112545045",
    "city": "Москва",
    "salary_from": 130000,
    "salary_to": 200000,
    "currency": "RUR",
    "experience": "Более 6 лет",
    "busy": "Полная занятость",
    "schedule": "Удаленная работа",
    "requirements": "Знание нормативных актов и требований и большой опыт работы юристом и/или консультантом. Постоянное совершенствование своих профессиональных навыков. ",
    "duties": "Разработка новых программ курсов/семинаров по праву (в т.ч. актуализация имеющихся программ) для крупных и средних компаний (с выручкой..."
  }

@pytest.fixture()
def example_answer_1_on_user_db_m():
    return [('Центр занятости населения по Городу Бийску, Бийскому и Солтонскому Районам',
  250),
 ('Ассоциация Специалистов Городского Хозяйства по Развитию Управленческих '
  'Кадров',
  156),
 ('ГБУЗ ПО ПСКОВСКАЯ ОБЛАСТНАЯ ИНФЕКЦИОННАЯ БОЛЬНИЦА', 138)]


@pytest.fixture()
def example_answer_2_on_user_db_m():
    return [('Ассоциация Специалистов Городского Хозяйства по Развитию Управленческих '
  'Кадров',
  'Корпоративный юрист в холдинговую компанию',
  250000,
  330000,
  'https://hh.ru/vacancy/112308142'),
 ('Центр занятости населения по Городу Бийску, Бийскому и Солтонскому Районам',
  'Заведующий библиотекой',
  45000,
  50000,
  'https://hh.ru/vacancy/112371048'),
 ('ГАУ СО Агентство по развитию человеческого капитала',
  'Заместитель руководителя по информатизации',
  130000,
  0,
  'https://hh.ru/vacancy/112567457')]


@pytest.fixture()
def example_answer_4_on_user_db_m():
    return [(112308142,
  'Ассоциация Специалистов Городского Хозяйства по Развитию Управленческих '
  'Кадров',
  'Корпоративный юрист в холдинговую компанию',
  'https://hh.ru/vacancy/112308142',
  'Москва',
  250000,
  330000,
  'RUR',
  'От 1 года до 3 лет',
  'Высшее юридическое образование. Релевантный опыт работы не менее 3-х лет '
  'обязателен. Корпоративная практика. Судебная практика по корпоративным '
  'спорам.',
  'Крупный многоотраслевой холдинг (ЖКХ, строительство) со множественностью '
  'юридических лиц. Участие в реализации юридической стратегии холдинга. '
  'Участие в правовом сопровождении корпоративных...'),
 (112567457,
  'ГАУ СО Агентство по развитию человеческого капитала',
  'Заместитель руководителя по информатизации',
  'https://hh.ru/vacancy/112567457',
  'Южно-Сахалинск',
  130000,
  0,
  'RUR',
  'От 1 года до 3 лет',
  'Высшее-профессиональное или среднее-профессиональное образование по профилю '
  'деятельности. Опыт работы на аналогичной должности не мене 1 года. ',
  'Осуществлять установку, настройку и обновление операционных систем, '
  'прикладного программного обеспечения, серверных приложений и сетевых и '
  'сетевых сервисов филиала. '),
 (112652290,
  'ГАУ СО Агентство по развитию человеческого капитала',
  'Геодезист',
  'https://hh.ru/vacancy/112652290',
  'Саратов',
  120000,
  220000,
  'RUR',
  'От 3 до 6 лет',
  'Высшее образование в области геодезии, картографии, геоинформатики или '
  'смежных дисциплин. Глубокое знание действующих законов и нормативных актов '
  'в области геодезических...',
  'Выполнять инженерно-геодезические изыскания для различных строительных и '
  'инфраструктурных проектов. Проводить полевые измерения с использованием '
  'геодезического оборудования (теодолит, нивелир, GPS). ')]


@pytest.fixture()
def example_answer_5_on_user_db_m():
    return [(110744809,
  'Центр занятости населения по Городу Бийску, Бийскому и Солтонскому Районам',
  'Оператор станков с программным управлением',
  'https://hh.ru/vacancy/110744809',
  'Бийск',
  40000,
  100000,
  'RUR',
  'От 3 до 6 лет',
  'Образование среднее специальное или опыт работы не менее 3 лет.',
  'Изготовление деталей на станках с ЧПУ.'),
 (111040477,
  'Центр занятости населения по Городу Бийску, Бийскому и Солтонскому Районам',
  'Инженер программист',
  'https://hh.ru/vacancy/111040477',
  'Бийск',
  81420,
  0,
  'RUR',
  'От 1 года до 3 лет',
  'Усидчивость, внимательность, дисциплинированность Опыт работы от 3 лет '
  'Образование: Высшее.',
  'Программирование в среде 1С: 8.2; 8.3.'),
 (110963866,
  'Филиал ГКУ ПО Центр занятости населения Пензенской области по г. Заречному',
  'Инженер-программист ("ФНПЦ "ПО "Старт" имени М. В. Проценко)',
  'https://hh.ru/vacancy/110963866',
  'Пенза',
  41915,
  0,
  'RUR',
  'Нет опыта',
  'Образование: Высшее.',
  'Разрабатывать программы, технологию решения задач, инструкции по работе с '
  'программами. Осуществлять подготовку разработанных программ к откладке.')]


@patch('src.management_bd.class_bd_manager.psycopg2.connect')
def test_create_db(mock_connect, example_class_db_m, example_test_db_name):
    mock_cursor = MagicMock()
    mock_connect.return_value.__enter__.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [('Company A', 5), ('Company B', 3), ('Company C', 1)]

    result = example_class_db_m.create_db(example_test_db_name)

    if mock_cursor.execute(f"DROP DATABASE {example_test_db_name}"):
        assert result == f"\nБаза {example_test_db_name} для добавления информации о компаниях и их вакансиях создана."


@patch('src.management_bd.class_bd_manager.psycopg2.connect')
def test_create_table(mock_connect, example_class_test_db_m):
    mock_cursor = MagicMock()
    mock_connect.return_value.__enter__.return_value.cursor.return_value = mock_cursor

    result = example_class_test_db_m.create_tables_for_data_hh()
    mock_cursor.execute(f"DROP TABLE companies")
    if mock_cursor.execute(f"DROP TABLE companies") is False:
        assert result is True

@patch('src.management_bd.class_bd_manager.psycopg2.connect')
def test_save_data_to_db(mock_connect, example_class_test_db_m, part_response_for_request_hh2_vac,
                         part_response_for_request_hh2_comp, example_answer_4_on_user_db_m):
    mock_cursor = MagicMock()
    mock_connect.return_value.__enter__.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = ('Company A', 5), ('Company A', 'Vacancy A', 1000, 2000, 'http://example.com/vacancy_a')

    result = example_class_test_db_m.save_data_to_db([part_response_for_request_hh2_comp], [part_response_for_request_hh2_vac])

    assert result is True
    mock_cursor.execute("""
                SELECT c.company_name, COUNT(v.vacancy_id) AS vacancy_counter 
                FROM companies c
                LEFT JOIN vacancies v USING(company_name)
                GROUP BY c.company_name;
            """)


@patch('src.management_bd.class_bd_manager.psycopg2.connect')
def test_get_companies_and_vacancies_count(mock_connect, example_class_user_db_m, example_answer_1_on_user_db_m):
    # Настройка имитации курсора и результата
    mock_cursor = MagicMock()
    mock_connect.return_value.__enter__.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [('Company A', 5), ('Company B', 3), ('Company C', 1)]

    result = example_class_user_db_m.get_companies_and_vacancies_count()
    for i in result:
        print(i)
    print(result)
    assert result[:3] == example_answer_1_on_user_db_m
    mock_cursor.execute("""
                SELECT c.company_name, COUNT(v.vacancy_id) AS vacancy_counter 
                FROM companies c
                LEFT JOIN vacancies v USING(company_name)
                GROUP BY c.company_name
    """)

@patch('src.management_bd.class_bd_manager.psycopg2.connect')
def test_get_all_vacancies(mock_connect, example_class_user_db_m, example_answer_2_on_user_db_m):
    mock_cursor = MagicMock()
    mock_connect.return_value.__enter__.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        ('Company A', 'Vacancy A', 1000, 2000, 'http://example.com/vacancy_a'),
        ('Company B', 'Vacancy B', 1500, 2500, 'http://example.com/vacancy_b')
    ]

    result = example_class_user_db_m.get_all_vacancies()

    assert result[:3] == example_answer_2_on_user_db_m
    mock_cursor.execute("""
                SELECT c.company_name, v.vacancy_name, v.salary_min, v.salary_max, v.vacancy_url
                FROM companies c
                JOIN vacancies v USING(company_name)
            """)

@patch('src.management_bd.class_bd_manager.psycopg2.connect')
def test_get_avg_salary(mock_connect, example_class_user_db_m):
    mock_cursor = MagicMock()
    mock_connect.return_value.__enter__.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [('Company A', 1500), ('Company B', 2000)]

    result = example_class_user_db_m.get_avg_salary()

    assert result == Decimal('54354')
    mock_cursor.execute("""
                ELECT ROUND(AVG((salary_min + salary_max) / 2)) AS avg_salary
                FROM vacancies;
            """)

@patch('src.management_bd.class_bd_manager.psycopg2.connect')
def test_get_vacancies_with_higher_salary(mock_connect, example_class_user_db_m, example_answer_4_on_user_db_m):
    mock_cursor = MagicMock()
    mock_connect.return_value.__enter__.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [('Vacancy A',), ('Vacancy B',)]

    result = example_class_user_db_m.get_vacancies_with_higher_salary()

    assert result[:3] == example_answer_4_on_user_db_m
    mock_cursor.execute("""
                SELECT * FROM vacancies
                WHERE (salary_min + salary_max) > 
                (SELECT AVG(salary_min + salary_max) FROM vacancies)
            """)

@patch('src.management_bd.class_bd_manager.psycopg2.connect')
def test_get_vacancies_with_keyword(mock_connect, example_class_user_db_m, example_answer_5_on_user_db_m):
    keyword = 'программ'
    mock_cursor = MagicMock()
    mock_connect.return_value.__enter__.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [('Developer Vacancy',)]

    result = example_class_user_db_m.get_vacancies_with_keyword(keyword)

    assert result[:3] == example_answer_5_on_user_db_m
    mock_cursor.execute(
        "SELECT * FROM vacancies"
        " WHERE vacancy_name LIKE %s", ('%программ%',)
    )