# src/main.py
import dearpygui.dearpygui as dpg
import os
import pyperclip
from screenshot import capture_interactive_screenshot # 导入新函数
from api import search_image
from config import config
from utils import log_message
from screenshot import ScreenShot  # 导入 ScreenShot 类
import keyboard

dpg.create_context()

# Global variable to hold the screenshot instance
screenshot_instance = None

# 加载字体
with dpg.font_registry():
    with dpg.font("resources/SimHei.ttf", 16) as font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)
        dpg.bind_font(font)

dpg.create_viewport(title='Searcher', width=900, height=600, min_width=400, min_height=300)

with dpg.window(tag="MainWindow"):
    with dpg.collapsing_header(label="软件设置",default_open=True):
        with dpg.group(label="软件设置",horizontal=False):
            dpg.add_text("软件设置")
            with dpg.group(horizontal=True):
                dpg.add_checkbox(label="窗口置顶", 
                                default_value=config.get("always_on_top", False),
                                callback=lambda s: set_always_on_top(dpg.get_value(s)),
                                tag="always_on_top_checkbox")
                dpg.add_checkbox(label="截图时隐藏窗口", 
                                default_value=config.get("hide_on_capture", False),
                                callback=lambda s: set_hide_on_capture(dpg.get_value(s)),
                                tag="hide_on_capture_checkbox")
                
            hotkey_capture = dpg.add_input_text(label="截图快捷键",default_value=config.get("hotkey_capture", "ctrl+q"))
            hotkey_search = dpg.add_input_text(label="搜索快捷键",default_value=config.get("hotkey_search", "ctrl+w"))

            with dpg.group(horizontal=True):
                dpg.add_button(label="保存设置", callback=lambda: save_settings())
            dpg.add_separator()

    with dpg.collapsing_header(label="答题API设置",default_open=False):
        dpg.add_text("答题API设置")
        api_url_input = dpg.add_input_text(label="API地址",
                                            default_value=config.get("api_url"),
                                            width=400,
                                            tag="api_url_input")
        api_token_input = dpg.add_input_text(label="Token",
                                                password=True,
                                                default_value=config.get("api_token"),
                                                width=400,
                                                tag="api_token_input")
        with dpg.group(horizontal=True):
            dpg.add_button(label="保存API配置", callback=lambda: save_api_config())
            dpg.add_button(label="复制Token", callback=lambda: copy_token())

        dpg.add_separator()

    with dpg.collapsing_header(label="OCR模型设置",default_open=False):
        dpg.add_text("OCR模型设置")
        api_url_input = dpg.add_input_text(label="API地址",
                                            default_value=config.get("api_url"),
                                            width=400,
                                            tag="ocr_url_input")
        api_token_input = dpg.add_input_text(label="Token",
                                                password=True,
                                                default_value=config.get("api_token"),
                                                width=400,
                                                tag="ocr_token_input")
        with dpg.group(horizontal=True):
            dpg.add_button(label="保存API配置", callback=lambda: save_api_config())
            dpg.add_button(label="复制Token", callback=lambda: copy_token())

        dpg.add_separator()

    with dpg.collapsing_header(label="功能页面",default_open=True):
            with dpg.group(horizontal=False,label="functions"):
                dpg.add_text("功能界面")
                #dpg.add_image("screenshot.png")
                dpg.add_combo(label="当前题目类型",tag="function_select",items=["单选题","多选题","判断题","填空题","其他类型题目"],default_value="单选题")
                dpg.add_input_text(label="识别内容",tag="recognition_context",multiline=True)
                with dpg.group(horizontal=True):
                    # 修改按钮的回调为 capture_interactive_screenshot
                    dpg.add_button(label="截图", callback=lambda: capture_interactive_screenshot(), tag="btn_capture")
                    dpg.add_button(label="搜索", callback=lambda: search_question_wrapper(), tag="btn_search")

                dpg.add_text("", tag="search_result_tag")
                dpg.add_spacer(height=10)

            dpg.add_separator()
    with dpg.collapsing_header(label="系统日志",default_open=True):
            with dpg.group(horizontal=False):
                dpg.add_text("操作日志：")
                dpg.add_text("", tag="log_output", wrap=500)

# with dpg.handler_registry(tag="input_handlers"):
#     # 修改快捷键的回调
#     dpg.add_key_press_handler(callback=lambda s, a: handle_hotkey())

def handle_hotkey():
    keyboard.add_hotkey(config.get('hotkey_capture','ctrl+q'),capture_interactive_screenshot)
    keyboard.add_hotkey(config.get('hotkey_search','ctrl+w'), search_question_wrapper)

def search_question_wrapper():
    """搜索问题的包装函数，处理UI更新"""
    # 获取截图文件名
    screenshot_filename = config.get("screenshot_filename")
    # 如果截图文件不存在，则设置搜索结果标签为错误信息
    if not os.path.exists(screenshot_filename):
        dpg.set_value("search_result_tag", "错误：请先截图")
        return

    # 调用搜索图片函数，获取搜索结果
    result = search_image(screenshot_filename)
    # 如果搜索结果不为空，则设置搜索结果标签为找到的结果数量
    if result:
       dpg.set_value("search_result_tag", f"找到 {len(result)} 条结果")

def save_settings():
    """保存设置到配置文件"""
    config.set("hotkey_capture", dpg.get_value(hotkey_capture))
    config.set("hotkey_search", dpg.get_value(hotkey_search))
    log_message("设置已保存,重启后生效！")

def set_always_on_top(value):
    """设置窗口置顶状态"""
    config.set("always_on_top", value)
    dpg.set_viewport_always_top(value)

def set_hide_on_capture(value):
    """设置截图后隐藏窗口"""
    config.set("hide_on_capture", value)

def copy_token():
    """复制Token到剪贴板"""
    token = dpg.get_value("api_token_input")
    pyperclip.copy(token)
    log_message("Token已复制")

def save_api_config():
    """保存API配置到文件"""
    config.set("api_url", dpg.get_value("api_url_input"))
    config.set("api_token", dpg.get_value("api_token_input"))
    log_message("API 配置已保存")


handle_hotkey()
dpg.set_primary_window("MainWindow", True)
dpg.setup_dearpygui()
dpg.show_viewport()
# 应用窗口置顶配置
dpg.set_viewport_always_top(config.get("always_on_top", False))
dpg.start_dearpygui()
dpg.destroy_context()
