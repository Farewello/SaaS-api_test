import pytest
from api_module.login import login
from api_module.brand import get_brand_list
from api_module.topics import topics_save, get_topics_pageList
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


@pytest.fixture
def topic_id(brand_env):
    """创建一个话题，返回 topicId，存入全局变量，测试后清理 topic_id。"""
    tid = topics_save("测试话题-自动化")
    yield tid
    clear_env('topic_id')
