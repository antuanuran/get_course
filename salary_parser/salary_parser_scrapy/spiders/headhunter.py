import re

import scrapy


class HeadhunterSpider(scrapy.Spider):
    name = "headhunter"
    start_urls = [
        (
            "https://hh.ru/search/vacancy"
            "?ored_clusters=true&search_period=7&search_field=name&search_field=company_name"
            "&search_field=description&text=Python&enable_snippets=false&customDomain=1"
        ),
    ]

    KNOWN_CURRENCIES = {
        "₽": 1,
        "$": 90,
        "Br": 30,
        "₸": 0.2,
        # TODO
    }

    find_digits = re.compile(r"\d+")

    def _safe_parse_int(self, value: str) -> int:
        return int(float(value.replace(",", ".")))

    def parse(self, response, **kwargs):  # noqa: C901
        # page = response.url.split("/")

        data = []

        for selector in response.xpath('//div[@class="vacancy-serp-item__layout"]'):
            name = selector.css("span.serp-item__title").xpath("text()").get()
            city = selector.css("div.vacancy-serp-item__info").xpath("div[2]/text()").get()
            raw_salary = selector.css("div.vacancy-serp-item-body__main-info").xpath("div[1]/span[1]/text()").getall()
            link = selector.css("a::attr(href)").get()

            price_min = 0
            price_max = 0
            currency = "₽"
            for element in raw_salary:
                element = element.strip()
                if not element:
                    continue
                if element in self.KNOWN_CURRENCIES:
                    currency = element
                    continue
                value = element.encode("ascii", "ignore").decode("ascii")
                values = self.find_digits.findall(value)
                if not values:
                    continue
                if price_min:
                    price_max = self._safe_parse_int(values[0])
                else:
                    price_min = self._safe_parse_int(values[0])
                    if len(values) > 1:
                        price_max = self._safe_parse_int(values[1])

            if not price_max:
                price_max = price_min

            converted_price_min = int(price_min * self.KNOWN_CURRENCIES[currency])
            converted_price_max = int(price_max * self.KNOWN_CURRENCIES[currency])

            data.append(
                {
                    "name": name,
                    "city": city,
                    "price_min": price_min,
                    "price_max": price_max,
                    "currency": currency,
                    "converted_price_min": converted_price_min,
                    "converted_price_max": converted_price_max,
                    "link": link,
                }
            )

        print(data)

        next_page = response.xpath('//div[@class="pager"]/a').attrib.get("href")
        if next_page:
            next_page_url = "https://hh.ru" + next_page
            request = scrapy.Request(url=next_page_url)
            yield request
