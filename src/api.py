# src/api.py
import requests
from utils import log_message,copy_to_clipboard
from config import config 
import json
from typing import Dict
def search(query, timeout=30):
    """
    发送图片到指定的API进行搜索。

    Args:
        image_path (str): 要搜索的图片的路径。
        timeout (int): 请求超时时间（秒）。

    Returns:
        dict: API响应的JSON数据, 如果请求失败则返回None。
    """
    model_params = {"免费模型(充值用户使用)": "free", "基础推理模型": "basic"}
    api_url = config.get("search/like/api_url") 
    api_token = config.get("search/like/api_token")
    api_model = config.get("search/like/api_model","")
    if api_model in model_params:
        api_model = model_params[api_model]
    enable_search = config.get("search/like/api_search",False)
    if not api_url.startswith("http"):
        log_message("错误:API地址格式无效")
        return None
    
    headers = {
    'Content-Type': 'application/json',
    }

    json_params = {
        "query": query,
        "token": api_token,
        "model": api_model,
        "search": enable_search
    }
    req = requests.post(api_url, json=json_params, timeout=timeout,headers=headers)
    if req.status_code == 200:
        data = req.json()
        res = resolve_context(data)
        log_message("查询返回数据："+json.dumps(data, ensure_ascii=False))
        log_message("答案：{}".format(res))
        if config.get("auto_copy"):
            copy_to_clipboard(res)
        return res
    else:
        log_message(f"Error: {req.status_code} - {req.text}")

    return None

def resolve_context(context:Dict):
    success = context.get("success")
    error_msg = context.get("error")
    query_type = context.get("data").get("type",0)
    if success:
        if query_type == 0:
            return context["data"]["others"]
        elif query_type == 1:
            result = ",".join(context["data"]["choose"])
            return result
        elif query_type == 2:
            return context["data"]["fill"]
        elif query_type == 3:
            return context["data"]["judge"]
    return error_msg