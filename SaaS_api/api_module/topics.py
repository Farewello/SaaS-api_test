import requests
from api_module.BaseApi import BaseApi
from api_module.brand import get_brand_list
from api_module.login import login
from common.global_env import get_env
from common.log import Logger

logger = Logger().get_logger()


# 查询话题列表
def get_topic_pageList():
    """查询当前商家品牌的话题列表"""
    merchant_id = get_env('merchant_id')
    brand_id = get_env('brand_id')

    if merchant_id is None:
        raise ValueError('merchant_id 未设置，请先调用 login()')
    if brand_id is None:
        raise ValueError('brand_id 未设置，请先调用 get_brand_list()')

    res = BaseApi().run_api(
        'topics.yaml', 'get_topic_pageList',
        merchantId=merchant_id,
        brandId=brand_id,
    )

    if res.status_code != 200:
        raise requests.RequestException(
            f'话题列表接口 HTTP 异常：status_code={res.status_code}'
        )

    return res


if __name__ == '__main__':
    login()
    get_brand_list()
    result = get_topic_pageList()
    logger.info(f'话题列表响应：{result.text}')
