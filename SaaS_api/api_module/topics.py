import requests
from api_module.BaseApi import BaseApi
from common.log import Logger

logger = Logger().get_logger()


# 查询话题列表
def get_topic_pageList():
    """查询当前商家品牌的话题列表"""
    res = BaseApi().run_api('topics.yaml', 'get_topic_pageList')

    if res.status_code != 200:
        raise requests.RequestException(
            f'话题列表接口 HTTP 异常：status_code={res.status_code}'
        )

    return res


if __name__ == '__main__':
    from api_module.login import login
    from api_module.brand import get_brand_list
    login()
    get_brand_list()
    result = get_topic_pageList()
    logger.info(f'话题列表响应：{result.text}')
