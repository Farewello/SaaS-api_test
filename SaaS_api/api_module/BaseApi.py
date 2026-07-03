import os
import requests
import yaml
from string import Template
from common.read_config import config_data, project_root_path
from common.log import Logger

logger = Logger().get_logger()


class BaseApi:
    """API 请求基类 — 共享 Session、YAML 数据驱动"""

    session = requests.Session()

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

    def send_request(self, method, url, headers=None, params=None, data=None, json=None, files=None):
        """发送 HTTP 请求"""
        # 拼接完整 URL，处理首尾斜杠
        base_url = config_data['base']['url'] + '/'
        full_url = base_url + url.lstrip('/')

        # 合并 session.headers 和当前请求的 headers
        merged_headers = dict(self.session.headers)
        if headers:
            merged_headers.update(headers)

        logger.info(
            f"\n\t请求方式：{method},\n\t请求地址：{full_url},\n\t请求 params：{params},"
            f"\n\t请求 headers：{merged_headers},\n\t请求 json：{json},\n\t请求 data：{data}"
        )

        try:
            res = self.session.request(
                method=method,
                url=full_url,
                headers=merged_headers,
                json=json,
                data=data,
                params=params,
                files=files,
            )
            logger.info(
                f"\n\t响应状态码：{res.status_code},\n\t响应文本：{res.text}"
            )
            return res
        except requests.RequestException as e:
            logger.error(f"请求失败：{e}")
            raise

    def run_api(self, yaml_path, func_name, **kwargs):
        """读取 YAML 定义并发送请求，支持模板变量替换。"""
        yaml_full_path = os.path.join(project_root_path, 'yaml_api', yaml_path)

        with open(yaml_full_path, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)

        api_data = yaml_data[func_name]

        # 模板变量替换
        if kwargs:
            api_data = self._substitute(api_data, kwargs)

        # 过滤掉值为 None 的字段（避免传给 requests 的参数含 None）
        api_data = {k: v for k, v in api_data.items() if v is not None}

        return self.send_request(**api_data)
