import os
import yaml

class ReadConfig:

    #获取当前地址
    def __init__(self):
        self.root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #拼接当前位置的绝对路
        self.config_path = os.path.join(self.root_path, 'config', 'config.yaml')


    #读取文件
    def get_config(self):
        with open(self.config_path, 'r', encoding = 'utf-8') as f:
            yaml_data = yaml.safe_load(f)
        return yaml_data


#实例化
read_config = ReadConfig()
project_root_path = read_config.root_path
config_data = read_config.get_config()

