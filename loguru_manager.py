
from loguru import logger
from os import path

base_dir = "./logs"

config_dict = dict(
    rotation="0:00",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {thread.name} | {message}",
    retention="7 days",
    encoding="utf8",
)


# 按日志级别过滤
def filter_level(level):
    def fn(m):
        return m["level"] == level
    return fn


def loguru_config():
    # 注意：日志输出到当前的工作目录，请仔细确认
    logger.add(
        path.join(base_dir, "error_{time:YYYY-MM-DD}.log"),
        level="ERROR",
        filter=filter_level("ERROR"),
        **config_dict
    )
    logger.error('loguru_config_error')
    logger.add(
        path.join(base_dir, "warning_{time:YYYY-MM-DD}.log"),
        level="WARNING",
        filter=filter_level("WARNING"),
        **config_dict
    )
    logger.warning('loguru_config_warning')
    logger.add(
        path.join(base_dir, "info_{time:YYYY-MM-DD}.log"),
        level="INFO",
        filter=filter_level("INFO"),
        **config_dict
    )
    logger.info('loguru_config_info')
    logger.add(
        path.join(base_dir, "debug_{time:YYYY-MM-DD}.log"),
        level="DEBUG",
        filter=filter_level("DEBUG"),
        **config_dict
    )
    logger.debug("loguru_config_debug")


# 按平台名+日志级别过滤
def filter_key_and_level(key, level):
    def fn(m):
        return m["level"] == level and m["extra"].get("ext_key", "") == key
    return fn


def loguru_bind_platform(platform_name):
    log_path = path.join(base_dir, platform_name)
    logger.add(
        path.join(log_path, "error_{time:YYYY-MM-DD}.log"),
        level="ERROR",
        filter=filter_key_and_level(platform_name, "ERROR"),
        **config_dict
    )
    logger.error('loguru_config_error')
    logger.add(
        path.join(log_path, "warning_{time:YYYY-MM-DD}.log"),
        level="WARNING",
        filter=filter_key_and_level(platform_name, "WARNING"),
        **config_dict
    )
    logger.warning('loguru_config_warning')
    logger.add(
        path.join(log_path, "info_{time:YYYY-MM-DD}.log"),
        level="INFO",
        filter=filter_key_and_level(platform_name, "INFO"),
        **config_dict
    )
    logger.info('loguru_config_info')
    logger.add(
        path.join(log_path, "debug_{time:YYYY-MM-DD}.log"),
        level="DEBUG",
        filter=filter_key_and_level(platform_name, "DEBUG"),
        **config_dict
    )
    logger.debug("loguru_config_debug")
    return logger.bind(ext_key=platform_name)


if __name__ == '__main__':
    loguru_config()
