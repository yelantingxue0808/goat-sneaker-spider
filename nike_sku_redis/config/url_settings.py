"""
@Author  : 孔天宇
@Desc    : 
"""
# goat_url
URL = 'https://api.nike.com.cn/discover/product_wall/v1/marketplace/CN/language/zh-Hans/consumerChannelId/' \
      'd9a5bc42-4b9c-4976-858a-f159cf99c647?path=/w/mens-shoes-nik1zy7ok&attributeIds=16633190-45e5-4830-a068-232ac' \
      '7aea82c,0f64ecc7-d624-4e91-b171-b83a03dd8550&queryType=PRODUCTS&anchor={}&count=24'

COOKIES = {
    'geoloc': 'cc=CN',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2219f1dff84af23f-0120729ede13ce4-26061051-2520156-19f1dff84b0284b%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTlmMWRmZjg0YWYyM2YtMDEyMDcyOWVkZTEzY2U0LTI2MDYxMDUxLTI1MjAxNTYtMTlmMWRmZjg0YjAyODRiIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D',
    'ni_pp': 'pdp|nikecom>pdp>nike%20air%20force%201%20low%20by%20%E5%A4%A7%E8%BF%9E%E8%8B%B1%E5%8D%9A',
    'ni_cs': 'b1786576-3cf3-412e-bf7a-3a1ac67dffd7',
    'cdn_sec_tc': '701dd19717845270641152652e239c47130d6e365f48b1ee5b3f4484c2',
    'acw_tc': '2760821117845270641585250e3069c704567101adf2d36c26213e5e03e955',
    'sensorsdata2015jssdksession': '%7B%22session_id%22%3A%2219f7e05f7833f6094382fc231dd9826061051252015619f7e05f7841fc0%22%2C%22first_session_time%22%3A1784525748099%2C%22latest_session_time%22%3A1784527092500%7D',
    'ssxmod_itna': '1-YqAxuDgGqDw2GkDhx_xxQw4YMzx9DGuPi=DzxC5iOD_xQvK08D6QDB_r=PAFoPeYhrqG0D2Y3h3=GbNDlr2eDZDGIQDqx0EbRYD_rNNeNzlgieQH_lEP3=TMEohs=Oiy=P1LNsH=zRcchxhfxmPKg53K0eY3xGLDY=DCuGxSEbD44dDt4DIDAYDDxDW04DLDYoDYSndxGPi=aaFxauWD0YDzqDgD7jWDPDEDG3D04W470qKKpxD0wxAO7DiDODDbxnWsWyWBPDSQYalDPDM8xGXKglpxDtnavhHT=CljUo=2PHDtqD9/ZnY2L8Qf76fdO6biEIiEblpEa_rleqAqeGQqBx4AmrQ4iBhxGDYmr3C2rGG_AYenwKfRXDGIDu3VR4Dro0y/l5ADADdx=NiTB7eoTk/_xG0DW9Y4xebOplxie4eADqADxf3eaDK=fiShqTEbK04PqxQErh0TGYddr3pxT/4qeD',
    'ssxmod_itna2': '1-YqAxuDgGqDw2GkDhx_xxQw4YMzx9DGuPi=DzxC5iOD_xQvK08D6QDB_r=PAFoPeYhrqG0D2Y3h3=GboD=a3YYIKOD7PdWKBE8W3DBkLQqKf87GH3ap=4WguWj3wi8uzrA9D14z5AI4hRQGNcKDh6R_hxPLALl0qnWq0GWCER9dt4/EfxKxxYpxUniY2neThKoa66YB=cQfQNMTtKjR4T7AmC21HpSgvGK3W4KUez=FD',
}

HEADERS = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'anonymousid': 'unknown-anonymousid',
    'cache-control': 'no-cache',
    'nike-api-caller-id': 'nike:dotcom:browse:wall.client:2.0',
    'origin': 'https://www.nike.com.cn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.nike.com.cn/',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    # 'cookie': 'geoloc=cc=CN; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219f1dff84af23f-0120729ede13ce4-26061051-2520156-19f1dff84b0284b%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTlmMWRmZjg0YWYyM2YtMDEyMDcyOWVkZTEzY2U0LTI2MDYxMDUxLTI1MjAxNTYtMTlmMWRmZjg0YjAyODRiIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D; ni_pp=pdp|nikecom>pdp>nike%20air%20force%201%20low%20by%20%E5%A4%A7%E8%BF%9E%E8%8B%B1%E5%8D%9A; ni_cs=b1786576-3cf3-412e-bf7a-3a1ac67dffd7; cdn_sec_tc=701dd19717845270641152652e239c47130d6e365f48b1ee5b3f4484c2; acw_tc=2760821117845270641585250e3069c704567101adf2d36c26213e5e03e955; sensorsdata2015jssdksession=%7B%22session_id%22%3A%2219f7e05f7833f6094382fc231dd9826061051252015619f7e05f7841fc0%22%2C%22first_session_time%22%3A1784525748099%2C%22latest_session_time%22%3A1784527092500%7D; ssxmod_itna=1-YqAxuDgGqDw2GkDhx_xxQw4YMzx9DGuPi=DzxC5iOD_xQvK08D6QDB_r=PAFoPeYhrqG0D2Y3h3O_4D/A74GzDiTKGhDBWoOeD2Av5_5NSCY43pKixETd=TXIDwxQOivgkij=sH659wLudY3xGLDY=DCuGxShrD4S3Dt4DIDAYDDxDWU4DLDYoDYRT5xGpdMQnrXQRWD0YDzqDgD7jWUeDEDG3D0SRBlGx=ODDl707gDxmxDYpdxc07TOFDAuDiaMbDjLPD/8eUqKDBS/kKQPWLakOI_lcHxBQD7uFNrC98near1CgbFmEPa4XQDiAev7D1GGB7DNiDnQ_rD4NQDeDx5bxKt4eWmxA2zY0NSPDneYZ_HFixk5lIypfyZ3rxNDT_BYIOT8_HQDeKD0KrYGD4/AND_iY44IYqa_48BtPbNK7iruCnoqKxx9BthGTWbYdrip2OQEDD; ssxmod_itna2=1-YqAxuDgGqDw2GkDhx_xxQw4YMzx9DGuPi=DzxC5iOD_xQvK08D6QDB_r=PAFoPeYhrqG0D2Y3h3O4iTp7WRonANsbEyXGqdSOGxNTxuiD',
}
