# app/core/logging.py
import json
import logging
import sys
from typing import Any, Mapping, MutableMapping

DEFAULT_LEVEL = logging.INFO

class JsonFormatter(logging.Formatter):
    """Minimal JSON formatter with extras support."""
    def format(self, record: logging.LogRecord) -> str:
        payload: MutableMapping[str, Any] = {
            "level": record.levelname,
            "time": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S%z"),
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        # Attach any custom attributes (e.g., request_id)
        for key in ("request_id", "path", "method", "status_code"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        return json.dumps(payload, ensure_ascii=False)

def setup_logging(level: int = DEFAULT_LEVEL, json_output: bool = True) -> None:
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    if json_output:
        handler.setFormatter(JsonFormatter())
    else:
        fmt = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
        handler.setFormatter(logging.Formatter(fmt))
    root.addHandler(handler)

    # Quiet noisy libs if needed
    logging.getLogger("uvicorn").setLevel(level)
    logging.getLogger("uvicorn.error").setLevel(level)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)  # access logs are often too chatty

def enable_sql_logging(verbose: bool = False) -> None:
    """Turn on SQL logs (set True only for debugging)."""
    lvl = logging.INFO if verbose else logging.WARNING
    logging.getLogger("sqlalchemy.engine").setLevel(lvl)
