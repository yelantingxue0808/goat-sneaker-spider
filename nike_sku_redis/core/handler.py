"""
@Author  : 孔天宇
@Desc    : 
"""
import json
import random
import time
import requests
from multiprocessing import current_process
from config import url_settings,settings
from utils import utils, logger
from dao import save_data

def parse_data(url_data):
    """
    将每个url发送给服务器，服务器返回数据并对数据进行处理
    """
    # 获取数据
    sku_list = []
    for url in url_data:
        session = requests.Session()
        time.sleep(random.uniform(2, 5))
        response = session.get(
            url=url,
            cookies=url_settings.COOKIES,
            headers=url_settings.HEADERS,
        )
        resp_data = response.text
        resp_data = json.loads(resp_data)
        for productGroup in resp_data.get("productGroupings", []):
            for product in productGroup.get('products', []):
                sku = product.get('productCode', '')
                # 将所有的sku保存到列表中
                sku_list.append(sku)
    return sku_list


def task_process():
    """
    提取url,解析数据，保存数据在
    """
    process_id = int(current_process().name.split('-')[-1])
    for index in range(0, 33, 10):
        # 每10个url为一组可以组成的组数
        group_num = (index // 10) + 1
        if process_id % settings.PROCESS_NUM == group_num % settings.PROCESS_NUM:
            url_list = utils.get_url()[index:index + 10]
            sku_data = parse_data(url_list)
            logger.get_logger().info(f'进程{process_id}解析处理的url范围是{index}~{index + 10}')
            logger.get_logger().info(f'进程{process_id}处理的数据有{len(sku_data)}个数据为：{sku_data}')
            # 4个进程解析完成的商品货号保存到redis集合中，保证唯一性和去重
            return save_data.save_data_redis(sku_data)
