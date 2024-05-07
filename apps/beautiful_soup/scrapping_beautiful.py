import requests
from bs4 import BeautifulSoup
from django.conf import settings
from fake_headers import Headers

url = settings.URL_VACANCY
head = Headers(browser="firefox", os="win").generate()

resp = requests.get(url, headers=head)
soup = BeautifulSoup(resp.text, "html.parser")

cards_all = soup.find_all(class_="vacancy-serp-item__layout")


def main():
    data_dict = {}
    data_list = []

    for card in cards_all:
        # Название вакансии
        name = card.find("span", {"data-qa": "serp-item__title"}).text

        # Город
        city = card.find("div", {"data-qa": "vacancy-serp__vacancy-address"}).text

        # Salary
        raw_salary = card.find("span", {"data-qa": "vacancy-serp__vacancy-compensation"})
        if raw_salary:
            currency = None
            salary_min = None
            salary_max = None
            salary_avg = None

            raw_salary = raw_salary.text.strip()
            raw_salary = raw_salary.encode("ascii", "ignore").decode("ascii").strip()
            salary = raw_salary.split()

            if len(salary) == 1:
                salary_min = float(*salary)
                salary_max = float(*salary)
                salary_avg = float(*salary)
                currency = "руб."

            elif len(salary) == 3:
                salary_min = float(salary[0])
                salary_max = float(salary[1])
                salary_avg = (salary_min + salary_max) / 2
                currency = salary[2]

            else:
                salary_min = float(salary[0])

                try:
                    salary_max = float(salary[1])
                    salary_avg = (salary_min + salary_max) / 2
                    currency = "руб."

                except ValueError:
                    salary_max = salary[0]
                    salary_avg = salary[0]
                    currency = salary[1]

        else:
            salary_min = None
            salary_max = None
            salary_avg = None
            currency = "руб."

        # Ссылка на вакансию
        link = card.find("a")["href"]

        data_dict["name"] = name
        data_dict["city"] = city
        data_dict["link"] = link
        data_dict["salary_min"] = salary_min
        data_dict["salary_max"] = salary_max
        data_dict["salary_avg"] = salary_avg
        data_dict["currency"] = currency

        # print(data_dict)
        data_list.append(data_dict.copy())

    return data_list
