
import sys, os
import logging
from logging.handlers import RotatingFileHandler


def log_init(log_name='test', level="INFO"):
    # 日志存放路径
    log_dir = './logs'
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    # 日志文件路径
    if '.log' not in log_name:
        log_name = log_name + '.log'
    log_name = os.path.join(log_dir, log_name)
    # 日志格式
    log_fmt = '[1: %(asctime)s], [2: %(filename)s], [3: %(funcName)s], [4: %(levelname)s], [5: %(levelno)s], ' \
              '[6: %(lineno)d], [7: %(module)s], [8: %(message)s], [9: %(name)s], [10: %(process)d], ' \
              '[11: %(processName)s], [12: %(thread)d], [13: %(threadName)s]'

    # 使用basicConfig输出到文件
    # logging.basicConfig(level=level, format=log_fmt, filename=log_name)
    # log_instance = logging.getLogger(log_name)

    # 使用回滚模块RotatingFileHandler输出到文件
    log_file_handler = RotatingFileHandler(filename=log_name, maxBytes=102400, backupCount=5, encoding='utf-8')
    log_file_handler.setFormatter(logging.Formatter(log_fmt))  # 记录格式
    log_file_handler.setLevel(level)  # 记录等级
    log_instance = logging.getLogger(log_name)  # 创建日志对象
    log_instance.setLevel(level)    # 记录等级
    log_instance.addHandler(log_file_handler)  # 记录文件处理管理器

    # 输出到控制台
    print_consolse = logging.StreamHandler()  # sys.stdout or sys.stderr may be used.
    print_consolse.setFormatter(logging.Formatter(log_fmt))  # 记录格式
    print_consolse.setLevel(level)  # 记录等级
    # log_instance.addHandler(print_consolse)

    return log_instance


if __name__ == '__main__':
    log = log_init()
    log.info('info msg')
    log.warning('warning msg')
    log.error('error msg')
