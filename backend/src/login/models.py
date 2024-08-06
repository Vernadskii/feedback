from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class MyUserManager(BaseUserManager):
    """Rewrite UserManager to delete unwanted 'username' attribute."""
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def active(self):
        return self.get_queryset().exclude(is_active=True)

    def _create_user(self, email, password, **extra_fields):
        """Create and save a user with the given email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):  # don't use AbstractUser because don't need 'username'
    GENDER_FEMALE = 1
    GENDER_MALE = 2
    GENDER = (
        (GENDER_FEMALE, "женский"),
        (GENDER_MALE, "мужской"),
    )

    first_name = models.CharField("имя", max_length=255, blank=False)
    last_name = models.CharField("фамилия", max_length=255, blank=False)
    middle_name = models.CharField("отчество", max_length=255, blank=True)
    email = models.EmailField("email address", blank=False, unique=True)

    phone_validator = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be entered in the format: '9622397855'. Up to 10 digits allowed.",
        code='invalid_phone_number',
    )
    phone = models.CharField("телефон", validators=[phone_validator], max_length=10, blank=False)

    job_title = models.CharField("должность", max_length=255, blank=True)
    birth_date = models.DateField("дата рождения", blank=True, null=True)
    gender = models.PositiveIntegerField(
        choices=GENDER, default=None, blank=True, null=True, verbose_name="пол",
    )
    avatar = models.ImageField("фотография", default="static/default_avatar.png")

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. " +
            "Unselect this instead of deleting accounts.",
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    # TODO: add HistoricalRecords

    objects = MyUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = 'email'  # Unique identifier for the user. It is the field that users will use to log in.
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Prompted for creating a superuser.

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        return self.get_full_name()

    def get_full_name(self) -> str:
        """Return the first_name plus the last_name, with a space in between."""
        full_name = "%s %s" % (self.first_name, self.last_name)  # noqa: WPS323
        return full_name.strip()
