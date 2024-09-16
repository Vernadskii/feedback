import logging


class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.event = getattr(record, 'event', 'default_event')
        return super().format(record)
