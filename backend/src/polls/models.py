from django.db import models
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

    CHANNELS_CODES = (
        "CHANNEL_SMS",
        "CHANNEL_EMAIL",
        "CHANNEL_WEB",
    )

    CHANNELS_ORDER: tuple[int, ...] = (
        CHANNEL_WEB,
        CHANNEL_EMAIL,
        CHANNEL_SMS,
    )

    CHANNELS_TOOLTIPS = (
        'SMS - Отправка sms сообщения клиенту с вопросом, на который клиент отвечает в ответном сообщении.',
        'E-mail - Отправка email письма со ссылкой на опрос.',
        'Web - Канал для сбора обратной связи через ссылку. Коммуникация по данному каналу отправлена не будет.',
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

    author = models.ForeignKey(UserProfile, verbose_name="Автор", blank=False, null=False, on_delete=models.PROTECT)

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

    def __str__(self):
        return self.title

    def save(self, *args, trigger_status_update=False, **kwargs):
        if self.status not in self.STATUSES_FINAL:
            if timezone.now().date() > self.date_finish:
                self.status = self.STATUS_FINISHED

        super().save(*args, **kwargs)


class PollQuestion(models.Model):
    fs = S3ProxyFileSystemStorage()
    # objects = PollQuestionManager()

    TYPE_TEXT = 1
    TYPE_SINGLE_ANSWER = 2
    TYPE_MULTIPLE_ANSWERS = 3

    TYPES = (
        (TYPE_TEXT, "Свободная форма"),
        (TYPE_SINGLE_ANSWER, "Одиночный выбор"),
        (TYPE_MULTIPLE_ANSWERS, "Множественный выбор"),
    )

    SKIPPABLE_TYPES: tuple[int] = (
        TYPE_SINGLE_ANSWER,
        TYPE_MULTIPLE_ANSWERS,
    )

    TYPES_CODES = (
        "TYPE_TEXT",
        "TYPE_SINGLE_ANSWER",
        "TYPE_MULTIPLE_ANSWERS",
    )

    # Используются в Poll.objects.update_answer_stats()
    TYPES_STATS_METHODS = {
        (TYPE_TEXT, "count"),
        (TYPE_SINGLE_ANSWER, "answers_count"),
        (TYPE_MULTIPLE_ANSWERS, "answers_count"),
    }

    poll = models.ForeignKey(Poll, verbose_name="Опрос", blank=False, on_delete=models.PROTECT)
    question_type = models.PositiveIntegerField(verbose_name="Тип вопроса", blank=False, choices=TYPES)
    title = models.TextField(verbose_name="Текст вопроса", blank=False)
    is_required = models.BooleanField(verbose_name="Обязательный", default=True)
    image = models.ImageField("Изображение", upload_to="questions", default=None, null=True, storage=fs)

    has_skip_answer = models.BooleanField(
        verbose_name='Присутствует ответ "Затрудняюсь ответить"',
        default=False,
    )
    is_last_page = models.BooleanField(
        default=False,
        verbose_name='Последняя страница опроса',
    )
    end_message_text = models.TextField(
        blank=True,
        null=True,
        verbose_name='Текст завершающего сообщения',
    )

    is_line_input_form = models.BooleanField(
        verbose_name='Форма для ввода ответа на вопрос в свободной форме - строка (Иначе - абзац)',
        default=False,
    )
    is_numerical_answer = models.BooleanField(
        verbose_name='Ответ на вопрос в свободной форме должен быть числом',
        default=False,
    )
    modified_at = models.DateTimeField(verbose_name="Дата модификации", auto_now=True)

    class Meta:
        ordering = ["order"]
