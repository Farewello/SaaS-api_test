"""
日志模块 — 类封装命名 logger，环境变量覆盖等级。

用法：
    from common.log import get_logger
    logger = get_logger(__name__)

环境变量：
    LOG_LEVEL       = DEBUG / INFO / WARNING / ERROR   全局级别（默认 DEBUG）
    LOG_STREAM_LEVEL= DEBUG / INFO / WARNING / ERROR   控制台级别（默认 INFO）
    LOG_FILE_LEVEL  = DEBUG / INFO / WARNING / ERROR   文件级别（默认 DEBUG）

控制台策略：
  普通运行 → 自己配 StreamHandler → stdout
  pytest 运行 → 由 pytest live_logs（--log-cli-level）接管，不额外配控制台 handler
文件策略：
  始终写入 logs/YYYY-MM-DD.log，每日分割，永久保留
"""
import logging
import os
import sys
import time


# ── 内部缓存 ────────────────────────────────────────────────

_log_dir_cache = None
_logger_cache = {}

_FORMAT = logging.Formatter(
    '%(name)s - %(asctime)s - %(filename)s:[%(lineno)s] - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


# ── 路径计算（仅一次） ─────────────────────────────────────

def _log_dir():
    global _log_dir_cache
    if _log_dir_cache is None:
        project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        _log_dir_cache = os.path.join(project_path, 'logs')
        os.makedirs(_log_dir_cache, exist_ok=True)
    return _log_dir_cache


# ── 环境变量解析 ───────────────────────────────────────────

def _resolve_level(env_name, default):
    val = os.environ.get(env_name)
    if val:
        level = getattr(logging, val.upper(), None)
        if level is not None:
            return level
    return getattr(logging, default)


# ── pytest 环境检测 ─────────────────────────────────────────

def _in_pytest():
    """判断是否在 pytest 运行环境中"""
    return (
        'pytest' in sys.modules
        or os.environ.get('PYTEST_CURRENT_TEST')
        or os.path.basename(sys.argv[0]).startswith('pytest')
    )


# ── 公开 API ────────────────────────────────────────────────

def get_logger(name=None):
    """获取命名 logger，自动配置流 + 文件 handler。

    参数名建议传 __name__，这样日志会带上模块名前缀方便溯源。
    每个命名 logger 首次调用时创建 handler，之后复用。
    """
    name = name or __name__

    # 缓存命中 → 直接返回
    if name in _logger_cache:
        return _logger_cache[name]

    logger = logging.getLogger(name)
    logger.setLevel(_resolve_level('LOG_LEVEL', 'DEBUG'))

    # handler 防重（同一个 logger 名只加一次）
    if not logger.handlers:
        # 控制台 handler：仅非 pytest 环境配（pytest 用 live_logs 接管）
        if not _in_pytest():
            sh = logging.StreamHandler(sys.stdout)
            sh.setLevel(_resolve_level('LOG_STREAM_LEVEL', 'INFO'))
            sh.setFormatter(_FORMAT)
            logger.addHandler(sh)

        # 文件 handler → logs/YYYY-MM-DD.log（始终写入）
        fh = logging.FileHandler(
            os.path.join(_log_dir(), time.strftime('%Y-%m-%d') + '.log'),
            encoding='utf-8',
        )
        fh.setLevel(_resolve_level('LOG_FILE_LEVEL', 'DEBUG'))
        fh.setFormatter(_FORMAT)
        logger.addHandler(fh)

        # 关 propagation，防命名 logger 日志被 root 重复处理
        logger.propagate = False

    _logger_cache[name] = logger
    return logger
