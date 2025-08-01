import logging
from logging.handlers import TimedRotatingFileHandler
import os
import configparser
import settings

def setup_logger():
    # 读取 config.ini 配置
    config = configparser.ConfigParser()
    config.read(settings.INI_FILE, encoding='utf-8')
    log_file = settings.TEST_DATA_FILE
    log_level_str = config.get('logging', 'log_level', fallback='DEBUG').upper()
    log_format = config.get('logging', 'log_format', fallback='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    backup_count = config.getint('logging', 'backup_count', fallback=30)

    # 映射日志等级
    log_level = getattr(logging, log_level_str, logging.DEBUG)

    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    if not logger.handlers:
        # 创建一个 TimedRotatingFileHandler，按天生成新日志文件
        # log_file 日志文件路径
        # when = 'midnight' 每天午夜轮换日志文件一次（新建一个新文件）
        # interval = 1 每1个周期（这里是1天）执行轮换
        # backupCount = 30 最多保留30个历史日志文件，超过的自动删除
        # encoding = 'utf-8' 避免中文乱码等问题
        handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=backup_count, encoding='utf-8')
        handler.suffix = "%Y-%m-%d"
        handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(handler)

    return logger
