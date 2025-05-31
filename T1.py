import requests
import re
from collections import Counter
import time

ips2 = [
    "81.30.83.98",
    "194.84.46.110",
    "37.192.247.194",
    "31.246.103.203"
]

def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def extract_ips(html):
    # Регулярное выражение для поиска IPv4 адресов
    pattern = r'(\d{1,3}\.){3}\d{1,3}'
    ips = re.findall(pattern, html)

    # re.findall с группами возвращает кортежи, преобразуем в строки
    ips = re.findall(r'(\d{1,3}(?:\.\d{1,3}){3})', html)

    return set(ips)  # уникальные IP


def get_country_by_ip(ip):
    url = f"https://ipwhois.app/json/{ip}"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        if data.get("success", True) is False:
            return None
        return data.get("country")
    except Exception as e:
        print(f"Ошибка при запросе для IP {ip}: {e}")
        return None

def show(ips):
    country_counter = Counter()

    for ip in ips:
        country = get_country_by_ip(ip)
        if country:
            country_counter[country] += 1
            print(f"{ip} -> {country}")
        else:
            print(f"{ip} -> Страна не определена")
        time.sleep(1)

    print("\nРейтинг стран по количеству пользователей-редакторов:")
    for country, count in country_counter.most_common():
        print(f"{country}: {count}")

def main():
    show(ips2)
    url = "https://ru.wikipedia.org/w/index.php?title=JSON&action=history"
    html = get_html(url)

    ips = extract_ips(html)
    print(f"Найдено уникальных IP: {len(ips)}")
    show((ips))





if __name__ == "__main__":
    main()
