# src/api.py
import requests
from utils import log_message
from config import config  # Import the config object


def search_image(image_path, timeout=10): #移除api_url, api_token参数
    """
    发送图片到指定的API进行搜索。

    Args:
        image_path (str): 要搜索的图片的路径。
        timeout (int): 请求超时时间（秒）。

    Returns:
        dict: API响应的JSON数据, 如果请求失败则返回None。
    """
    api_url = config.get("api_url") # 使用config.get
    api_token = config.get("api_token")
    log_max_length = config.get("log_max_length")

    if not api_url.startswith("http"):
        log_message("错误：API地址格式无效")
        return None
    if not image_path:
         log_message("图片路径无效")
         return None

    try:
        with open(image_path, 'rb') as f:
            response = requests.post(
                api_url,
                headers={'Authorization': f'Bearer {api_token}'},
                files={'image': f},
                timeout=timeout
            )
            response.raise_for_status()  # 检查HTTP错误
            result = response.json()
            log_message(f"API响应：{(str(result), log_max_length)}")
            return result

    except requests.exceptions.RequestException as e:
        log_message(f"API错误：{str(e)}")
        return None
    except Exception as e:
        log_message(f"意外错误：{str(e)}")
        return None