import pytest
from api_module.login import login
from api_module.brand import get_brand_list
from common.global_env import clear_env
from common.read_config import config_data


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown():
    """整个测试会话：登录 → 获取品牌 → 测试 → 清理"""
    login(phone=config_data['base']['phone'], pwd=config_data['base']['pwd'])
    get_brand_list()
    yield
    clear_env()       # 测试后：清理全局变量
