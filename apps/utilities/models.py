from django.db import models


class BlacklistedWord(models.Model):
    class Meta:
        verbose_name = "запрещенное слово"
        verbose_name_plural = "запрещенные слова"

    def __str__(self) -> str:
        return self.word

    word = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        from apps.beautiful_soup.scrapping_beautiful import main

        main()
        super().save(*args, **kwargs)
