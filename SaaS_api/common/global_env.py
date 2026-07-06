from types import SimpleNamespace

# 全局变量实例
global_env = SimpleNamespace()


def set_env(key, value):
    """设置全局变量"""
    setattr(global_env, key, value)


def get_env(key, default=None):
    """获取全局变量"""
    return getattr(global_env, key, default)


def clear_env():
    """清除所有非私有属性"""
    for attr in list(vars(global_env)):
        if not attr.startswith('_'):
            delattr(global_env, attr)
