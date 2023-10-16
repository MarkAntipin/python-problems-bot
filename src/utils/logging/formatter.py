import json
import logging
from logging import LogRecord


class JSONFormatter(logging.Formatter):
    def format(self, record: LogRecord) -> str:  # noqa: A003
        log_data = {
            'time': self.formatTime(record),
            'name': record.name,
            'level': record.levelname,
            'message': record.getMessage(),
        }
        return json.dumps(log_data)
