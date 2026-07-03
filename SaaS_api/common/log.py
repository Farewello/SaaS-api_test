import logging
import os
import time


class Logger:
    def __init__(self, logger_name='SaaS', logger_level='DEBUG', stream_level='DEBUG', file_level='DEBUG'):
        # 1、创建日志记录器
        self.__logger = logging.getLogger(logger_name)
        # 2、设置日志记录器的日志等级（全局）
        self.__logger.setLevel(logger_level)
        # 3、创建日志格式器
        fmt = logging.Formatter('%(name)s - %(asctime)s - %(filename)s:[%(lineno)s] - [%(levelname)s] - %(message)s')
        # 4-1、创建控制台（流）处理器
        sh = logging.StreamHandler()
        # 5-1、设置控制台（流）处理器的日志等级
        sh.setLevel(stream_level)
        # 6-1、给控制台（流）处理器设置格式器
        sh.setFormatter(fmt)
        # 4-2、创建文件处理器
        # (1) 获取项目的根目录路径
        curr_file_abs_path = os.path.abspath(__file__)
        project_path = os.path.dirname(os.path.dirname(curr_file_abs_path))
        # (2) 创建logs日志目录（如果不存在）
        logs_dir_path = os.path.join(project_path, 'logs')
        if not os.path.exists(logs_dir_path):
            os.makedirs(logs_dir_path)
        # (3) 拼接完整的log日志文件的路径，日志文件名称以”年-月-日“的规则进行命名
        log_file_name = time.strftime('%Y-%m-%d') + '.log'
        log_file_path = os.path.join(logs_dir_path, log_file_name)
        fh = logging.FileHandler(filename=log_file_path, mode='a', encoding='utf-8')
        # 5-2、设置文件处理器的日志等级
        fh.setLevel(file_level)
        # 6-2、给文件处理器设置格式器
        fh.setFormatter(fmt)

        # 获取当前日志器里的处理器列表
        handlers_list = self.__logger.handlers
        # 如果处理器列表的长度等于0（即：尚未添加处理器）时，才会添加处理器，
        # 不写这一段，会出现“日志记录重复显示”的bug
        if len(handlers_list) == 0:
            # 7-1、将控制台（流）处理器添加到日志记录器
            self.__logger.addHandler(sh)
            # 7-2、将文件处理器添加到日志记录器
            self.__logger.addHandler(fh)

    # 将__logger对象属性私有化，写一个”对外方法“来获取__logger对象
    def get_logger(self):
        return self.__logger
