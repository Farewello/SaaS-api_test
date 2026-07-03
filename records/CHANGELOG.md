# Changelog

> 本文件记录每次功能新增 / 修复 / 重构 / 测试变更。
> 每条记录对应一次 Git commit + tag，回滚：`git checkout <tag>`。

## [2026-07-03] — v0.1.1

### Changed
- **BaseApi 核心重构**：新增 `_extract_template_vars()` + `SESSION_VAR_MAP` 机制，`run_api()` 自动从全局变量注入会话变量（merchantId / brandId），调用方无需手动 get_env + 传参
- **brand.py** 简化：移除手动 `get_env('merchant_id')` + merchantId 传参
- **topics.py** 简化：移除手动 merchantId / brandId 的取和传
- **demo.py** 简化：delete_kb_folder / list_kb_folders 签名去掉 merchantId / brandId 参数，自动注入

### Docs
- records/CLAUDE.md 更新：新增"会话变量自动注入"章节
- CLAUDE.md 快速命令更新

## [2026-07-03] — v0.1.0

### Added
- 基础框架搭建：BaseApi 数据驱动核心（YAML 模板替换 + 共享 Session）
- 登录接口（login.yaml + api_module/login.py）
- 品牌列表接口（brand.yaml + api_module/brand.py）
- 话题列表接口（topics.yaml + api_module/topics.py）
- 知识库文件夹创建接口（knowledge.yaml）
- 知识库文件夹删除接口（kb_delete.yaml + demo.py 批量删除脚本）
- pytest 集成：conftest.py session fixture（自动登录→获取品牌）
- 登录测试用例（test_case/test_login.py）
- 日志模块（common/log.py，控制台 + 文件按日切割）
- 配置读取模块（common/read_config.py）
- 全局变量存储（common/global_env.py）
- Faker 工具类（common/tools.py）
- 需求 / 修改记录体系搭建（records/CLAUDE.md + records/CHANGELOG.md）
- Git 版本控制初始化 + 首个 tag v0.1.0
