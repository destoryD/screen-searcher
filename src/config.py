# src/config.py
import json
import os

CONFIG_FILE = "config.json"  # 配置文件名
DEFAULT_CONFIG = {
    "api_url": "https://api.datam.site/search",
    "api_token": "",
    "screenshot_filename": "screenshot.png",
    "hide_on_capture": False,
    "log_max_length": 2000,
    "always_on_top": False,
    'hotkey_capture': 'ctrl+q',
    'hotkey_search': 'ctrl+w'
}

class Config:
    def __init__(self, config_file=CONFIG_FILE):
        self.config_file = config_file
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
                self._config_data = DEFAULT_CONFIG
        else:
            print(f"Config file {self.config_file} not found. Creating with default values.")
            self._config_data = DEFAULT_CONFIG
            self.save_config()

    def save_config(self):
        """将配置保存到 JSON 文件。"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self._config_data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving config to {self.config_file}: {e}")


    def get(self, key, default=None):
        """获取配置项的值。"""
        return self._config_data.get(key, default)

    def set(self, key, value):
        """设置配置项的值。"""
        self._config_data[key] = value
        self.save_config()  # 每次设置都保存，简化操作


# 全局配置实例
config = Config()
