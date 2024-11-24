import uuid
from functools import cache

from django.db import models
from django.db.models import JSONField
from django.utils import timezone

from polls.utils.storage import S3ProxyFileSystemStorage
from users.models import UserProfile


class Poll(models.Model):
    CHANNEL_SMS = 1
    CHANNEL_EMAIL = 2
    CHANNEL_WEB = 3

    CHANNELS = (
        (CHANNEL_SMS, "SMS"),
        (CHANNEL_EMAIL, "E-mail"),
        (CHANNEL_WEB, "Web"),
    )

    STATUS_ACTIVE = 2
    STATUS_FINISHED = 3
    STATUS_DELETED = 4
    STATUS_DRAFT = 5

    # неизменяемые статусы
    STATUSES_FINAL = [STATUS_FINISHED, STATUS_DELETED]

    STATUSES = (
        (STATUS_ACTIVE, "Активный"),
        (STATUS_FINISHED, "Закончен"),
        (STATUS_DELETED, "Удалён"),
        (STATUS_DRAFT, "Черновик"),
    )

    DEFAULT_MAIL_TITLE: str = 'Торговая сеть Бананчик: Опрос'
    DEFAULT_MAIL_PREHEADER: str = 'Приглашаем вас пройти опрос'
    DEFAULT_MAIL_CONTENT: str = (
        '<div>'
        '<strong>Здравствуйте!</strong><br><br>'
        '</div>'
        '<div>'
        'Спасибо, что выбираете магазины «Бананчик».'
        '</div>'
        '<div>'
        'Поделитесь Вашим мнением что необходимо исправить или улучшить, какие у нас слабые и сильные стороны —'
        ' это поможет сделать «Бананчик» лучше.'
        '</div>'
    )

    title = models.CharField(verbose_name="Название опроса", blank=False, max_length=255, unique=True)
    channel = models.PositiveIntegerField(verbose_name="Канал", choices=CHANNELS, blank=False, default=CHANNEL_WEB)
    status = models.PositiveIntegerField(
        verbose_name="Статус опроса", blank=False, choices=STATUSES, default=STATUS_DRAFT,
    )
    date_start = models.DateField(verbose_name="Дата начала опроса", blank=False, default=timezone.localdate)
    date_finish = models.DateField(verbose_name="Дата окончания опроса", blank=False, default=timezone.localdate)
    communications_total = models.PositiveIntegerField(
        verbose_name="Общее количество коммуникаций на опрос", blank=False, default=0,
    )
    stats_sent = models.PositiveIntegerField(verbose_name="Отправлено", default=0, editable=False)

    author = models.ForeignKey(
        UserProfile, verbose_name="Автор", blank=False, null=False, on_delete=models.PROTECT,
    )

    modified = models.DateTimeField(verbose_name="Обновлено", auto_now=False, default=timezone.now)

    mail_title = models.CharField(
        verbose_name='Заголовок письма',
        max_length=255,
        default=DEFAULT_MAIL_TITLE,
    )
    mail_preheader = models.CharField(
        verbose_name='Прехедер письма',
        max_length=255,
        default=DEFAULT_MAIL_PREHEADER,
    )
    mail_content = models.TextField(
        verbose_name='Текст письма',
        default=DEFAULT_MAIL_CONTENT,
    )

    class Meta:
        ordering = ["modified"]
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

        indexes = [models.Index(fields=["status"])]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, trigger_status_update=False, **kwargs):  # noqa: ANN002, ANN003
        if self.status not in self.STATUSES_FINAL:
            if timezone.now().date() > self.date_finish:
                self.status = self.STATUS_FINISHED  # noqa: WPS601

        super().save(*args, **kwargs)

    @staticmethod
    @cache
    def poll_statuses() -> list[int]:
        """Return the list with possible statuses numbers."""
        return [st[0] for st in Poll.STATUSES]

    @staticmethod
    @cache
    def poll_channels() -> list[int]:
        """Return the list with possible channel numbers."""
        return [ch[0] for ch in Poll.CHANNELS]


