import logging


def test_case(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            logging.info(f"{func.__name__} [PASSED]")
        except Exception as e:
            logging.error(f"{func.__name__} [FAILED]: {e}")

    return wrapper


def handle_kafka_error(err):
    raise Exception(f"Error: {err}")
