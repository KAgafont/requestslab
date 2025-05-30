import requests
import json

def get_hh_vacancies(search_text, per_page=10, page=0):
    """
    Получает список вакансий с сайта HeadHunter по заданному поисковому запросу.
    """
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": search_text,
        "per_page": per_page,
        "page": page,
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API HeadHunter: {e}")
        return None


def calculate_average_salary(vacancies):
    """
    Вычисляет среднюю зарплату по списку вакансий.
    Учитываются только вакансии с указанными значениями 'from' и 'to'.
    """
    total_salary = 0
    count = 0
    if vacancies and 'items' in vacancies:
        for vacancy in vacancies['items']:
            salary = vacancy.get('salary')
            if salary and salary.get('from') and salary.get('to'):
                total_salary += (salary['from'] + salary['to']) / 2
                count += 1

    if count > 0:
        return total_salary / count
    else:
        return None


# Пример использования
search_text = "C#"
vacancies = get_hh_vacancies(search_text, per_page=100, page=0)  # Запрашиваем до 100 вакансий на первой странице

if vacancies:
    average_salary = calculate_average_salary(vacancies)
    if average_salary:
        print(f"Средняя зарплата по вакансиям C#: {average_salary:.2f}")
    else:
        print("Нет данных о зарплате для расчета средней зарплаты.")
