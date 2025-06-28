import logging

# запуск логирования 
logging.basicConfig(
    level=logging.INFO,  # Show messages with level INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),  # Write logs to file
        logging.StreamHandler()  # Also output logs to console
    ]
)

#главный логгер для приложения
logger = logging.getLogger("loggi_moviedb")


def get_logger(module_name):
    """
    Return a logger instance for the given module name.

    Args:
        module_name (str): The name of the module requesting the logger.

    Returns:
        Logger instance associated with the module_name.
    """
    return logging.getLogger(module_name)