"""
@Author  : 孔天宇
@Desc    : 
"""
from config import settings
from multiprocessing import Process
from core import handler

def execute_task():
    # 创建3个进程每个进程将10个url分为一组解析并保存数据
    processes = []
    for _ in range(settings.PROCESS_NUM):
        process = Process(target=handler.task_process)
        processes.append(process)
        process.start()

    for pro in processes:
        # 阻塞等待所有子进程
        pro.join()