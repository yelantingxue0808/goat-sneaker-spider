"""
@Author  : 孔天宇
@Desc    : 
"""
from config import url_settings


def get_url():
    """
    获取当前所有的url存储到列表中
    """
    url_list = []
    for url_num in range(24, 793, 24):
        url_list.append(url_settings.URL.format(url_num))
    return url_list
