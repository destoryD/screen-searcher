import requests
from utils import log_message,copy_to_clipboard
from config import config 
import json
from typing import Dict
import dearpygui.dearpygui as dpg
import openai
class API_Model(object):
    def __init__(self, name="api_model"):
        self.name = name
    
    def search(self, query:str):
        pass

    def _resolve_(self, context:Dict):
        pass

    def _reload_(self):
        pass

class API_Model_Like(API_Model):
    def __init__(self, auto_reload:bool = False):
        self.name = "LIKE知识库"
        super().__init__(self.name)
        self.auto_reload = auto_reload
        self.headers = {'Content-Type': 'application/json'}
        self.status = 0
        self._init_params_()

    def _init_params_(self):
        self.api_url = config.get("search/like/api_url")
        self.api_token = config.get("search/like/api_token")
        self.headers['Authorization'] = f'Bearer {self.api_token}'
        self.api_model = config.get("search/like/api_model", "")
        self.api_models = self.get_api_models()
        self.check_url = "https://app.datam.site/"
        self.enable_search = config.get("search/like/api_search", False)
        self.enable_vision = config.get("search/like/api_vision", True)
        self.available = self.check_api_status()
        self.balance = self.get_api_balance()
        self.refresh_ui_status(update=False)
        return
    
    def check_api_status(self):
        try:
            response = requests.get(self.check_url)
            return response.status_code == 200
        except Exception as e:
            log_message(f"Error: {e}")
            return False

    def get_api_models(self):
        models_api = "https://app.datam.site/api/v1/query/models"
        req = requests.get(models_api, headers=self.headers)
        if req.status_code == 200:
            data = req.json()
            models = data.get("models", [])
            return models
        else:
            log_message(f"Error: {req.status_code} - {req.text}")
            return []

    def get_api_balance(self):
        balance_api = "https://app.datam.site/api/v1/balance"

        req = requests.get(balance_api, headers=self.headers)
        if req.status_code == 200:
            data = req.json()
            balance = int(data.get("balance", 0))
            log_message("查询余额成功，余额为：{}".format(balance))
            return balance
        else:
            log_message(f"Error: {req.status_code} - {req.text}")
            return 0
        
    def refresh_ui_status(self, update=True):
        if update:
            self._init_params_()
        dpg.set_value("search/like/api_balance", "API余额：{} 次".format(str(self.balance)))
        response = requests.get(self.check_url)
        self.available = response.status_code == 200
        dpg.set_value("search/like/api_status", "当前API状态：{}".format("可用" if self.available else "不可用"))
        dpg.configure_item("search/like/api_model", items=self.api_models)
        return 
    
    def show_status(self):
        status_msg = ""
        if self.status == 0:
            status_msg = "空闲"
        elif self.status == 1:
            status_msg = "处理中"
        else:
            status_msg = "未知状态"
        dpg.set_value("search_status_tag", "当前状态：{}".format(status_msg))

    def _reload_(self):
        self._init_params_()
        return
    
    def search(self, query:str, timeout:int = 120):
        if self.auto_reload:
            self._reload_()

        if not self.api_url.startswith("http"):
            log_message("错误:API地址格式无效")
            return None

        json_params = {
            "query": query,
            "model": self.api_model,
            "search": self.enable_search,
            "vision": self.enable_vision,
        }
        # self.headers = {'Authorization': f'Bearer {self.api_token}', 'Content-Type': 'application/json'}
        self.status = 1
        self.show_status()
        req = requests.post(self.api_url, json=json_params, timeout=timeout, headers=self.headers)
        if req.status_code == 200:
            data = req.json()
            res, msg = self.resolve_context(data)
            # breakpoint()
            log_message("查询返回数据：" + json.dumps(data, ensure_ascii=False))
            log_message("查询返回信息：" + msg)
            log_message("答案：{}".format(res))
            if config.get("auto_copy"):
                copy_to_clipboard(res)
            self.status = 0
            self.show_status()
            return res
        else:
            log_message(f"Error: {req.status_code} - {req.text}")


    def resolve_context(self, context:dict):
        msg = context.get("message", "请求失败")
        output = context.get("results", {}).get("output", {})
        result = ""
        if output:
            question_type = output.get("questionType", "OTHER")
            answer = output.get("answer", {})
            if question_type == "CHOICE":
                result = ",".join(answer.get("selectedOptions", []))
            elif question_type == "FILL_IN_BLANK":
                result = ",".join(answer.get("blanks", []))
            elif question_type == "JUDGMENT":
                result = answer.get("isCorrect", True)
                result = "正确" if result else "错误"
            elif question_type == "OTHER":
                result = answer.get("otherText", "")
        return result, msg

class API_Model_OpenAI(API_Model):
    def __init__(self, auto_reload:bool = False):
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