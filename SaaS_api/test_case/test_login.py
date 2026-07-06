from api_module.login import login
from common.global_env import get_env


def test_login_success():
    """正常登录：走 login.py 默认配置，token 和 merchant_id 正确写入"""
    response_vo = login()

    assert response_vo['token'] is not None
    assert get_env('merchant_id') is not None
