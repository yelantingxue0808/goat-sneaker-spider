"""
@Author  : 孔天宇
@Desc    : 
"""
from config import logging_settings
import os
import logging


def get_logger():
    logger = logging.getLogger(logging_settings.LOGGER_NAME)
    if logger.handlers:  # 避免重复添加处理器
        return logger
    # 确保日志目录存在
    if not os.path.exists(logging_settings.LOGGER_PATH):
        os.mkdir(logging_settings.LOGGER_PATH)
    path_file = os.path.join(logging_settings.LOGGER_PATH, 'logger_nike.log')
    # 初始化处理器+格式器
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(path_file, encoding='utf-8', mode='a')
    formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s : %(message)s')
    # 绑定格式+添加处理器
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger
