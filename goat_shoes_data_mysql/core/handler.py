"""
@Author  : 孔天宇
@Desc    : 
"""
import random
import time

import curl_cffi
from curl_cffi import requests
from multiprocessing import Process, current_process
from config import url_settings, url_template_id_settings
from utils import logger, utils
from dao import save_data, data_base


def parse_data(params_list):
    goods_list = []
    # 一个线程复用同一个Session
    session = requests.Session(impersonate="chrome124")
    for url_params in params_list:
        time.sleep(random.random())
        sku_data = url_params['sku']
        PARAM = url_params['params']

        try:
            response = session.get(
                'https://www.goat.com/web-api/v1/product_variants/buy_bar_data',
                params=PARAM,
                cookies=url_settings.COOKIES,
                headers=url_settings.HEADERS,
                timeout=10  # 加上超时，防止卡住
            )

            # print(response.status_code)
            # pprint.pprint(response.json())
            response_data = response.json()

            for data in response_data:
                goods_dic = {}
                size_option = data.get('sizeOption', {}).get('value', '')
                amount = data.get("lowestPriceCents", {}).get('amount', '') / 100
                goods_dic['商品货号'] = sku_data
                goods_dic["商品尺寸"] = size_option
                goods_dic['商品价格'] = amount
                goods_list.append(goods_dic)
                logger.get_logger().info(f'{goods_dic}提取完成')
            logger.get_logger().info(f'货号{sku_data}提取完成，共{len(response_data)}个尺码')
        except Exception as e:
            logger.get_logger().info(f'货号{sku_data}解析失败: {e}')
            # 单个sku失败不影响整体，跳过继续
            continue
    return goods_list


def parse_goods_id(sku):
    """
    通过redis中获取到的sku货来获取商品的唯一id号
    (也就是通过sku映射该球鞋的唯一id号)
    """
    url_template_id_settings.PARAMS['queryString'] = sku
    response = curl_cffi.get(
        'https://www.goat.com/web-api/consumer-search/get-product-search-results',
        params=url_template_id_settings.PARAMS,
        cookies=url_template_id_settings.COOKIES,
        headers=url_template_id_settings.HEADERS,
        impersonate='chrome124'
    )
    # 控制货号
    # 获取product_template_id
    try:
        json_data = response.json()
        template_id = json_data.get('data', {}).get('productsList', [])[0].get('id', "")
        return template_id
    except Exception as e:
        print(f'生成商品的id出现异常:{e}')
        return None


def task_process():
    """
    每个子进程执行的任务
    生成商品id,通过商品id发送url，解析数据，保存数据到mysql中
    """
    # redis是有状态的,连接数据库
    r = data_base.connect_redis()
    sku_count = 0  # 统计当前进程从Redis取出的sku总数
    url_sku_params = []  # 存放构造好的请求参数（sku+productTemplateId）
    process_id = int(current_process().name.split('-')[-1])  # 获取进程编号（比如Process-1取1）

    # 2. 核心循环：直到Redis的sku集合为空，才停止弹出（每个进程会循环弹出redis中的sku）
    while True:
        if r.scard('sku'):
            sku_params = {}
            sku_data = r.spop('sku')  # 原子弹出，多进程不会重复取同一个sku
            product_id = parse_goods_id(sku=sku_data)
            if product_id is not None:
                url_settings.PARAMS['productTemplateId'] = product_id
                sku_params['sku'] = sku_data
                sku_params['params'] = url_settings.PARAMS
                url_sku_params.append(sku_params)
            sku_count += 1
        else:
            logger.get_logger().info(f'进程{process_id}，从redis中取出{sku_count}个数据,有{len(url_sku_params)}个字典参数')
            break

    item_list = utils.batch_thread(url_sku_params)
    logger.get_logger().info(f'进程{process_id}将有{len(item_list)}条解析完成的数据存放到mysql中')
    logger.get_logger().info(f'进程{process_id}准备存放的数据为{item_list}')
    return save_data.save_data_mysql(item_list, process_id)
