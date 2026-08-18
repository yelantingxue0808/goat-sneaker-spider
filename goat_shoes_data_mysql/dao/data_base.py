"""
@Author  : 孔天宇
@Desc    : 
"""
from redis import StrictRedis
from utils import logger


def connect_redis():
    try:
        r = StrictRedis(host="localhost", db=2, password='123456', decode_responses=True)
        return r
    except Exception as e:
        logger.get_logger().info(f'redis连接失败{e}')
