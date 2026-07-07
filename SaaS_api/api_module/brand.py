from api_module.BaseApi import BaseApi
from common.global_env import set_env
from common.log import get_logger

logger = get_logger(__name__)


def get_brand_list():
    """获取当前商户的品牌列表，将 brandId 存入全局变量"""
    res = BaseApi().run_api('brand.yaml', 'get_brand_list')
    body = BaseApi.validate_response(res, label='品牌列表')

    response_vo = body['responseVo']
    page_list = response_vo.get('pageList', [])
    if page_list:
        brand_id = page_list[0]['brandId']
        set_env('brand_id', brand_id)
        logger.info(f'获取品牌列表成功 | 存入全局变量 brandId={brand_id}')

    return response_vo


if __name__ == '__main__':
    from api_module.login import login
    login()
    get_brand_list()
