import dearpygui.dearpygui as dpg
from config import config
from utils import log_message
import os
import pyperclip
from screenshot import ScreenShot
from ocr_models import Qwen_MODEL,PaddleOCR_MODEL,Sili_MODEL,Zhipu_MODEL
from api_models import API_Model_Like,API_Model_OpenAI
import webbrowser
import global_vars
def search_question_wrapper():
    """搜索问题的包装函数，处理UI更新"""
    screenshot_filename = config.get("screenshot_filename")
    if not os.path.exists(screenshot_filename):
        dpg.set_value("search_result_tag", "错误：请先截图")
        return
    type_params = {"单选题":"【单选题】","多选题":"【多选题】","判断题":"【判断题】","填空题":"【填空题】","其他类型题目":"【其他类型题目】"}
    query = dpg.get_value("recognition_context")
    query_type = dpg.get_value("search/query_type")
    
    # 如果启用了自动添加题目类型
    if config.get("auto_complete", False):
        query = type_params.get(query_type, '') + query
    
    log_message("题目类型为：{} 开始请求API".format(query_type))

    result = global_vars.api_model.search(query)

    if result:
       dpg.set_value("search_result_tag", "答案: "+ result)

def save_settings():
    """保存设置到配置文件"""
    config.set("hotkey_capture", dpg.get_value('hotkey_capture'))
    config.set("hotkey_search", dpg.get_value('hotkey_search'))
    log_message("设置已保存,重启后生效！")

def set_auto_copy(value):
    """保存设置到配置文件"""
    config.set("auto_copy", value)
def set_auto_complete(value):
    """保存设置到配置文件"""
    config.set("auto_complete", value)
def set_ocr_auto(value):
    """保存设置到配置文件"""
    config.set("ocr_auto", value)

def set_search_auto(value):
    """保存设置到配置文件"""
    config.set("search_auto", value)

def set_always_on_top(value):
    """设置窗口置顶状态"""
    config.set("always_on_top", value)
    dpg.set_viewport_always_top(value)

def set_hide_on_capture(value):
    """设置截图后隐藏窗口"""
    config.set("hide_on_capture", value)
def set_search_online(value):
    """设置在线搜索"""
    config.set("search/like/api_search", value)
def copy_token():
    """复制Token到剪贴板"""
    token = dpg.get_value("search/like/api_token")
    pyperclip.copy(token)
    log_message("Token已复制")

def save_api_config():
    """保存API配置到文件"""
    config.set("search/like/api_url", dpg.get_value("search/like/api_url"))
    config.set("search/like/api_token", dpg.get_value("search/like/api_token"))
    log_message("API 配置已保存")
def set_query_type(value):
    """设置查询类型"""
    config.set("search/query_type", value)
    log_message(f"查询类型已设置为 {value}")

def set_query_model(value):
    """设置查询模型"""
    config.set("search/like/api_model", value)
    log_message(f"查询模型已设置为 {value}")

def ocr_recognize():
    log_message("调用OCR流程-使用模型{}".format(config.get("ocr/model")))
    result = global_vars.ocr_model.recognize()
    print(result)
    dpg.set_value("recognition_context", result)
    
    # 添加自动推断题目类型功能
    if config.get("auto_detect_type", False) and result:
        question_type = detect_question_type(result)
        if question_type:
            dpg.set_value("search/query_type", question_type)
            log_message(f"自动推断题目类型为: {question_type}")
    
    log_message("OCR识别完毕")
    return result

def detect_question_type(text):
    """根据文本内容推断题目类型"""
    text = text.lower()
    
    # 判断题特征
    if "正确" in text and "错误" in text:
        return "判断题"
    if "对" in text and "错" in text:
        return "判断题"
    
    # 单选题特征
    if any(marker in text for marker in ["a.", "b.", "c.", "d.", "a、", "b、", "c、", "d、"]):
        # 检查是否有多选提示
        if "多选" in text or "多项" in text:
            return "多选题"
        return "单选题"
    
    # 多选题特征
    if "多选" in text or "多项" in text:
        return "多选题"
    
    # 填空题特征
    if "填空" in text or "_____" in text or "____" in text or "__" in text:
        return "填空题"
    
    # 如果没有明确特征，返回None，保持原有选择
    return None

