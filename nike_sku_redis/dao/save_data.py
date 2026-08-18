"""
@Author  : 孔天宇
@Desc    : 
"""
from redis import StrictRedis
from utils import logger
from multiprocessing import current_process


def save_data_redis(sku_data):
    try:
        r = StrictRedis(host="localhost", db=2, password="123456", decode_responses=True)
        sku_count = 0
        for sku in sku_data:
            r.sadd("sku", sku)
            sku_count += 1
        logger.get_logger().info(f"进程{int(current_process().name.split('-')[-1])}保存到redis中的货号总计：{sku_count}件，累计"
                                 f"{r.scard('sku')}")

        r.close()
    except Exception as e:
        logger.get_logger().info(f'redis连接失败，报错内容为：{e}')
