import logging


def get_logger() -> logging.Logger:
    logger = logging.getLogger("workflow_executor")

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(levelname)s] %(asctime)s | %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
