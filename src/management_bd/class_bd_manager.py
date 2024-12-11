# Импортируем библиотеку psycopg2 для взаимодействия с базами данных
import psycopg2


class DBManager:
    """
    Класс для взаимодействия с БД
    """

    def __init__(self, bd: str, params_conn: dict,):
        """
        Инициирует конструктор класса
        """
        self._bd = bd
        self._params_conn = params_conn
        conn = psycopg2.connect(dbname=self._bd, **self._params_conn)
        conn.autocommit = True
        self._conn = conn
        self._cursor = self._conn.cursor()
    #
    def create_db(self, database_users_name='database_user') -> str:
        """
        Создание пустой базы данных
        """
        try:
            self._cursor.execute(f"DROP DATABASE {database_users_name}")
        except Exception as e:
            print(f"\nОшибка создания базы данных: {e}")
        finally:
            self._cursor.execute(f"CREATE DATABASE {database_users_name}")

        return f"\nБаза {database_users_name} для добавления информации о компаниях и их вакансиях создана."


    def create_tables_for_data_hh(self):
        """
        Создание таблиц для данных по компаниям и их вакансиям
        """

        with self._cursor as cur:
            cur.execute("""
                CREATE TABLE companies (
                company_id integer PRIMARY KEY,
                company_name varchar(150) unique NOT NULL,
                company_url text NOT NULL,
                count_vacancies integer NOT NULL
                )
            """)

        self._cursor = self._conn.cursor()

        with self._cursor as cur:
            cur.execute("""
                CREATE TABLE vacancies (
                vacancy_id integer PRIMARY KEY,
                company_name varchar(150) NOT NULL,
                vacancy_name varchar(150) NOT NULL,
                vacancy_url text NOT NULL,
                city varchar(150) NOT NULL,
                salary_min integer,
                salary_max integer,
                currency varchar(50) NOT NULL,
                experience varchar(50) NOT NULL,
                requirements text,
                responsibilities text,
                
                constraint fk_vacancies_companies foreign key (company_name) REFERENCES companies(company_name)
                )
            """)
        return True
        # self._cursor.close()

    def save_data_to_db(self, companies_data: list[dict],
                        vacancies_data: list[dict]):
        """Сохранение данных о компаниях и вакансиях в базу данных."""

        self._cursor = self._conn.cursor()

        with self._cursor as cur:
            for company in companies_data:
                company_id = company['id']
                company_name = company['name']
                company_url = company['link']
                count_vacancies = company['open_vacancies']
                cur.execute("""
                    INSERT INTO companies (company_id, company_name, company_url, count_vacancies)
                    VALUES (%s, %s, %s, %s)
                """, (company_id, company_name, company_url, count_vacancies))

            for vacancy in vacancies_data:
                vacancy_id = vacancy['id']
                company_name = vacancy['employer_name']
                vacancy_name = vacancy['name']
                vacancy_url = vacancy['link']
                city = vacancy['city']
                # salary = vacancy['salary']
                salary_min = vacancy['salary_from']
                salary_max = vacancy['salary_to']
                currency = vacancy['currency']
                experience = vacancy['experience']
                requirements = vacancy['requirements']
                responsibilities = vacancy['duties']
                cur.execute("""
                    INSERT INTO vacancies (vacancy_id, company_name, vacancy_name, vacancy_url, city, 
                    salary_min, salary_max, currency, experience, requirements, responsibilities)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (vacancy_id, company_name, vacancy_name, vacancy_url, city, salary_min, salary_max, currency,
                      experience, requirements, responsibilities))

        return True

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """

        self._cursor = self._conn.cursor()

        self._cursor.execute("""
                SELECT c.company_name, COUNT(v.vacancy_id) AS vacancy_counter 
                FROM companies c
                LEFT JOIN vacancies v USING(company_name)
                GROUP BY c.company_name;
            """)
        return self._cursor.fetchall()

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию
        """

        self._cursor = self._conn.cursor()

        self._cursor.execute("""
                SELECT c.company_name, v.vacancy_name, v.salary_min, v.salary_max, v.vacancy_url
                FROM companies c
                JOIN vacancies v USING(company_name);
            """)
        return self._cursor.fetchall()

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям
        """

        self._cursor = self._conn.cursor()

        self._cursor.execute("""
                SELECT ROUND(AVG((salary_min + salary_max) / 2)) AS avg_salary
                FROM vacancies;
            """)
        return self._cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """

        self._cursor = self._conn.cursor()

        self._cursor.execute("""
                SELECT * FROM vacancies
                WHERE (salary_min + salary_max) > 
                (SELECT AVG(salary_min + salary_max) FROM vacancies);
            """)
        return self._cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий,
        в названии которых содержатся переданные в метод слова
        """

        self._cursor = self._conn.cursor()

        self._cursor.execute("""
                SELECT * FROM vacancies 
                WHERE vacancy_name LIKE '%%' || %s || '%%';
            """, (keyword,))  # '%%' означает любую последовательность символов перед и после ключевого слова (%s)
        return self._cursor.fetchall()

    def __del__(self):
        """
        Заканчивает соединение с объектом для внесения изменения в базу данных и закрывает соединение с базой.
        """
        self._cursor.close()
        self._conn.close()