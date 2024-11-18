import json
import pika
from django.conf import settings
from django.core.management import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from common.base_sync import SyncRabbit
from common.logger import logger
from common.receipt import Receipt
from polls.models import Poll, PollConditions

LOGGER_EVENT: str = 'receipt_process'
LOGGER_MESSAGE: str = 'Get incoming receipt'


class Command(SyncRabbit, BaseCommand):
    help = "Process receipts data"
    receipt_period = 1 * 60  # (1 час) Максимально допустимое время для чека
    consumer = None
    cache = None
    pending_stats = {}
    pending_stats_extra = {}  # тут храним PUSH-токены клиентов и ID чеков
    pending_stats_updated = None

    def handle(self, *args, **kwargs):
        logger.info(
            event='receipt_process__handle',
            message='receipt_process is being started',
        )

        self._prepare()
        self.connect_mq(settings.RABBITMQ_HEARTBEAT)
        self.mq_channel.basic_qos(prefetch_count=50)  # set the limit for the channel
        self.mq_channel.basic_consume(on_message_callback=self.callback, queue="receipts")
        self.mq_channel.start_consuming()
        logger.info(
            event='receipt_process__handle',
            message='receipt_process has been started',
        )

    def callback(self, ch, method, properties, body):
        receipt_data = json.loads(body)
        logger.debug(event=LOGGER_EVENT, message=LOGGER_MESSAGE, payload__receipt_data=receipt_data)
        receipt = Receipt(receipt_data)
        suitable_polls = self._get_suitable_polls(receipt)  # ищем доступные опросы
        if len(suitable_polls) > 0:
            selected_poll_id = Poll.objects.get_random_priority_poll(suitable_polls)
            self.add_poll_data_to_queue(selected_poll_id, receipt)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def add_poll_data_to_queue(self, selected_poll_id, receipt):
        client = receipt.data()["client"]
        poll_data = {
            "poll_id": selected_poll_id,
            "client_id": client["id"]
        }

        self.mq_channel.basic_publish(
            exchange="feedback",
            routing_key="poll_notifications",
            body=json.dumps(poll_data, cls=DjangoJSONEncoder),
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def _get_suitable_polls(self, receipt):
        all_active_polls = Poll.objects.filter(status=Poll.STATUS_ACTIVE)

        conditions = PollConditions.objects.filter(poll_id__in=active_polls).exclude(
                condition_id=PollConditions.RESPONDENT_TRIGGERS_TEST
            ).order_by(
                "poll_id",
            ).values()
