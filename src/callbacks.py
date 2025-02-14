import dearpygui.dearpygui as dpg
from config import config
from utils import log_message
import os
import pyperclip
from screenshot import ScreenShot
from ocr_models import Qwen_MODEL
from api import search
import webbrowser
def search_question_wrapper():
    """搜索问题的包装函数，处理UI更新"""
    # 获取截图文件名
    screenshot_filename = config.get("screenshot_filename")
    # 如果截图文件不存在，则设置搜索结果标签为错误信息
    if not os.path.exists(screenshot_filename):
        dpg.set_value("search_result_tag", "错误：请先截图")
        return
    type_params = {"单选题":"【单选题】","多选题":"【多选题】","判断题":"【判断题】","填空题":"【填空题】","其他类型题目":"【其他类型题目】"}
    query = dpg.get_value("recognition_context")
    query_type = dpg.get_value("search/query_type")
    query = type_params.get(query_type,'') + query
    log_message("题目类型为：{} 开始请求API".format(query_type))
    # 调用搜索图片函数，获取搜索结果
    result = search(query)
    # 如果搜索结果不为空，则设置搜索结果标签为找到的结果数量
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

def copy_token():
    """复制Token到剪贴板"""
    token = dpg.get_value("search/api_token")
    pyperclip.copy(token)
    log_message("Token已复制")

def save_api_config():
    """保存API配置到文件"""
    config.set("search/api_url", dpg.get_value("search/api_url"))
    config.set("search/api_token", dpg.get_value("search/api_token"))
    log_message("API 配置已保存")
def set_query_type(value):
    """设置查询类型"""
    config.set("search/query_type", value)
    log_message(f"查询类型已设置为 {value}")

def set_query_model(value):
    """设置查询模型"""
    config.set("search/api_model", value)
    log_message(f"查询模型已设置为 {value}")
def ocr_recognize():
    model = config.get("ocr/model")
    result = ""
    log_message("调用OCR流程")
    if model == "阿里百炼OCR":
        api_key = config.get("ocr/ali-ocr/api_key")
        ocr_model = Qwen_MODEL(api_key)
        result = ocr_model.recognize()
        print(result)
    dpg.set_value("recognition_context",result)
    log_message("OCR识别完毕")
    return result
def save_ocr_config():
    """保存OCR配置到文件"""
    config.set("ocr/model", dpg.get_value("ocr/model"))
    config.set("ocr/ali-ocr/api_key", dpg.get_value("ocr/ali-ocr/api_key"))
    log_message("OCR 配置已保存")
    
def capture_interactive_screenshot():
    """
    Captures an interactive screenshot using the ScreenShot class and returns the captured image.
    Returns:
        PIL.Image.Image or None: The captured image if successful, None otherwise.
    """
    import dearpygui.dearpygui as dpg
    pos = dpg.get_viewport_pos()
    #print(dpg.get_viewport_configuration('Searcher'))
    if config.get("hide_on_capture",False):
        dpg.configure_viewport("Searcher",x_pos=-10000,y_pos=-10000)
    screenshot_tool = ScreenShot()  # Instantiate the ScreenShot class
    img = screenshot_tool.img # Capture the image
    img.save(config.get("screenshot_filename","screenshot.png"))
    dpg.set_viewport_pos(pos)
    log_message("截图完成")
    if config.get("ocr_auto",False):
        ocr_recognize()
        if config.get("search_auto",False):
            search_question_wrapper()
    return img # Capture and return the image

def openlink(url):
    webbrowser.open(url)