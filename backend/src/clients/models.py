from django.db import models


class Client(models.Model):
    GENDER_UNKNOWN = 0
    GENDER_MALE = 1
    GENDER_FEMALE = 2

    GENDERS = (
        (GENDER_UNKNOWN, "не указан"),
        (GENDER_MALE, "мужской"),
        (GENDER_FEMALE, "женский"),
    )

    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    card_number = models.CharField(verbose_name="Номер карты", max_length=255, blank=True, null=True)
    first_name = models.CharField(verbose_name="Имя", max_length=255, blank=True, null=True)
    last_name = models.CharField(verbose_name="Фамилия", max_length=255, blank=True, null=True)
    city = models.CharField(verbose_name="Город", max_length=255, blank=True, null=True)
    gender = models.PositiveIntegerField(verbose_name="Пол", choices=GENDERS, default=GENDER_UNKNOWN)
    date_birth = models.DateField(verbose_name="Дата рождения", blank=True, null=True)
    email = models.CharField(verbose_name="Email", max_length=255, blank=True, null=True)
    phone = models.CharField(verbose_name="Телефон", max_length=50, blank=True, null=True)
    last_communication = models.DateTimeField(verbose_name="Дата последней коммуникации", blank=True, null=True)