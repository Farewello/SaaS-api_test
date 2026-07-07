from api_module.BaseApi import BaseApi
from common.read_config import config_data
from common.global_env import set_env
from common.log import get_logger

logger = get_logger(__name__)


def login(phone=None, pwd=None):
    """登录并保存 token 和 merchantId"""
    phone = phone or config_data['base']['phone']
    pwd = pwd or config_data['base']['pwd']

    res = BaseApi().run_api('login.yaml', 'login', phone=phone, pwd=pwd)
    body = BaseApi.validate_response(res, label='登录')

    response_vo = body['responseVo']
    token = response_vo['token']
    BaseApi.session.headers['authorization'] = 'Bearer ' + token

    merchant_id = response_vo['merchantList'][0]['merchantId']
    set_env('merchant_id', merchant_id)
    logger.info(f'登录成功 | merchantId={merchant_id}')

    return response_vo


if __name__ == '__main__':
    login()
