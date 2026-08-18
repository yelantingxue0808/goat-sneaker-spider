"""
@Author  : 孔天宇
@Desc    : 
"""
from concurrent.futures import ThreadPoolExecutor, wait,as_completed
from core import handler


def batch_thread(params):
    """
    多线程发送url并解析数据,每个线程处理未知个参数，并进行解析
    """
    thread_pool = ThreadPoolExecutor(6)
    tasks = []
    # 每step个为一组,
    step = len(params) // 6
    if step == 0:
        step = 1  # 数据少于6个时，每组至少1个
    for index in range(0, len(params), step):
        params_list = params[index:index + step]
        task = thread_pool.submit(handler.parse_data, params_list)
        tasks.append(task)
    # 等待所有任务完成（阻塞等待）
    wait(tasks)

    item_list = []
    # 获取返回值
    for data in as_completed(tasks):
        item_list.extend(data.result())
    return item_list
