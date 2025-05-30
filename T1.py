import requests
import re
import collections
from bs4 import BeautifulSoup

def get_ip_country(ip_address):
    """Определяет страну по IP-адресу, используя API ipwhois.io."""
    try:
        response = requests.get(f"https://ipwhois.io/{ip_address}")
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        return data.get("country")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса к API ipwhois.io: {e}")
        return None
    except Exception as e:
        print(f"Ошибка обработки ответа API: {e}")
        return None


def analyze_wikipedia_editors(wiki_url):
    """
    Анализирует историю изменений страницы Wikipedia,
    извлекает IP-адреса редакторов и определяет их страны.
    """
    try:
        response = requests.get(wiki_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении страницы Wikipedia: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Поиск всех ссылок на историю изменений
    history_links = soup.find_all('a', href=re.compile(r'/w/index.php\?title=.+&action=history'))

    ip_addresses = []
    for link in history_links:
      history_url = 'https://en.wikipedia.org' + link['href']

      response = requests.get(history_url)
      response.raise_for_status()

      soup = BeautifulSoup(response.text, 'xml') # ИЗМЕНЕНИЕ ЗДЕСЬ: Используем XML-парсер

      # Находит все div блоки с классом "mw-changeslist-line"
      change_lines = soup.find_all('div', class_='mw-changeslist-line')

      for line in change_lines:
          user_link = line.find('a', class_='mw-userlink')
          if user_link:
              href = user_link.get('href')
              # Извлекаем IP-адрес из ссылки пользователя
              ip_match = re.search(r'User:((\d{1,3}\.){3}\d{1,3})', href)
              if ip_match:
                  ip_addresses.append(ip_match.group(1))

    if not ip_addresses:
        print("IP-адреса не найдены.")
        return

    country_counts = collections.Counter()
    for ip in ip_addresses:
        country = get_ip_country(ip)
        if country:
            country_counts[country] += 1

    print("\nРейтинг стран по количеству редакторов:")
    for country, count in country_counts.most_common():
        print(f"{country}: {count}")


# Пример использования
wiki_url = "https://en.wikipedia.org/w/index.php?title=JSON&action=history"
analyze_wikipedia_editors(wiki_url)
