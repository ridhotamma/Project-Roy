import logging
import logging.config
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(sys.stdout)

log_formatter = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)s] %(filename)s:%(lineno)d: %(message)s")
stream_handler.setFormatter(log_formatter)

logger.addHandler(stream_handler)
