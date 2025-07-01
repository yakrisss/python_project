"""
Logger configuration module.

Sets up basic logging to a file and provides a function to get
module-specific logger instances with consistent formatting and encoding.
"""


import logging

# Configure root logger (do this once in main entry point of the app)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
    ]
)

# Optional: main app logger for generic logs
logger = logging.getLogger("loggi_moviedb")


def get_logger(module_name: str) -> logging.Logger:
    """
    Return a logger instance for the given module name.

    Args:
        module_name (str): The name of the module requesting the logger.

    Returns:
        logging.Logger: Logger instance associated with the module_name.
    """
    return logging.getLogger(module_name)
