class Global:
    """全局变量储存"""
    pass


# 创建全局实例
global_env = Global()


def set_env(key, value):
    """设置全局变量"""
    setattr(global_env, key, value)


def get_env(key, default=None):
    """获取全局变量"""
    return getattr(global_env, key, default)


def clear_env():
    """清除所有全局变量"""
    for attr in list(vars(global_env).keys()):
        if not attr.startswith('_'):  # 跳过内置属性
            delattr(global_env, attr)
