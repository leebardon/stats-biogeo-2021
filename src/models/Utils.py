import logging
import os
from pathlib import Path
from src.models import Save

BASE = Path(os.path.abspath(__file__)).parents[2]
LOGS = Save.check_dir_exists(f"{BASE}/.logs")

def setup_logger(name, level=logging.INFO):
    """
    Args:
        level: Logs at or above 'level' are committed to file as default.
    Returns:
        logger: instance of logger class
    """
    formatter = logging.Formatter('%(asctime) %(filename)s:%(funcName)s: %(levelname)s - %(message)s')
    handler = logging.FileHandler(f"{LOGS}/{name}.log")
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
