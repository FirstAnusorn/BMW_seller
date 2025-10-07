import logging
import os

def setup_logger(name):
    logger = logging.getLogger(name)
    
    if logger.hasHandlers():
        return logger
    
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(f'{log_dir}/app.log')
    stream_handler = logging.StreamHandler()

    file_handler.setLevel(logging.DEBUG) 
    stream_handler.setLevel(logging.INFO) 

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
    return logger