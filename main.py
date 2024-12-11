# Импортируем классы для работы и отправки запросов на сервисы по подбору вакансий
import string

from config import config
# Импортируем библиотеку string удобной фильтрации по ключевому слову
from string import punctuation
# Импортируем библиотеку string удобной фильтрации по ключевому слову
from string import ascii_letters

from src.api_integration.class_parser import HeadHunterAPI
# Импортируем классы для работы и отправки запросов на сервисы по подбору вакансий
from src.management_bd.class_bd_manager import DBManager
# Импортируем функцию для определения окончания слова "сайт"
# from src.func.auxiliary_func import end_word_question
# Импортируем класс для преобразования информации с сервисов в список вакансий
# from src.work_with_vacancies.class_vacancy import Vacancy
# Импортируем класс для работы со списком вакансий
# from src.work_with_vacancies.work_with_vacancies_list import VacanciesProcessing
# Импортируем класс для работы с INI файлами
from src.work_with_files.work_with_data import INIManager
# Импортируем класс для работы с Excel файлами
import psycopg2


def main():
    """
        Функцию для взаимодействия с пользователем через консоль. Данная функция реализует:

        Ввод поискового запроса для запроса вакансий из со всех поддерживаемых программой сервисов вакансий;
        Получение топ N вакансий по зарплате (N запрашивает у пользователя);
        Получение вакансии с ключевым словом в описании.

    """
    # Создание экземпляров классов для работы с API всех сайтов с вакансиями, которые доступны программе
    hh_api = HeadHunterAPI()
    hh_api.params_for_comp = 'да'

    print(f'\nВас приветствует мини приложение для получения и сохранения в файл базы данных (по умолчанию базы данных '
          f'PostgreSQL) информации по компаниям, по умолчанию минимум 10, и их вакансиям с сайта {hh_api}. \nДанное '
          f'приложение получает информацию лишь по тем компаниях, у которых на сайте присутствуют открытые вакансии. '
          f'\nЕсли не укажите количество компаний для вывода информации по ним и дальнейшей работе с этой информацией, '
          f'выведется по умолчания по топ 10 компаниям. \nТакже, для работы с приложением вам необходимо установить ПО '
          f'для работы с базами данных "PostgreSQL", скачать его можно с сайта по ссылке '
          f'https://www.postgresql.org/download/. \nВ процессе установки "PostgreSQL", или после этого, нужно задать '
          f'пароль для пользователя "postgres", который является "администратором" для автоматически создаваемой при '
          f'установке приложения базы "postgres". \nДалее по алгоритму работы приложения Вам необходимо будет ввести '
          f'данные: сервер с БД и порт подключения - "localhost" и 5432 (оба значения по умолчанию), БД, которая '
          f'присутствует по умолчанию на сервере - "postgres", и данные для авторизации в ней, которые вы указали при '
          f'установке "PostgreSQL". \nПри успешной установке соединения данные будут записаны в файл с конфигурацией '
          f'подключения - "database.ini".')


    print('\nДля начала подключимся к вашей базе, которая точно присутствует на вашем сервере (БД по умолчанию). '
          'Как только установится соединение, введенные Вами данные будут сохранены в конфигурационный файл для '
          'подключения к ней.')

    while True:
        user_server = input(f'\nУкажите наименование сервера (хоста) или его IP-адрес (в формате https://*.*.*.* , '
                            f'IP-адрес хоста по умолчания "localhost" - https://127.0.0.1) '
                            f'\nили нажмите "Enter" и будет применено значение по умолчанию: ')
        if user_server == '':
            user_server = 'localhost'
        user_server_port = input(f'\nУкажите номер порта для подключения к серверу или нажмите "Enter" и будет применено '
                            f'значение по умолчанию: ')
        if user_server_port == '':
            user_server_port = '5432'
        user_default_bd = input(f'\nУкажите наименование базы данных или нажмите "Enter" и будет применено значение по '
                            f'умолчанию: ')
        if user_default_bd == '':
            user_default_bd = 'postgres'
        user_authorizations_name = input(f'\nУкажите пользователя базы данных, указанной ранее или нажмите "Enter" и будет '
                                         f'применено значение по умолчанию: ')
        if user_authorizations_name == '':
            user_authorizations_name = 'postgres'
        user_authorizations_pass = input(f'\nУкажите пароль пользователя базы данных, указанной ранее: ')

    # Подключение к серверу с базами данных и создание базы для передачи в нее информации из запроса приложения
        try:
            conn = psycopg2.connect(
                host=user_server,
                port=user_server_port,
                dbname=user_default_bd,
                user=user_authorizations_name,
                password=user_authorizations_pass
            )
            conn.close()
            print('\nСоединение с базой успешно установлено. '
                  '\nСоздан конфигурационный файл для соединения с базой по умолчанию, которую вы указали ранее '
                  '- "database.ini".')
            break
        except psycopg2.OperationalError:
            print(f'\n\n\nНе удалось установить соединение с базой данных. Проверьте вводимые данные.')
        # while psycopg2.OperationalError:
        #     user_server = input(f'\nУкажите наименование сервера (хоста) или его IP-адрес (в формате https://*.*.*.* , '
        #                         f'IP-адрес хоста по умолчания "localhost" - https://127.0.0.1) или нажмите "Enter" и будет '
        #                         f'применено значение по умолчанию: ')
        #     if user_server == '':
        #         user_server = 'localhost'
        #     user_server_port = input(
        #         f'\nУкажите номер порта для подключения к серверу или нажмите "Enter" и будет применено '
        #         f'значение по умолчанию: ')
        #     if user_server_port == '':
        #         user_server_port = '5432'
        #     user_default_bd = input(
        #         f'\nУкажите наименование базы данных или нажмите "Enter" и будет применено значение по '
        #         f'умолчанию: ')
        #     if user_default_bd == '':
        #         user_default_bd = 'postgres'
        #     user_authorizations_name = input(
        #         f'\nУкажите пользователя базы данных, указанной ранее или нажмите "Enter" и будет '
        #         f'применено значение по умолчанию: ')
        #     if user_authorizations_name == '':
        #         user_authorizations_name = 'postgres'
        #     user_authorizations_pass = input(f'\nУкажите пароль пользователя базы данных, указанной ранее: ')
            continue
            # try:
            #     conn = psycopg2.connect(
            #         host=user_server,
            #         port=user_server_port,
            #         dbname=user_default_bd,
            #         user=user_authorizations_name,
            #         password=user_authorizations_pass
            #         )
            #     conn.close()
            # except psycopg2.OperationalError:
            #     print('\n\n\nНе удалось установить соединение с базой данных. Проверьте вводимые данные.')
            #     user_server = input(f'\nУкажите наименование сервера или нажмите "Enter" и будет применено значение '
            #                         f'по умолчанию: ')
            #     if user_server == '':
            #         user_server = 'localhost'
            #     user_server_port = input(
            #         f'\nУкажите номер порта для подключения к серверу или нажмите "Enter" и будет применено '
            #         f'значение по умолчанию: ')
            #     if user_server_port == '':
            #         user_server_port = '5432'
            #     user_bd = input(f'\nУкажите наименование базы данных или нажмите "Enter" и будет применено значение по '
            #                     f'умолчанию: ')
            #     if user_default_bd == '':
            #         user_default_bd = 'postgres'
            #     user_authorizations_name = input(
            #         f'\nУкажите пользователя базы данных, указанной ранее или нажмите "Enter" и будет '
            #         f'применено значение по умолчанию: ')
            #     if user_authorizations_name == '':
            #         user_authorizations_name = 'postgres'
            #     user_authorizations_pass = input(f'\nУкажите пароль пользователя базы данных, указанной ранее: \n')
    # else:
    # name_ini_file = input(
    #     f'\nУкажите имя конфигурационного файла ли нажмите "Enter" и будет применено значение по умолчанию: ')

    ini_file = INIManager()
    ini_file.write_to_file(user_server, user_authorizations_name, user_authorizations_pass, user_server_port)
    params_conn = config()

    user_bd = input(f'\nУкажите наименование базы данных латинскими буквами (можно использовать "Space/Пробел"), '
                    f'\nкоторая будет создана для записи данных по вашему запросу на {hh_api} или нажмите "Enter" '
                    f'и база будет названа "user_vacancies_hh": ').replace(" ", "_")
    list_str_name_user_bd = user_bd.split()
    str_punctuation = string.punctuation
    str_tellers = string.ascii_letters
    if list_str_name_user_bd in ('', 'None', [], None):
        user_bd = 'user_vacancies_hh'
    else:
        for letters in list_str_name_user_bd:
            if letters not in (str_punctuation, str_tellers):
                print('\nВ наименовании БД Вы указали не допустимы символы, наименование базы будет "user_vacancies_hh".')
                user_bd = 'user_vacancies_hh'

    default_bd = DBManager(user_default_bd, params_conn)
    default_bd.create_db(user_bd)
    default_bd.__del__()
    new_bd = DBManager(user_bd, params_conn)
    new_bd.create_tables_for_data_hh()

    # print(f"\nБаза {user_bd} для добавления информации о компаниях и их вакансиях создана.")

    search_query = input("\nВведите поисковый запрос для формирования списка компаний, отсортированных по"
                         " количеству открытых вакансий по убыванию: ")
    open_vacancies = 'да'
    hh_api.params_for_comp = open_vacancies
    list_request_for_company = hh_api.get_companies(search_query)
    while not list_request_for_company:
        print(f"\nПо данному запросу не найдено ни одной компании. Повторите запрос.")

        search_query = input("\nВведите поисковый запрос для формирования списка компаний, отсортированных по"
                             " количеству открытых вакансий по убыванию: ")
        open_vacancies = 'да'
        hh_api.params_for_comp = open_vacancies
        list_request_for_company = hh_api.get_companies(search_query)

    try:
        top_n = int(input('\nВведите количество компаний, по которым будет отправлен запрос информации по вакансиям.'
                          ' Либо нажмите "Enter" и будет применено значение по умолчанию: '))
        if top_n < 10:
            print('\nВведенное количество компаний для вывода в топ не может быть меньше 10. '
                  'Для ранжирования по убывания будет взято значение по умолчанию.')
    except ValueError:
        top_n = 10

    list_top_n_companies = hh_api.get_top_n_companies(list_request_for_company, top_n)
    list_companies_id = []
    for comp in list_top_n_companies:
        list_companies_id.append(comp['id'])

    salary_agreement = input(
        '\nЗапросить информацию по вакансиям без конкретно указанной зарплаты (по договоренности)?'
        ' Введите: "да" или "нет": ').lower()
    while salary_agreement != 'да' or salary_agreement != 'нет':
        if salary_agreement == 'да' or salary_agreement == 'нет':
            break
        else:
            print("\nВы ввели некорректное значение. Введите корректный ответ.")
            salary_agreement = input('\nЗапросить информацию по вакансиям без конкретно указанной зарплаты (по '
                                     'договоренности)? Введите: "да" или "нет": ').lower()

    hh_api.params_for_vac = salary_agreement
    list_vac_companies = hh_api.get_vacancies('', list_companies_id)
    new_bd.save_data_to_db(list_top_n_companies, list_vac_companies)

    print(f"\nДанные о компаниях и их вакансиях в БД {user_bd} добавлены.")

    print(f'\nТеперь вы можете получить информацию о компаниях и их вакансиях, сделав любой их предложенных запросов, '
          f'либо нажмите "Enter" и закончите работу с приложением:'
          f'\n        1 - Список всех компаний и количество вакансий у каждой компании'
          f'\n        2 - Список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на '
          f'вакансию'
          f'\n        3 - Средняя зарплата по вакансиям'
          f'\n        4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям'
          f'\n        5 - Список всех вакансий, в названии которых содержатся ключевые слова')

    # user_query_on_bd = input(f'\nВведите интересующий Вас запрос: ')

    while True:
        user_query_on_bd = input(f'\n\n\nВведите интересующий Вас запрос: ')
        if user_query_on_bd == '1':
            companies_and_vacancies_count = new_bd.get_companies_and_vacancies_count()
            print("\n\n\nКомпании и количество доступных вакансий:")
            for company_name, vacancy_counter in companies_and_vacancies_count:
                print(f"{company_name}: {vacancy_counter}")
        elif user_query_on_bd == '2':
            all_vacancies = new_bd.get_all_vacancies()
            print("\n\n\nВсе вакансии:")
            for vacancy in all_vacancies:
                company_name, vacancy_name, salary_min, salary_max, vacancy_url = vacancy
                print(f"Компания: {company_name}. Вакансия: {vacancy_name}. Зарплата: {salary_min}-{salary_max}. "
                      f"Ссылка на вакансию: {vacancy_url}.")
        elif user_query_on_bd == '3':
            avg_salary = new_bd.get_avg_salary()
            print(f"\n\n\nСредняя зарплата по всем вакансиям: {avg_salary}.")
        elif user_query_on_bd == '4':
            higher_salary_vacancies = new_bd.get_vacancies_with_higher_salary()
            print("\n\n\nВакансии с зарплатой выше средней:")
            for vacancy in higher_salary_vacancies:
                # company_name, vacancy_name, salary_min, salary_max, vacancy_url = vacancy
                print(f'Компания: {vacancy[1]}. Вакансия: {vacancy[2]}. Ссылка на вакансию: {vacancy[3]}. '
                      f'Город: {vacancy[4]}. Зарплата: {vacancy[5]}-{vacancy[6]}. Валюта: {vacancy[7]}. '
                      f'Опыт: {vacancy[8]}. Требования: {vacancy[9]}. Обязанности: {vacancy[10]}.')
        elif user_query_on_bd == '5':
            keyword = input("\nВведите ключевое слово для поиска вакансий: ")
            vacancies_with_keyword = new_bd.get_vacancies_with_keyword(keyword)
            # print(type(vacancies_with_keyword))
            print(f"\n\n\nВсе вакансии с ключевым словом '{keyword}':")
            for vacancy in vacancies_with_keyword:
                # print(type(vacancy))
                # company_name, vacancy_name, salary_min, salary_max, vacancy_url = vacancy
                # print(f"Компания: {company_name}, Вакансия: {vacancy_name}, Зарплата: {salary_min}-{salary_max},"
                #       f"Ссылка на вакансию: {vacancy_url}")
                print(f'Компания: {vacancy[1]}. Вакансия: {vacancy[2]}. Ссылка на вакансию: {vacancy[3]}. '
                      f'Город: {vacancy[4]}. Зарплата: {vacancy[5]}-{vacancy[6]}. Валюта: {vacancy[7]}. '
                      f'Опыт: {vacancy[8]}. Требования: {vacancy[9]}. Обязанности: {vacancy[10]}.')
        elif user_query_on_bd == '':
            new_bd.__del__()
            print("\nПриложение заканчивается свою работу. Надеемся Вы еще им воспользуетесь! :)")
            exit()
        else:
            print("\nВы ввели некорректное значение. Введите корректный номер запроса.")
        # conn.autocommit = True
        # cur = conn.cursor()
        # cur.execute(f"DROP DATABASE {database_name}")
        # cur.execute(f"CREATE DATABASE {database_name}")


    # user_authorizations_pass

if __name__ == "__main__":
    main()