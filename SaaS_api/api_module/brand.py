from api_module.BaseApi import BaseApi
from common.global_env import set_env
from common.log import get_logger

logger = get_logger(__name__)


def get_brand_list():
    """获取当前商户的品牌列表，将 brandId 存入全局变量"""
    res = BaseApi().run_api('brand.yaml', 'get_brand_list')

    body = BaseApi.validate_response(res, label='品牌列表')

    response_vo = body.get('responseVo')
    if not response_vo:
        raise KeyError('品牌列表响应中缺失 responseVo')

    page_list = response_vo.get('pageList', [])
    if not page_list:
        logger.warning('品牌列表为空，未设置 brand_id')
    else:
        brand_id = page_list[0].get('brandId')
        if brand_id is not None:
            set_env('brand_id', brand_id)
            logger.info(f'获取品牌列表成功 | brandId={brand_id}, 共 {len(page_list)} 条')
        else:
            logger.warning('品牌列表元素中缺少 brandId')

    return response_vo


if __name__ == '__main__':
    get_brand_list()
