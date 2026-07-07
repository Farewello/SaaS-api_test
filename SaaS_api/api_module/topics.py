from api_module.BaseApi import BaseApi
from common.global_env import set_env
from common.log import get_logger

logger = get_logger(__name__)


def get_topics_page_list():
    """查询当前商家品牌的话题列表"""
    res = BaseApi().run_api('topics.yaml', 'get_topics_page_list')
    body = BaseApi.validate_response(res, label='话题列表')
    response_vo = body['responseVo']
    logger.info(f'获取话题列表成功 | 共 {len(response_vo.get("pageList", []))} 条')
    return response_vo


def topics_save(text):
    """创建话题，查列表拿到 topicId 并存入全局变量，返回 topicId"""
    res = BaseApi().run_api('topics.yaml', 'topics_save', text=text)
    BaseApi.validate_response(res, label='创建话题')
    logger.info(f'创建话题 "{text}" 成功')

    page = get_topics_page_list()
    topic_id = page['pageList'][0]['topicId']
    set_env('topic_id', topic_id)
    logger.info(f'存入全局变量 topicId={topic_id}')

    return topic_id


def topics_change_status(topicId, status):
    """禁用/启用话题。topicId 和 status 都必须显式传入。"""
    res = BaseApi().run_api('topics.yaml', 'topics_change_status',
                            topicId=topicId, status=status)
    BaseApi.validate_response(res, label='话题状态变更')
    logger.info(f'话题 {topicId} 状态变更为 {status}')


def topics_delete(topicIds):
    """topicIds 传入列表，如 [20981, 20982]；也兼容传单值，内部自动转列表"""
    if not isinstance(topicIds, list):  # ← 加在这里
        topicIds = [topicIds]
    res = BaseApi().run_api('topics.yaml', 'topics_delete', topicIds=topicIds)
    BaseApi.validate_response(res, label='话题删除')
    logger.info(f'话题 {topicIds} 删除成功')

if __name__ == '__main__':
    from api_module.login import login
    from api_module.brand import get_brand_list
    login()
    get_brand_list()
    tid = topics_save('测试话题')
    topics_change_status(topicId=tid, status=0)
    topics_delete(topicIds=tid)