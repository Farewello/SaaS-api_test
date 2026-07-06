import pytest
from api_module.login import login
from api_module.brand import get_brand_list
from common.global_env import get_env, clear_env
from common.read_config import config_data
from common.log import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="session")
def brand_env():
    """登录并获取品牌列表，返回 merchant_id / brand_id（session 级）。"""
    logger.info('[Fixture brand_env] 登录初始化...')
    login(phone=config_data['base']['phone'], pwd=config_data['base']['pwd'])
    get_brand_list()

    result = {
        'merchant_id': get_env('merchant_id'),
        'brand_id': get_env('brand_id'),
    }
    logger.info(f'[Fixture brand_env] 初始化完成 | merchant_id={result["merchant_id"]}, brand_id={result["brand_id"]}')

    yield result

    logger.info('[Fixture brand_env] 清理全局变量')
    clear_env()