def save_openai_api_config():
    """保存OpenAI API配置到文件"""
    config.set("search/openai/api_url", dpg.get_value("search/openai/api_url"))
    config.set("search/openai/api_key", dpg.get_value("search/openai/api_key"))
    config.set("search/openai/model", dpg.get_value("search/openai/model"))
    config.set("search/openai/models_list", dpg.get_value("search/openai/models_list"))
    config.set("search/openai/temperature", dpg.get_value("search/openai/temperature"))
    config.set("search/openai/max_tokens", dpg.get_value("search/openai/max_tokens"))
    log_message("OpenAI API 配置已保存")

def save_ocr_config():
    """保存OCR配置到文件"""
    config.set("ocr/ali-ocr/api_key", dpg.get_value("ocr/ali-ocr/api_key"))
    config.set("ocr/sili-ocr/api_key", dpg.get_value("ocr/sili-ocr/api_key"))
    config.set("ocr/zhipu-ocr/api_key", dpg.get_value("ocr/zhipu-ocr/api_key"))
    config.set("ocr/paddle-ocr/model", dpg.get_value("ocr/paddle-ocr/model"))
    config.set("ocr/paddle-ocr/lang", dpg.get_value("ocr/paddle-ocr/lang"))
    set_ocr_model(dpg.get_value("ocr/model"))
    log_message("OCR 配置已保存")

def set_ocr_model(value):
    """设置OCR模型"""
    config.set("ocr/model", value)
    if config.get("ocr/model") == "阿里百炼OCR":
        global_vars.ocr_model = Qwen_MODEL(config.get("ocr/ali-ocr/api_key"))
    elif config.get("ocr/model") == "PaddleOCR":
        global_vars.ocr_model = PaddleOCR_MODEL(lang=config.get("ocr/paddle-ocr/lang"),ocr_version=config.get("ocr/paddle-ocr/model"))
    elif config.get("ocr/model") == "硅基流动":
        global_vars.ocr_model = Sili_MODEL(config.get("ocr/sili-ocr/api_key"))
    elif config.get("ocr/model") == "智谱AI":
        global_vars.ocr_model = Zhipu_MODEL(config.get("ocr/zhipu-ocr/api_key"))
    log_message(f"OCR模型已设置为 {value}")

def set_api_model(value):
    """设置API模型"""
    config.set("search/tiku", value)
    if config.get("search/tiku") == "LIKE知识库":
        global_vars.api_model = API_Model_Like(auto_reload=True)
    elif config.get("search/tiku") == "OpenAI兼容API":
        global_vars.api_model = API_Model_OpenAI(auto_reload=True)
    log_message(f"查题API已设置为 {value}")

def set_openai_query_model(value):
    """设置OpenAI查询模型"""
    config.set("search/openai/model", value)
    log_message(f"OpenAI查询模型已设置为 {value}")

def refresh_openai_api():
    """刷新OpenAI"""
    if isinstance(global_vars.api_model,API_Model_OpenAI):
        global_vars.api_model.vis_api_status()
    else:
        tmp_model = API_Model_OpenAI()
        tmp_model.vis_api_status()
        del tmp_model

def refresh_like_api():
    """刷新知识库"""
    if isinstance(global_vars.api_model,API_Model_Like):
        global_vars.api_model.vis_api_balance()
    else:
        tmp_model = API_Model_Like()
        tmp_model.vis_api_balance()
        del tmp_model

def capture_interactive_screenshot():
    """
    Captures an interactive screenshot using the ScreenShot class and returns the captured image.
    Returns:
        PIL.Image.Image or None: The captured image if successful, None otherwise.
    """
    pos = dpg.get_viewport_pos()
    #print(dpg.get_viewport_configuration('Searcher'))
    if config.get("hide_on_capture",False):
        dpg.configure_viewport("Searcher",x_pos=-10000,y_pos=-10000)
    screenshot_tool = ScreenShot()  # Instantiate the ScreenShot class
    img = screenshot_tool.img # Capture the image
    if img:
        img.save(config.get("screenshot_filename","screenshot.png"))
        log_message("截图完成")
    else:
        log_message("截图未完成")
    dpg.set_viewport_pos(pos)
    if config.get("ocr_auto",False):
        ocr_recognize()
        if config.get("search_auto",False):
            search_question_wrapper()
    return img # Capture and return the image

def openlink(url):
    webbrowser.open(url)

def set_auto_detect_type(value):
    """保存自动推断题目类型设置到配置文件"""
    config.set("auto_detect_type", value)
    log_message(f"自动推断题目类型已{'启用' if value else '禁用'}")