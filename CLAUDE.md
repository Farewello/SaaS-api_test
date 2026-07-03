# SaaS API 接口自动化测试

这是基于 **pytest** + **数据驱动** 的 SaaS 接口自动化测试项目。

**完整项目说明 →** [`records/CLAUDE.md`](./records/CLAUDE.md)
**修改/需求记录 →** [`records/CHANGELOG.md`](./records/CHANGELOG.md)

### 结构速览

```
SaaS_api/                     ← 代码目录
    api_module/
        BaseApi.py            ← 核心基类（YAML 驱动 + 共享 Session）
        login.py / brand.py / topics.py
    common/
        global_env.py         ← 全局变量存储
        read_config.py        ← 配置读取
        log.py                ← 日志模块
    yaml_api/                 ← 接口定义（YAML + $模板变量）
    test_case/                ← pytest 测试用例
    conftest.py               ← session fixture（登录→品牌→清理）
    config/config.yaml        ← 环境配置
```

### 快速命令

```bash
cd SaaS_api && pytest -v       # 跑全部测试
pytest test_case/test_login.py  # 跑指定用例
python demo.py 726 753         # 批量删除知识库文件夹
```
