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

    response_vo = body.get('responseVo') or {}
    token = response_vo.get('token')
    if not token:
        raise KeyError('登录响应中缺失 token')

    BaseApi.session.headers['authorization'] = 'Bearer ' + token

    # 提取并保存 merchantId
    merchant_id = (response_vo.get('merchantList') or [{}])[0].get('merchantId')
    if merchant_id:
        set_env('merchant_id', merchant_id)
        logger.info(f'登录成功 | merchantId={merchant_id}')
    else:
        logger.warning('merchantList 为空或缺少 merchantId')

    return response_vo


if __name__ == '__main__':
    login()
