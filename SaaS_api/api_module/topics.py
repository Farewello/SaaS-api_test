from api_module.BaseApi import BaseApi


# 查询话题列表
def get_topic_pageList():
    """查询当前商家品牌的话题列表

    Returns:
        dict: 话题列表的 responseVo 对象

    Raises:
        requests.RequestException: HTTP 层面异常
        ValueError: 业务层面异常或 JSON 解析失败
    """
    res = BaseApi().run_api('topics.yaml', 'get_topic_pageList')

    body = BaseApi.validate_response(res, label='话题列表')

    response_vo = body.get('responseVo')
    if not response_vo:
        raise KeyError('话题列表响应中缺失 responseVo')

    return response_vo


if __name__ == '__main__':
    from api_module.login import login
    from api_module.brand import get_brand_list
    login()
    get_brand_list()
    result = get_topic_pageList()
    from common.log import get_logger
    logger = get_logger(__name__)
    logger.info(f'获取话题列表成功 | 共 {len(result.get("pageList", []))} 条')
