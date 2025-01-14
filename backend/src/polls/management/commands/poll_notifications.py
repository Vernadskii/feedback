import json

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand

from clients.models import Client
from common.base_sync import SyncRabbit
from common.logger import logger
from polls.models import Poll, PollProgress
from utils.notification_services.email import EmailSender

LOGGER_EVENT: str = 'receipt_process'
LOGGER_MESSAGE: str = 'Get incoming receipt'


class Command(SyncRabbit, BaseCommand):
    help = "Send poll notifications"
    queue_name: str = 'poll_notifications'

    def handle(self, *args, **kwargs):
        logger.info(
            event='poll_notifications__handle',
            message='poll_notifications is being started',
        )

        self._prepare()
        self.connect_mq(settings.RABBITMQ_HEARTBEAT)
        self.mq_channel.basic_qos(prefetch_count=50)  # set the limit for the channel
        self.mq_channel.basic_consume(on_message_callback=self.callback, queue=self.queue_name)
        self.mq_channel.start_consuming()
        logger.info(
            event='poll_notifications__handle',
            message='poll_notifications__handle has been started',
        )

    def callback(self, ch, method, properties, body):
        notify_data = None
        try:
            notify_data = json.loads(body)
        except Exception as ex:
            logger.error(
                event='notify_poll_callback',
                message='JSON decode error',
            )

        if notify_data:
            self._notify_poll(notify_data=notify_data)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def _notify_poll(self, notify_data):
        client_card = notify_data.get("client_card_number")
        client = Client.objects.get(card_number=client_card)
        if not client:
            logger.warning(
                event='_notify_poll',
                message=f'There is no client with card number {client_card}',
            )
            return

        poll_id = notify_data.get("poll_id")
        poll = Poll.objects.get(pk=poll_id)

        if poll is None:
            # TODO: add logging
            return

        if poll.status != Poll.STATUS_ACTIVE:
            # TODO: add logging
            return

        notified = True  # flag that shows the client already notified
        try:
            PollProgress.objects.get(poll=poll, client=client)
        except ObjectDoesNotExist:
            notified = False

        if notified is False:
            new_progress = PollProgress.objects.create(poll=poll, client=client, status=PollProgress.STATUS_ACTIVE)
            if poll.channel == Poll.CHANNEL_EMAIL:
                result = EmailSender.send_email(sent_to=client.email, subject=poll.mail_title, content=poll.mail_content)
                print(result)
