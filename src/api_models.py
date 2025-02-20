import requests
from utils import log_message,copy_to_clipboard
from config import config 
import json
from typing import Dict

class API_Model(object):
    def __init__(self,name="api_model"):
        self.name = name
    
    def search(self,query:str):
        pass

    def _resolve_(self,context:Dict):
        pass

    def _reload_(self):
        pass

class API_Model_Like(API_Model):
    def __init__(self,auto_reload=False):
        self.name = "LIKE知识库"
        super().__init__(self.name)
        self.api_url = config.get("search/like/api_url") 
        self.api_token = config.get("search/like/api_token")
        self.api_model = config.get("search/like/api_model","")
        self.enable_search = config.get("search/like/api_search",False)
        self.auto_reload = auto_reload
        self.model_params = {"免费模型(充值用户使用)": "free", "基础推理模型": "basic"}
        if self.api_model in self.model_params:
            self.api_model = self.model_params[self.api_model]
        self.headers = {'Content-Type': 'application/json'}
    def _init_params_(self):
        self.api_url = config.get("search/like/api_url")
        self.api_token = config.get("search/like/api_token")
        self.api_model = config.get("search/like/api_model","")
        self.enable_search = config.get("search/like/api_search",False)
        self.model_params = {"免费模型(充值用户使用)": "free", "基础推理模型": "basic"}
        if self.api_model in self.model_params:
            self.api_model = self.model_params[self.api_model]
        return
    def _reload_(self):
        self._init_params_()
        return
    def search(self,query:str,timeout:int=60):
        if self.auto_reload:
            self._reload_()
        if not self.api_url.startswith("http"):
            log_message("错误:API地址格式无效")
            return None

        json_params = {
            "query": query,
            "token": self.api_token,
            "model": self.api_model,
            "search": self.enable_search
        }
        req = requests.post(self.api_url, json=json_params, timeout=timeout,headers=self.headers)
        if req.status_code == 200:
            data = req.json()
            res = self.resolve_context(data)
            log_message("查询返回数据："+json.dumps(data, ensure_ascii=False))
            log_message("答案：{}".format(res))
            if config.get("auto_copy"):
                copy_to_clipboard(res)
            return res
        else:
            log_message(f"Error: {req.status_code} - {req.text}")
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
