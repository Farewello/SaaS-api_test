---
name: saas-api-project
description: SaaS API 接口自动化测试项目 — 数据驱动框架，pytest + YAML
metadata:
  type: project
---

# SaaS API 接口自动化测试

基于 **pytest** + **数据驱动** 的 SaaS 接口自动化测试项目。

## 核心架构

```
YAML 定义层  (yaml_api/*.yaml)
     ↓  $模板变量 替换
BaseApi 核心  (api_module/BaseApi.py)
     ↓  requests.Session（共享 token）
API 封装层  (api_module/*.py)
     ↓  pytest
测试用例层  (test_case/*.py)
```

**执行流程**（conftest.py session fixture）：
1. `login()` → 取 token 注入 Session header，merchantId 存入全局变量
2. `get_brand_list()` → 取第一个品牌的 brandId 存入全局变量
3. 用例执行 → 从全局变量取 merchantId/brandId
4. `clear_env()` → 清理全局变量

## 关键文件

| 路径 | 用途 |
|---|---|
| `api_module/BaseApi.py` | 核心：共享 Session、YAML 模板替换(`$var`)、请求发送 |
| `api_module/login.py` | 登录：获取 token + merchantId |
| `api_module/brand.py` | 品牌列表：获取 brandId |
| `api_module/topics.py` | 话题列表查询 |
| `common/global_env.py` | 全局变量存储 (set_env/get_env/clear_env) |
| `common/read_config.py` | YAML 配置读取 + 项目根路径 |
| `common/log.py` | 日志（控制台 + 文件，按日切割） |
| `common/tools.py` | Faker 工具（手机号生成） |
| `conftest.py` | pytest session 级 fixture：登录→获取品牌→清理 |
| `test_case/test_login.py` | 登录成功测试用例 |
| `demo.py` | 批量删除知识库文件夹脚本 `python demo.py [start] [end]` |
| `config/config.yaml` | 环境配置（URL、超时、账号密码） |
| `yaml_api/*.yaml` | 接口定义（method、url、headers、body 模板） |

## 快速命令

```bash
# 运行全部测试
cd SaaS_api && python -m pytest -v

# 运行指定用例
python -m pytest test_case/test_login.py -v

# 运行带日志输出
python -m pytest -v -s

# 批量删除知识库文件夹
python demo.py 726 753
```

## 模板变量与会话变量自动注入

YAML 中用 `$varName` 占位，`BaseApi._substitute()` 递归替换：
- 纯模板变量 `$name` → 保留原始类型（int/str 等）
- 混合字符串 `prefix_$name` → 字符串级替换
- 值为 `null` 的字段自动过滤，不传给 requests

**会话变量自动注入：** 登录后固定的变量（`merchantId` / `brandId`）无需手动传入，
`run_api()` 自动从全局变量补全。定义在 `BaseApi.SESSION_VAR_MAP`：

| 模板变量 | global_env 键 | 来源 |
|---|---|---|
| `$merchantId` | `merchant_id` | login() 自动存入 |
| `$brandId` | `brand_id` | get_brand_list() 自动存入 |

调用方只需：`BaseApi().run_api('xxx.yaml', 'func_name')`，不再需要 `get_env()` + 传参。
显式传入 kwargs 时优先级高于自动注入，可按需覆盖。

## 添加新接口的标准步骤

1. 在 `yaml_api/` 下创建 YAML 文件或追加内容
2. 在 `api_module/` 下创建封装函数，调用 `BaseApi().run_api(yaml, func_name, **kwargs)`
3. 在 `test_case/` 下添加 pytest 测试用例
4. 更新本文件（records/CLAUDE.md）和 records/CHANGELOG.md

## 配置与环境

当前固定连接 `starfield-core-service.weimobqa.com`。
`config.yaml` 中已预留多环境切换（`APP_ENV` 环境变量），尚未实现。
