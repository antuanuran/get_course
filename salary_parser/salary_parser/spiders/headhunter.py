import scrapy


class HeadhunterSpider(scrapy.Spider):
    name = "headhunter"
    start_urls = [
        ("https://hh.ru/search/vacancy?ored_clusters=true&text=python&search_period=7"),
    ]

    KNOWN_CURRENCIES = {
        "$": 90,
        # TODO
    }

    def parse(self, response, **kwargs):  # noqa: C901
        # page = response.url.split("/")[-2]

        raw_salaries = [
            selector.xpath("text()").getall()
            for selector in response.xpath('//div[@class="vacancy-serp-item__layout"]/div/div/div/span')
        ]

        data = []
        for raw_salary in raw_salaries:
            price_min = None
            price_max = None
            currency = "₽"
            for element in raw_salary:
                element = element.strip()
                if not element:
                    continue
                if element in self.KNOWN_CURRENCIES:
                    currency = element
                    continue
                value = element.encode("ascii", "ignore").decode("ascii")
                # TODO: extract digits
                try:
                    value = float(value)
                except ValueError:
                    pass
                if isinstance(value, float):
                    if price_min is None:
                        price_min = value
                    else:
                        price_max = value

            if price_min is None:
                continue
            avg_price = price_min
            if price_max is not None:
                avg_price = (price_max + price_min) / 2
            if currency != "₽":
                avg_price *= self.KNOWN_CURRENCIES[currency]
            data.append(avg_price)

        print(data)
        print(sum(data) / len(data))

        # next_page = response.css('li.next a::attr("href")').get()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)

        # print(f"\n Вывод наименования вакансии:")
        # i = 0
        # for selector in response.xpath('//*[@id="a11y-main-content"]/div/div/div/div/div/div/h3/span/span/a/span'):
        #     element = selector.xpath("text()").getall()
        #     i += 1
        #     print(f"{i}. {element}")
        #
        # i = 0
        # print(f"\n Вывод городов:")
        # for selector in response.xpath('//*[@id="a11y-main-content"]/div/div/div/div/div/div/div/div'):
        #     element = selector.xpath("text()").getall()
        #     if element:
        #         i += 1
        #         print(f"{i}. {element}")
        #
        # i = 0
        # print(f"\n Вывод комапний:")
        # for selector in response.xpath('//*[@id="a11y-main-content"]/div/div/div/div/div/div/div/div/div/div/a/span'):
        #     element = selector.xpath("text()").getall()
        #     if element:
        #         i += 1
        #         print(f"{i}. {element}")
