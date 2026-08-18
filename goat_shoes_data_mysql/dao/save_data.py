"""
@Author  : 孔天宇
@Desc    : 
"""
from utils import logger
import pymysql


def save_data_mysql(item_list, process_id):
    # 连接mysql数据库
    connection = pymysql.connect(host='localhost', user='root', password='123456', database='text3')
    cursor = connection.cursor()
    count = 0
    try:
        logger.get_logger().info(f'进程{process_id}准备将数据保存到mysql中。。。')
        for goods_dic in item_list:
            sku = goods_dic['商品货号']
            size_option = goods_dic["商品尺寸"]
            amount = goods_dic['商品价格']
            sql_insert = "insert into goat_goods(商品货号,商品尺寸,商品价格) values(%s,%s,%s)"
            cursor.execute(sql_insert, (sku, size_option, amount))
            count += 1
        logger.get_logger().info(f'进程{process_id}保存{count}个数据到mysql')
        # 提交事务
        connection.commit()
    except Exception as error:
        logger.get_logger().warning('数据保存发生异常：', error)
        # 回滚事务
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
