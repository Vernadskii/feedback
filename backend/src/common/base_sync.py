import signal
import sys

import pika
from django.conf import settings
from common.logger import logger


class CommonSync:
    """Базовый класс для синхронизаций."""

    def _module_name(self):
        return str(self.__module__).split('.')[-1]

    def _prepare(self):
        for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGQUIT]:
            signal.signal(sig, self.signal_handler)

    def signal_handler(self, signum, frame):
        logger.info(
            event=f'{self._module_name()}__handle',
            message='Terminating...',
        )
        sys.exit(0)


class SyncRabbit(CommonSync):
    """Синхронизация через Rabbit."""

    connection_mq = None
    mq_channel = None

    """
    Логика повторов:
    5 раз по 60 секунд
    5 раз по 10 минут
    """
    RETRY_INTERVALS = {
        # количество секунд |-> количество повторов
        60: 5,
        600: 5,
    }

    def signal_handler(self, signum, frame):
        self.close_mq()
        super().signal_handler(signum, frame)

    def connect_mq(self, heartbeat=90):
        credentials = pika.PlainCredentials(settings.RABBITMQ["USER"], settings.RABBITMQ["PASSWORD"])
        conn_param = pika.ConnectionParameters(
                host=settings.RABBITMQ["HOSTS"],
                virtual_host=settings.RABBITMQ["VHOST"],
                connection_attempts=5,
                retry_delay=1,
                credentials=credentials,
                heartbeat=heartbeat,
                blocked_connection_timeout=heartbeat,
        )

        self.connection_mq = pika.BlockingConnection(conn_param)
        self.mq_channel = self.connection_mq.channel()
        self.mq_channel.exchange_declare(exchange="feedback", durable=True, auto_delete=False)

        self.mq_channel.queue_declare(queue="receipts", durable=True)
        self.mq_channel.queue_bind("receipts", "feedback")

        self.mq_channel.queue_declare(queue="poll_notifications", durable=True)
        self.mq_channel.queue_bind("poll_notifications", "feedback")

    def close_mq(self):
        if self.connection_mq:
            logger.info(
                event=f'{self._module_name()}__handle',
                message='Closing gracefully MQ connection...',
            )
            self.connection_mq.close()
        return True
