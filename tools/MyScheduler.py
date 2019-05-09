# 这里是单个模块文件。
from flask_apscheduler import APScheduler


class myScheduler(APScheduler):

    """
    修改为单例模式，解决出现启动flask时，任务被执行两次的问题。

    """

    def __new__(cls, *args, **kwargs):
        """
        实现单例模式
        :param args:
        :param kwargs:
        :return:
        """

        if not hasattr(cls, '_instance'):

            cls._instance = super().__new__(cls)

        return cls._instance


