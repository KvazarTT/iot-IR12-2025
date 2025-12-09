import logging


def logged(exception_cls, mode):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_cls as e:
                logger = logging.getLogger()
                if logger.hasHandlers():
                    logger.handlers.clear()
                if mode == "file":
                    logging.basicConfig(filename=r'C:\Users\matvi\PycharmProjects\PythonProject1\Data\log.txt', level=logging.ERROR,
                                        format='%(asctime)s - %(levelname)s - %(message)s', force=True)
                elif mode == "console":
                    logging.basicConfig(level=logging.ERROR,
                                        format='LOG: %(asctime)s - %(message)s', force=True)
                logging.error(f"Помилка у функції {func.__name__}: {e}")
                raise e
        return wrapper
    return decorator