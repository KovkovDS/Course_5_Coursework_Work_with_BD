# Импортируем функцию urljoin для построения абсолютного url-адреса
# from itertools import count
from urllib.parse import urljoin
# Импортируем библиотеку requests для отправки http-запросов
import requests
# Импортируем библиотеку xmltojson для обработки html-данных в json-данные
# import json
# Импортируем библиотеку json для взаимодействия с JSON-объектами
# from bs4 import BeautifulSoup
from src.work_with_files.work_with_data import JSONManager


class HeadHunterAPI:

    def __init__(self):
        """Инициирует конструктор класса."""
        self._headers = {'User-Agent': 'HH-User-Agent'}
        self._base_url = 'https://api.hh.ru'
        self._params_for_vac = {'text': '', 'per_page': 20}
        self._params_for_comp = {'text': '', 'per_page': 20}
        self._vacancies = []
        self._companies = []
        self._company = {}

    @property
    def params_for_vac(self):
        """Геттер параметров для отправки запроса на сервис.
        Предоставляет доступ к атрибуту для изменения его значения."""
        return self._params_for_vac

    @params_for_vac.setter
    def params_for_vac(self, salary_agreement):
        """Сеттер параметров для отправки запроса на сервис. Изменяет значение атрибута."""
        if salary_agreement == 'нет':
            self._params_for_vac['only_with_salary'] = True
        else:
            pass

    @property
    def params_for_comp(self):
        """Геттер параметров для отправки запроса на сервис.
        Предоставляет доступ к атрибуту для изменения его значения."""
        return self._params_for_comp

    @params_for_comp.setter
    def params_for_comp(self, availability_vacancies):
        """Сеттер параметров для отправки запроса на сервис. Изменяет значение атрибута."""
        if availability_vacancies == 'да':
            self._params_for_comp['only_with_vacancies'] = True
        else:
            pass

    @staticmethod
    def get_top_n_companies(sorted_companies: list, n=10) -> list:
        """Возвращает топ n компаний."""
        top_n_companies = sorted_companies[0:n]
        return top_n_companies

    def get_companies(self, keyword: str, pages_count: int = 249) -> list:
        """Получает ответ на get-запрос и записывает его в список компаний при подключении к API сервиса с
        вакансиями."""
        url = urljoin(self._base_url, 'employers')
        self._params_for_comp['text'] = keyword
        self._params_for_comp['sort_by'] = 'by_vacancies_open'

        for page in range(pages_count + 1):
            self._params_for_comp['page'] = page
            response = requests.get(url, headers=self._headers, params=self._params_for_comp)
            response.raise_for_status()

            for item in response.json()['items']:
                self._companies.append({'name': item['name'], 'link': item['alternate_url'],
                                        'id': item['id'], 'open_vacancies': item['open_vacancies']})
        return self._companies

    def get_data_company(self, employer_id: str) -> dict:
        """Получает ответ на get-запрос и возвращает сведения (карточку) о компании-работодателе при подключении к API сервиса с
        вакансиями."""
        url = urljoin(self._base_url, 'employers/') + employer_id

        response = requests.get(url, headers=self._headers)
        response.raise_for_status()

        self._company = {'name': response.json()['name'], 'link': response.json()['alternate_url'],
                         'id': response.json()['id'], 'open_vacancies': response.json()['open_vacancies'],
                         'link_site': response.json()['site_url']}
        return self._company


    def get_vacancies(self, keyword: str, employer_id: str or list, pages_count: int = 99) -> list:
        """Получает ответ на get-запрос и записывает его в список вакансий при подключении к API сервиса с
        вакансиями."""
        url = urljoin(self._base_url, 'vacancies')
        self._params_for_vac['text'] = keyword
        self._params_for_vac['employer_id'] = employer_id

        for page in range(pages_count + 1):
            self._params_for_vac['page'] = page
            response = requests.get(url, headers=self._headers, params=self._params_for_vac, timeout=5)
            response.raise_for_status()

            for item in response.json()['items']:
                if item['salary'] is None or item['salary'] == {}:
                    item['salary'] = {'from': 0, 'to': 0, 'currency': 'RUB'}
                if item['salary']['from'] is None or item['salary']['from'] == "None":
                    item['salary']['from'] = 0
                if item['salary']['to'] is None or item['salary']['to'] == "None":
                    item['salary']['to'] = 0
                if item['employer'] is None or item['employer'] == {}:
                    # count_employer_id += 1
                    # item['employer'] = {'alternate_url': 'Не указано', 'id': count_employer_id, 'name': 'Не указано'}
                    continue
                if 'id' not in item['employer']:
                    # count_employer_id += 1
                    # item['employer']['id'] = count_employer_id
                    continue
                if 'name' not in item['employer']:
                    # item['employer']['name'] = 'Не указано'
                    continue
                if 'alternate_url' not in item['employer']:
                    # item['employer']['alternate_url'] = 'Не указано'
                    continue
                self._vacancies.append({'id': item['id'], 'name': item['name'], 'employer_id': item['employer']['id'],
                                        'employer_name': item['employer']['name'],
                                        'employer_url': item['employer']['alternate_url'],
                                        'link': item['alternate_url'], 'city': item['area']['name'],
                                        'salary_from': item['salary']['from'], 'salary_to': item['salary']['to'],
                                        'currency': item['salary']['currency'], 'experience': item['experience']['name'],
                                        'busy': item['employment']['name'], 'schedule': item['schedule']['name'],
                                        'requirements': str(item['snippet']['requirement']).
                                       replace('<highlighttext>', '').replace('</highlighttext>', ''),
                                        'duties': str(item['snippet']['responsibility']).
                                       replace('<highlighttext>', '').replace('</highlighttext>', '')})
        return self._vacancies

    def __str__(self):
        """Выводим для пользователя наименование сервиса, в который отправлен запрос."""
        return f"HeadHunter"

