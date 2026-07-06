import os
import requests
import yaml
import re
from string import Template
from common.read_config import config_data, project_root_path
from common.global_env import get_env
from common.log import get_logger
import time as _time

logger = get_logger(__name__)


class BaseApi:
    """API 请求基类 — 共享 Session、YAML 数据驱动、会话变量自动注入"""

    session = requests.Session()

    # 会话变量映射表：YAML 模板变量 → global_env 存储键
    # 这些变量登录/初始化后不再变化，调用 run_api 时无需手动传入
    SESSION_VAR_MAP = {
        'merchantId': 'merchant_id',
        'brandId': 'brand_id',
    }

    @staticmethod
    def _extract_template_vars(data):
        """递归提取字典/列表/字符串中所有的 $var 模板变量名"""
        vars_set = set()
        if isinstance(data, str):
            for m in re.finditer(r'\$(\w+)', data):
                vars_set.add(m.group(1))
        elif isinstance(data, dict):
            for v in data.values():
                vars_set.update(BaseApi._extract_template_vars(v))
        elif isinstance(data, list):
            for item in data:
                vars_set.update(BaseApi._extract_template_vars(item))
        return vars_set

    @staticmethod
    def _substitute(data, mapping):
        """递归替换字典/列表中的 $var 模板变量，保留原始类型。

        - 若值是纯模板变量 ``$name``，直接返回 ``mapping["name"]``（保留类型）
        - 若值是含模板的混合字符串 ``prefix_$name``，做字符串级替换（返回 str）
        - 非 str / dict / list 类型原样返回
        """
        if isinstance(data, str):
            if data.startswith('$') and data[1:] in mapping:
                return mapping[data[1:]]
            return Template(data).safe_substitute(mapping)
        if isinstance(data, dict):
            return {k: BaseApi._substitute(v, mapping) for k, v in data.items()}
        if isinstance(data, list):
            return [BaseApi._substitute(v, mapping) for v in data]
        return data

    @staticmethod
    def validate_response(res, *, label='响应', expect_code='000000'):
        """统一校验 HTTP 状态码 + JSON 合法性 + 业务 returnCode。

        Args:
            res: requests.Response 对象
            label: 接口中文描述（用于报错信息，如"登录"、"品牌列表"）
            expect_code: 期望的业务 returnCode，默认 '000000'

        Returns:
            dict: 解析后的 response body（已验证 returnCode 正确）

        Raises:
            requests.RequestException: HTTP 状态码异常
            ValueError: JSON 解析失败 or 业务码不符合预期
        """
        if res.status_code != 200:
            raise requests.RequestException(
                f'{label}接口 HTTP 异常：status_code={res.status_code}'
            )

        try:
            body = res.json()
        except ValueError as e:
            raise ValueError(f'{label}响应不是合法 JSON：{e}')

        return_code = body.get('returnCode')
        if return_code != expect_code:
            err_msg = body.get('returnMsg', '未知错误')
            raise ValueError(
                f'{label}失败：{err_msg} (code={return_code})'
            )

        return body

    def send_request(self, method, url, headers=None, params=None, data=None, json=None, files=None):
        """发送 HTTP 请求"""
        base_url = config_data['base']['url'] + '/'
        full_url = base_url + url.lstrip('/')

        merged_headers = dict(self.session.headers)
        if headers:
            merged_headers.update(headers)

        # DEBUG：完整的 URL、请求细节（仅文件）
        logger.debug(
            f"\n\t完整地址：{full_url}"
            f"\n\t请求 headers：{merged_headers}"
            f"\n\t请求 json：{json}"
            f"\n\t请求 data：{data}"
        )

        start = _time.perf_counter()
        try:
            res = self.session.request(
                method=method, url=full_url,
                headers=merged_headers,
                json=json, data=data,
                params=params, files=files,
                timeout=config_data['base'].get('timeout', 10),
            )
            elapsed = _time.perf_counter() - start

            logger.info(f"{method} /{url.lstrip('/')} → {res.status_code} ({elapsed:.3f}s)")
            logger.debug(
                f"\n\t响应文本：{res.text[:2000]}"
                f"{' …(truncated)' if len(res.text) > 2000 else ''}"
            )
            return res
        except requests.RequestException as e:
            elapsed = _time.perf_counter() - start
            logger.error(f"{method} /{url.lstrip('/')} → FAILED ({elapsed:.3f}s): {e}")
            raise

    def run_api(self, yaml_name, func_name, **kwargs):
        """读取 YAML 定义并发送请求，支持模板变量替换。

        自动注入 SESSION_VAR_MAP 中的会话变量（如 merchantId / brandId），
        优先使用 kwargs 传入的值，缺失时自动从全局变量补全。
        调用方无需手动 get_env() + 传参。
        """
        yaml_full_path = os.path.join(project_root_path, 'yaml_api', yaml_name)

        with open(yaml_full_path, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)

        api_data = yaml_data[func_name]

        # 自动注入会话变量：从 YAML 中提取所有 $var 模板变量名，
        # 如果 kwargs 中缺失且存在于 SESSION_VAR_MAP，则从 global_env 补全
        for var_name in self._extract_template_vars(api_data):
            if var_name not in kwargs and var_name in self.SESSION_VAR_MAP:
                env_val = get_env(self.SESSION_VAR_MAP[var_name])
                if env_val is not None:
                    kwargs[var_name] = env_val

        # 模板变量替换
        if kwargs:
            api_data = self._substitute(api_data, kwargs)

        # 过滤掉值为 None 的字段（避免传给 requests 的参数含 None）
        api_data = {k: v for k, v in api_data.items() if v is not None}

        return self.send_request(**api_data)
