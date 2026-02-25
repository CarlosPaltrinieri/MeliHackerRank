import logging
import sys
from logging import Formatter
from contextvars import ContextVar
import uuid

# Context variable to store trace_id for the current request
trace_id_var: ContextVar[str] = ContextVar("trace_id", default="")

class TraceIdFilter(logging.Filter):
    """
    Log filter to inject trace_id into log records.
    """
    def filter(self, record):
        record.trace_id = trace_id_var.get()
        return True

def setup_logging():
    """
    Configures the application logger with JSON-like or structured formatting
    including the Trace ID.
    """
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)
    
    # Avoid adding multiple handlers if setup is called multiple times
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        
        # Format: [Time] [Level] [TraceID] - Message
        formatter = Formatter(
            fmt="%(asctime)s | %(levelname)-8s | trace_id=%(trace_id)-36s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        handler.setFormatter(formatter)
        handler.addFilter(TraceIdFilter())
        logger.addHandler(handler)
        
        # Add a file handler to save logs to a file
        file_handler = logging.FileHandler("app.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        file_handler.addFilter(TraceIdFilter())
        logger.addHandler(file_handler)
        
    # Also apply the filter to the root logger and uvicorn if needed
    for name in ["uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"]:
        ext_logger = logging.getLogger(name)
        ext_logger.addFilter(TraceIdFilter())

    return logger

# Initialize global logger
logger = setup_logging()