# class RatingITCompanies:
#
#     def __init__(self):
#         """Инициирует конструктор класса."""
#         self._headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 \
#         (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#         self._base_url = 'https://raex-rr.com'
#         self._data_dict = {}
#
#     def get_data_from_rating(self) -> list:
#         """Получает ответ на get-запрос и записывает его в список вакансий при подключении к API сервиса с
#         вакансиями."""
#         url = urljoin(self._base_url, 'b2b/IT/best_in_software_development/2024/')
#         html_response = requests.get(url=url, headers=self._headers)
#
#         bs = BeautifulSoup(html_response.text, "html.parser")
#
#         full_list_top_it_companies = []
#         search_str = '/database/contender/'
#         for str_on_list in bs.find_all('a'):
#             if search_str in str_on_list.get('href'):
#                 full_list_top_it_companies.append(self._base_url + str_on_list.get('href'))
#         list_top_it_companies = full_list_top_it_companies[0:10]
#         # print(list_top_it_companies)
#
#         return list_top_it_companies
#
#     def data_to_list(self, list_href: list) -> list:
#         """Получает ответ на get-запрос и записывает его в список вакансий при подключении к API сервиса с
#         вакансиями."""
#         # self._base_url =
#         full_list_href_top_it_companies = []
#         search_str = 'class="member_link"'
#         for href in list_href:
#             # url = urljoin(self._base_url, 'b2b/IT/best_in_software_development/2024/')
#             html_response = requests.get(url=href, headers=self._headers)
#
#             bs = BeautifulSoup(html_response.text, "html.parser")
#             search_str_bs = bs.a['class']
#
#             # if search_str_bs == 'member_link':
#             #     print(bs.a)
#             #     full_list_href_top_it_companies.append(bs.a.get('href'))
#             # find_value =
#             for str_on_list in bs.find_all('a', class_="member_link"):
#                 # if search_str in str_on_list:
#                 # print(str_on_list)
#                 full_list_href_top_it_companies.append(str_on_list.get('href'))
#                 # print(str_on_list)
#             list_top_it_companies = full_list_href_top_it_companies
#             # print(list_top_it_companies)
#
#         return full_list_href_top_it_companies


