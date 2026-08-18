"""
@Author  : 孔天宇
@Desc    : 
"""
from config import settings
from multiprocessing import Process
from core import handler


def execute_task():
    """
    多进程+多线程存储数据
    """
    processes = []
    for _ in range(settings.PROCESS_NUM):
        process = Process(target=handler.task_process)
        process.start()
        processes.append(process)
    for pro in processes:
        pro.join()
