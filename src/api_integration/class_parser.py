# Импортируем функцию urljoin для построения абсолютного url-адреса
from urllib.parse import urljoin
# Импортируем библиотеку requests для отправки http-запросов
import requests


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
                    continue
                if 'id' not in item['employer']:
                    continue
                if 'name' not in item['employer']:
                    continue
                if 'alternate_url' not in item['employer']:
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
