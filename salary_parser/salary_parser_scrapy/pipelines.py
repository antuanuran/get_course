import pandas as pd


class SalaryParserPipeline:
    data = []

    def process_item(self, item, spider):
        self.data.append(item)
        return item

    def close_spider(self, spider):
        import os

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skillsup.settings")
        os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

        import django

        django.setup()

        from apps.vacancies.models import CityStatus

        df = pd.DataFrame(data=self.data)
        df: pd.DataFrame = df[["city", "converted_price_min", "converted_price_max"]].groupby("city").mean()
        for city, (min_price, max_price) in df.iterrows():
            CityStatus.objects.update_or_create(
                city=city,
                defaults=dict(min_price=int(min_price), max_price=int(max_price)),
            )
