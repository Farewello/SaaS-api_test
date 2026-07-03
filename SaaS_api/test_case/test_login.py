
from api_module.login import login
from common.read_config import config_data
from common.global_env import get_env


class TestLogin:
    def test_login_success(self):
        """测试登录是否成功"""
        res = login(phone=config_data['base']['phone'], pwd=config_data['base']['pwd'])
        response = res.json()

        # 验证登录成功
        assert res.status_code == 200
        assert response['returnCode'] == '000000'
        assert response['processResult'] is True
        assert response['responseVo']['token'] is not None

        # 验证 merchant_id 已保存
        assert get_env('merchant_id') is not None
