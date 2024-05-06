import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

url = "https://hh.ru/search/vacancy?ored_clusters=true&search_period=7&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&customDomain=1&currency_code=USD&text=Python&page=1"  # noqa: E501

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

        # Город
        city = card.find("div", {"data-qa": "vacancy-serp__vacancy-address"}).text
        print(city)

        # Salary
        raw_salary = card.find("span", {"data-qa": "vacancy-serp__vacancy-compensation"})
        if raw_salary:
            salary_list = []
            currency = None

            raw_salary = raw_salary.text.strip()
            print(f"Зарплатная вилка: ({raw_salary})")

            raw_salary = raw_salary.encode("ascii", "ignore").decode("ascii").strip()
            salary = raw_salary.split()

            if len(salary) == 1:
                salary_list.append(float(*salary))
                salary_list.append(float(*salary))
                currency = "руб."
                print(salary_list, currency)

            elif len(salary) == 3:
                salary_list.append(float(salary[0]))
                salary_list.append(float(salary[1]))
                currency = salary[2]
                print(salary_list, currency)

            else:
                salary_list.append(float(salary[0]))

                try:
                    salary_list.append(float(salary[1]))
                    currency = "руб."
                    print(salary_list, currency)

                except ValueError:
                    salary_list.append(salary[0])
                    currency = salary[1]
                    print(salary_list)
                    print(salary_list, currency)

        else:
            print("-")

        # Ссылка на вакансию
        link = card.find("a")["href"]
        print(link)