# example_response_rat = RatingITCompanies()
# list_example_response_rat = example_response_rat.get_data_from_rating()
# print(list_example_response_rat)
# list_example_response_rat = example_response_rat.data_to_list(list_example_response_rat)
# print(list_example_response_rat)
# str_example_response_rat = ', '.join(list_example_response_rat)
# print(str_example_response_rat)
# print(type(str_example_response_rat))


# example_response_comp = HeadHunterAPI()
# example_file_with_comp = JSONManager()
# example_file_with_vac = JSONManager()
# example_file_with_comp_with_site = JSONManager()
# availability_vacancies_ = 'да'
# salary_agreement_ = 'да'
# top_10_IT_companies = 'top_10_IT_companies'
# vac_top_10_IT_companies = 'vac_top_10_IT_companies'
# top_10_IT_companies_with_site = 'top_10_IT_companies_with_site'
# example_file_with_comp.file_name = top_10_IT_companies
# example_response_comp.params_for_vac = salary_agreement_
# example_response_comp.params_for_comp = availability_vacancies_
# list_example_response_comp = example_response_comp.get_companies('программ')
# list_example_companies = example_response_comp.get_top_n_companies(list_example_response_comp)
# writed_file_with_comp = example_file_with_comp.write_to_file(list_example_companies)
# print(list_example_response_comp)
# print(len(list_example_response_comp))
# list_vac_example_company = []
# list_example_companies_id = []
# list_example_companies_with_site = []
# for comp in list_example_companies:
#     list_example_companies_id.append(comp['id'])
# print(list_example_companies_id)
# for id_comp in list_example_companies_id:
#     element_list = example_response_comp.get_data_company(id_comp)
#     list_example_companies_with_site.append(element_list)
# print(list_example_companies_with_site)
# example_file_with_comp_with_site.file_name = top_10_IT_companies_with_site
# writed_file_with_comp_and_site = example_file_with_comp_with_site.write_to_file(list_example_companies_with_site)
# list_vac_example_company.extend(example_response_comp.get_vacancies('', list_example_companies_id))
# writed_file_with_vac = example_file_with_vac.write_to_file(list_vac_example_company)
# print(list_vac_example_company)
# print(len(list_vac_example_company))



# example_response_comp = HeadHunterAPI()
# example_file_with_comp = JSONManager()
# example_file_with_vac = JSONManager()
# example_file_with_comp_with_site = JSONManager()
# availability_vacancies_ = 'да'
# salary_agreement_ = 'да'
# top_10_IT_companies = 'top_10_IT_companies_2'
# vac_top_10_IT_companies = 'vac_top_10_IT_companies_2'
# top_10_IT_companies_with_site  = 'top_10_IT_companies_with_site_2 '
# example_file_with_comp.file_name = top_10_IT_companies
# example_response_comp.params_for_vac = salary_agreement_
# example_response_comp.params_for_comp = availability_vacancies_
# list_example_response_comp = example_response_comp.get_companies('разработка')
# list_example_companies = example_response_comp.get_top_n_companies(list_example_response_comp)
# writed_file_with_comp = example_file_with_comp.write_to_file(list_example_companies)
# print(list_example_companies)
# print(len(list_example_response_comp))
# list_vac_example_company = []
# list_example_companies_id = []
# list_example_companies_with_site = []
# for comp in list_example_companies:
#     list_example_companies_id.append(comp['id'])
# for id_comp in list_example_companies_id:
#     element_list = example_response_comp.get_data_company(id_comp)
#     list_example_companies_with_site.append(element_list)
# example_file_with_comp_with_site.file_name = top_10_IT_companies_with_site
# writed_file_with_comp_and_site = example_file_with_comp_with_site.write_to_file(list_example_companies_with_site)
# # print(list_example_companies_id)
# list_vac_example_company.extend(example_response_comp.get_vacancies('', list_example_companies_id))
# writed_file_with_vac = example_file_with_vac.write_to_file(list_vac_example_company)
# print(list_vac_example_company)
# print(len(list_vac_example_company))