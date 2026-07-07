from api_module.BaseApi import BaseApi
from common.log import get_logger

logger = get_logger(__name__)


def get_prompts_page_list():
    """查询当前商家品牌的场景问题列表"""
    res = BaseApi().run_api('prompts.yaml', 'get_prompts_page_list')
    body = BaseApi.validate_response(res, label='场景问题列表')
    response_vo = body['responseVo']
    logger.info(f'获取场景问题列表成功 | 共 {len(response_vo.get("pageList", []))} 条')
    return response_vo


def prompts_save(topicId, prompts):
    """创建场景问题。topicId 必须显式传入，prompts 支持列表或单值。"""
    if not isinstance(prompts, list):
        prompts = [prompts]
    res = BaseApi().run_api('prompts.yaml', 'prompts_save',
                            topicId=topicId, prompts=prompts)
    BaseApi.validate_response(res, label='创建场景问题')
    logger.info(f'场景问题创建成功 | topicId={topicId}')


if __name__ == '__main__':
    from api_module.login import login
    from api_module.brand import get_brand_list
    from api_module.topics import topics_save
    login()
    get_brand_list()
    tid = topics_save('场景子A')
    prompts_save(topicId=tid, prompts=["知识库中搜索相关数据时为什么排序不对", "机器人回复内容包含特殊字符"])
