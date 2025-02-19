# src/config.py
import json
import os

CONFIG_FILE = "config.json"  # 配置文件名
DEFAULT_CONFIG = "resources/config.json"

class Config:
    def __init__(self, config_file=CONFIG_FILE,default_config=DEFAULT_CONFIG):
        self.config_file = config_file
        self.default_config = default_config
        self._config_data = {}
        self.load_config()

    def load_config(self):
        """从 JSON 文件加载配置，如果文件不存在则创建默认配置。"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self._config_data = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config from {self.config_file}: {e}")
                print("Using default config.")
                if os.path.exists(self.default_config):
                    with open(self.default_config, "r", encoding="utf-8") as DEFAULT_CONFIG:
                        self._config_data = json.load(DEFAULT_CONFIG)
        else:
            print(f"Config file {self.config_file} not found. Creating with default values.")
            if os.path.exists(self.default_config):
                with open(self.default_config, "r", encoding="utf-8") as DEFAULT_CONFIG:
                    self._config_data = json.load(DEFAULT_CONFIG)
            self.save_config()

    def save_config(self):
        """将配置保存到 JSON 文件。"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self._config_data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving config to {self.config_file}: {e}")


    def get(self, key, default=None):
        """获取配置项的值。支持用/分隔的嵌套key，如'ocr/model/test'。"""
        try:
            keys = key.split('/')
            value = self._config_data
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key, value):
        """设置配置项的值。支持用/分隔的嵌套key，如'ocr/model/test'。"""
        keys = key.split('/')
        current = self._config_data
        for k in keys[:-1]:
            if k not in current or not isinstance(current[k], dict):
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value
        self.save_config()  # 每次设置都保存，简化操作


# 全局配置实例
config = Config()