class PollQuestion(models.Model):
    fs = S3ProxyFileSystemStorage()

    TYPE_TEXT = 1
    TYPE_SINGLE_ANSWER = 2
    TYPE_MULTIPLE_ANSWERS = 3

    TYPES = (
        (TYPE_TEXT, "Свободная форма"),
        (TYPE_SINGLE_ANSWER, "Одиночный выбор"),
        (TYPE_MULTIPLE_ANSWERS, "Множественный выбор"),
    )

    poll = models.ForeignKey(Poll, verbose_name="Опрос", blank=False, on_delete=models.PROTECT)
    question_type = models.PositiveIntegerField(verbose_name="Тип вопроса", blank=False, choices=TYPES)
    title = models.TextField(verbose_name="Текст вопроса", blank=False)
    is_required = models.BooleanField(verbose_name="Обязательный", default=True)
    image = models.ImageField("Изображение", upload_to="questions", default=None, null=True, storage=fs)

    has_skip_answer = models.BooleanField(
        verbose_name='Присутствует ответ "Затрудняюсь ответить"',
        default=False,
    )

    modified_at = models.DateTimeField(verbose_name="Дата модификации", auto_now=True)

    class Meta:
        ordering = ["modified_at"]


class PollQuestionAnswer(models.Model):
    question = models.ForeignKey(PollQuestion, verbose_name="Вопрос", blank=False, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст ответа", blank=False)
    modified_at = models.DateTimeField(verbose_name="Дата модификации", auto_now=True)

    class Meta:
        ordering = ["modified_at"]


class PollConditions(models.Model):
    """
    Условия для опросов. ID опроса, тип условия, JSON с условиями срабатывания опроса
    """

    TYPE_CONDITION = 1

    TYPES = (
        (TYPE_CONDITION, "Условия"),
    )

    CONDITIONS_TRIGGER_ITEM_RECEIPT_SUM = "conditions_trigger_item_receipt_sum"

    CONDITIONS_TRIGGER_ITEM_RECEIPT_EVENTS = (
        (CONDITIONS_TRIGGER_ITEM_RECEIPT_SUM, "Сумма чека"),
    )

    poll = models.OneToOneField(Poll, verbose_name="Опрос", blank=False, on_delete=models.PROTECT, unique=True)
    condition_type = models.PositiveIntegerField(verbose_name="Тип", blank=False, choices=TYPES)
    condition_id = models.CharField(
        verbose_name="Условие", max_length=255, default=CONDITIONS_TRIGGER_ITEM_RECEIPT_SUM,
        choices=CONDITIONS_TRIGGER_ITEM_RECEIPT_EVENTS
    )
    condition_value = JSONField(verbose_name="Содержание условия")
    modified_at = models.DateTimeField(verbose_name="Дата модификации", auto_now=True)

    class Meta:
        ordering = ["poll"]


class PollProgress(models.Model):
    """Прогресс прохождения опроса клиентом."""

    STATUS_ACTIVE = 1  # Пользователь ещё не ответил на все вопросы опроса.
    STATUS_FINISHED = 2  # Пользователь закончил прохождение опроса

    STATUSES = (
        (STATUS_ACTIVE, 'Активный'),
        (STATUS_FINISHED, 'Закончен'),
    )

    unique_id = models.UUIDField(verbose_name='Уникальный ID опроса', default=uuid.uuid4, editable=False)
    poll = models.ForeignKey(Poll, verbose_name='Опрос', blank=False, on_delete=models.PROTECT)
    client = models.ForeignKey('clients.Client', verbose_name='Клиент', null=True, blank=True, on_delete=models.PROTECT)
    status = models.PositiveIntegerField(verbose_name='Статус', blank=False, choices=STATUSES, default=STATUS_ACTIVE)
    modified_at = models.DateTimeField(verbose_name="Дата модификации", auto_now=True)

    def get_poll_questions(self):
        result = PollQuestion.objects.filter(poll_id=self.poll_id).prefetch_related('pollquestionanswer_set').all()
        return result


class PollProgressAnswer(models.Model):
    """
    Ответы пользователя на вопросы в опросе
    """
    poll_progress = models.ForeignKey('polls.PollProgress', verbose_name='Прогресс клиента', blank=False, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, verbose_name='Опрос', blank=False, on_delete=models.PROTECT)
    question = models.ForeignKey(PollQuestion, verbose_name='Вопрос', blank=False, on_delete=models.CASCADE)
    answer = models.ForeignKey(PollQuestionAnswer, verbose_name='Вариант ответа', blank=True, null=True, on_delete=models.CASCADE)
    answer_text = models.TextField(verbose_name='Текстовый ответ', blank=True, null=True)
    date = models.DateTimeField(verbose_name='Дата ответа', blank=False, auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name="Дата модификации", auto_now=True)
