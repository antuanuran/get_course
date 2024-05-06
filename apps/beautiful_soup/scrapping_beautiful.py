import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

url = "https://hh.ru/search/vacancy?ored_clusters=true&search_period=7&search_field=name&search_field=company_name&search_field=description&text=Python&enable_snippets=false&customDomain=1"  # noqa: E501

head = Headers(browser="firefox", os="win").generate()

resp = requests.get(url, headers=head)
soup = BeautifulSoup(resp.text, "html.parser")

cards_all = soup.find_all(class_="vacancy-serp-item__layout")


def main():
    # data = []
    for card in cards_all:
        print("\n")
        # Название вакансии
        name = card.find("span", {"data-qa": "serp-item__title"}).text
        print(name)

        # Salary
        raw_salary = card.find("span", {"data-qa": "vacancy-serp__vacancy-compensation"})
        if raw_salary:
            raw_salary = raw_salary.text.strip()
            salary = raw_salary.encode("ascii", "ignore").decode("ascii")
            print(salary)

        else:
            print("-")

        # Город
        city = card.find("div", {"data-qa": "vacancy-serp__vacancy-address"}).text
        print(city)

        # Ссылка на вакансию
        link = card.find("a")["href"]
        print(link)
