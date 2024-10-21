import logging
import functools

logging.basicConfig(
    level=logging.INFO,  # lvl logging INFO
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def log_function_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check, is the first argument of a class instance
        if args and hasattr(args[0], '__class__'):
            instance = args[0]
            class_name = instance.__class__.__name__
        try:
            # Call func
            result = func(*args, **kwargs)
            # Logging result
            if args and hasattr(args[0], '__class__'):
                logging_bot.info(f"Calling method '{class_name}.{func.__name__}' with args={args[1:]} kwargs={kwargs}")
                logging_bot.info(f"Method '{class_name}.{func.__name__}' returned {result}")
            else:
                logging_bot.info(f"Calling function '{func.__name__}' with args={args} kwargs={kwargs}")
                logging_bot.info(f"Function '{func.__name__}' returned {result}")

            return result

        except Exception as ex:
            # Logging error
            logging_bot.error(f"Error in method '{class_name}.{func.__name__}': {ex}")

    return wrapper


logging_bot = logging.getLogger(__name__)
