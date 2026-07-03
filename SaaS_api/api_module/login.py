import requests
from api_module.BaseApi import BaseApi
from common.read_config import config_data
from common.global_env import set_env
from common.log import Logger

logger = Logger().get_logger()


# 登录
def login(phone=None, pwd=None):
    """登录并保存 token 到全局 Session"""
    if phone is None:
        phone = config_data['base']['phone']
    if pwd is None:
        pwd = config_data['base']['pwd']

    res = BaseApi().run_api('login.yaml', 'login', phone=phone, pwd=pwd)

    # 防御性检查：HTTP 层面
    if res.status_code != 200:
        raise requests.RequestException(
            f'登录接口 HTTP 异常：status_code={res.status_code}'
        )

    body = res.json()

    # 防御性检查：业务层面
    if body.get('returnCode') != '000000' or body.get('processResult') is not True:
        logger.error(f'登录失败：{body.get("returnMsg", "未知错误")} (code={body.get("returnCode")})')
        raise ValueError(
            f'登录失败：{body.get("returnMsg", "未知错误")} (code={body.get("returnCode")})'
        )

    response = body['responseVo']
    token = response['token']
    BaseApi.session.headers['authorization'] = 'Bearer ' + token

    # 保存 merchantId 到全局变量（从 merchantList 第一个元素获取）
    merchant_list = response.get('merchantList', [])
    if not merchant_list:
        logger.warning('登录响应中 merchantList 为空，未设置 merchant_id')
    else:
        merchant_id = merchant_list[0]['merchantId']
        set_env('merchant_id', merchant_id)
        logger.info(f'登录成功，merchantId={merchant_id}')

    return res


if __name__ == '__main__':
    login()
