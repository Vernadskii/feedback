import atexit
from loguru._logger import Logger as LoguruLogger, Core as LoguruCore


class Logger(LoguruLogger):
    def bind(self, **kwargs):
        *options, extra = self._options
        return Logger(self._core, *options, {**extra, **kwargs})

    def trace(self, event: str, message: str = '', **kwargs):
        b = self.bind(event=event, **kwargs)
        super(Logger, b).trace(message)

    def debug(self, event: str, message: str = '', **kwargs):
        b = self.bind(event=event, **kwargs)
        super(Logger, b).debug(message)

    def info(self, event: str, message: str = '', **kwargs):
        b = self.bind(event=event, **kwargs)
        super(Logger, b).info(message)

    def success(self, event: str, message: str = '', **kwargs):
        b = self.bind(event=event, **kwargs)
        super(Logger, b).success(message)

    def warning(self, event: str, message: str = '', **kwargs):
        b = self.bind(event=event, **kwargs)
        super(Logger, b).warning(message)

    def error(self, event: str, message: str = '', **kwargs):
        b = self.bind(event=event, **kwargs)
        super(Logger, b).error(message)

    def exception(self, event: str, message: str = '', **kwargs):
        b = self.bind(event=event, **kwargs)
        super(Logger, b).exception(message)


logger = Logger(
    core=LoguruCore(),
    exception=None,
    depth=0,
    record=False,
    lazy=False,
    colors=False,
    raw=False,
    capture=True,
    patchers=None,
    extra={},
)

atexit.register(logger.remove)

