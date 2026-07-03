import requests
from api_module.BaseApi import BaseApi
from common.global_env import set_env
from common.log import Logger

logger = Logger().get_logger()


# 获取品牌列表并保存 brandId
def get_brand_list():
    """获取当前商户的品牌列表，并将第一个 brandId 存入全局变量"""
    res = BaseApi().run_api('brand.yaml', 'get_brand_list')

    if res.status_code != 200:
        raise requests.RequestException(
            f'品牌列表接口 HTTP 异常：status_code={res.status_code}'
        )

    body = res.json()
    if body.get('returnCode') != '000000':
        logger.error(f'获取品牌列表失败：{body.get("returnMsg", "未知错误")}')
        raise ValueError(
            f'获取品牌列表失败：{body.get("returnMsg", "未知错误")}'
        )

    page_list = body.get('responseVo', {}).get('pageList', [])
    if not page_list:
        logger.warning('品牌列表为空，未设置 brand_id')
    else:
        brand_id = page_list[0]['brandId']
        set_env('brand_id', brand_id)
        logger.info(f'获取品牌列表成功，brandId={brand_id}')

    return res


if __name__ == '__main__':
    get_brand_list()
