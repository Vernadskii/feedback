from django.core.validators import RegexValidator
from django.db import models

from django.contrib.auth.models import (AbstractBaseUser, AbstractUser, PermissionsMixin)

from django.utils import timezone
from django.contrib.auth.models import Group


class UserProfile(AbstractBaseUser, PermissionsMixin):
    GENDER_FEMALE = 1
    GENDER_MALE = 2
    GENDER = (
        (GENDER_FEMALE, "женский"),
        (GENDER_MALE, "мужской"),
    )

    email = models.EmailField("email", blank=False, unique=True)
    last_name = models.CharField("фамилия", max_length=255, blank=False)
    first_name = models.CharField("имя", max_length=255, blank=False)
    middle_name = models.CharField("отчество", max_length=255, blank=True)

    phone_validator = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be entered in the format: '9622397855'. Up to 10 digits allowed.",
        code='invalid_phone_number',
    )
    phone = models.CharField("телефон", validators=[phone_validator], min_length=10, max_length=10, blank=False)

    job_title = models.CharField("должность", max_length=255, blank=True)
    birth_date = models.DateField("дата рождения", blank=True, null=True)
    gender = models.PositiveIntegerField(choices=GENDER, default=None, blank=True, null=True, verbose_name="пол")
    avatar = models.ImageField("фотография", default="static/default_avatar.png")

    is_active = models.BooleanField(
        "active",
        default=True,
        help_text="Designates whether this user should be treated as active. " +
                  "Unselect this instead of deleting accounts.",
    )
    date_joined = models.DateTimeField("date joined", default=timezone.now)

    # TODO: add HistoricalRecords

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        full_name = f"{self.last_name} {self.first_name}"
        return full_name.strip()

