import requests
from utils import log_message,copy_to_clipboard
from config import config 
import json
from typing import Dict
import dearpygui.dearpygui as dpg
import openai
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
        self.auto_reload = auto_reload
        self.headers = {'Content-Type': 'application/json'}
        self._init_params_()
    def _init_params_(self):
        self.api_url = config.get("search/like/api_url")
        self.api_token = config.get("search/like/api_token")
        self.api_model = config.get("search/like/api_model","")
        self.enable_search = config.get("search/like/api_search",False)
        self.model_params = {"免费模型(充值用户使用)": "free", "基础推理模型": "basic"}
        self.available = True
        self.balance = 0
        if self.api_model in self.model_params:
            self.api_model = self.model_params[self.api_model]
        self.balance = self.get_api_balance()
        if self.balance <=0:
            self.available = False
        else:
            self.available = True
        self.vis_api_balance(update=False)
        return
    def get_api_balance(self,api_token=None):
        balance_api = "https://api.datam.site/balance"
        json_params = {
            "token": api_token if api_token else self.api_token
        }
        req = requests.post(balance_api, headers=self.headers,json=json_params)
        if req.status_code == 200:
            data = req.json()
            balance = data.get("data",{}).get("balance",0)
            log_message("查询余额成功，余额为：{}".format(balance))
            return balance
        else:
            log_message(f"Error: {req.status_code} - {req.text}")
            return 0
    def vis_api_balance(self,update=True):
        if update:
            self._init_params_()
        dpg.set_value("search/like/api_balance","API余额：{} 次".format(str(self.balance)))
        dpg.set_value("search/like/api_status","当前API状态：{}".format("可用" if self.available else "不可用"))
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
                return ",".join(context["data"]["fills"])
            elif query_type == 3:
                return context["data"]["judge"]
        return error_msg

class API_Model_OpenAI(API_Model):
    def __init__(self, auto_reload=False):
        self.name = "OpenAI兼容API"
        super().__init__(self.name)
        self.auto_reload = auto_reload
        self._init_params_()
        
    def _init_params_(self):
        self.api_url = config.get("search/openai/api_url", "")
        self.api_key = config.get("search/openai/api_key", "")
        self.client = openai.OpenAI(
                api_key=self.api_key,
                base_url=self.api_url
            )
        self.model = config.get("search/openai/model", "gpt-4o-mini")
        self.temperature = config.get("search/openai/temperature", 0.7)
        self.max_tokens = config.get("search/openai/max_tokens", 1000)
        self.available = self.test_model_with_conversation()
        self.vis_api_status(update=False)
        return
        
    def vis_api_status(self, update=True):
        if update:
            self._init_params_()
        dpg.set_value("search/openai/api_status", "当前API状态：{}".format("可用" if self.available else "不可用"))
        return
        
    def _reload_(self):
        self._init_params_()
        return
    
    def get_models_list(self):
        try:
            models_list = self.client.models.list()
            return models_list
        except:
            return None
    def search(self, query:str, timeout:int=60):
        if self.auto_reload:
            self._reload_()
        if not self.api_url.startswith("http"):
            log_message("错误:API地址格式无效")
            return None
            
        if not self.available:
            log_message("错误:API配置不可用，请检查API地址和密钥")
            return None
            
        try:
            # 使用openai库发送请求
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": query}],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                timeout=timeout
            )
            
            # 解析结果
            res = response.choices[0].message.content.strip()
            log_message("查询返回数据：" + str(response))
            log_message("答案：{}".format(res))
            if config.get("auto_copy"):
                copy_to_clipboard(res)
            return res
            
        except Exception as e:
            error_msg = f"请求异常: {str(e)}"
            log_message(error_msg)
            return error_msg
    
    def test_model_with_conversation(self):
        """通过简单对话测试模型是否可用"""
        try:
            test_message = "Hello"
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": test_message}],
                temperature=0.1,  # 使用低温度以获得更确定性的回复
                max_tokens=20,    # 限制token数量，加快测试速度
                timeout=10    # 设置较短的超时时间
            )
            
            # 检查是否有响应内容
            if response and response.choices and len(response.choices) > 0:
                content = response.choices[0].message.content.strip()
                log_message("Openai兼容API- {} 模型测试成功".format(self.model))
                # 只要有内容返回就认为测试成功
                return True
            return False
        except Exception as e:
            log_message(f"模型测试异常: {str(e)}")
            return False