import dearpygui.dearpygui as dpg
from config import config
import callbacks as cbs

def create_software_settings_gui():
    with dpg.collapsing_header(label="软件设置",default_open=True):
        with dpg.group(label="软件设置",horizontal=False):
            dpg.add_text("软件设置")
            with dpg.group(horizontal=True):
                dpg.add_checkbox(label="窗口置顶", 
                                default_value=config.get("always_on_top", False),
                                callback=lambda s: cbs.set_always_on_top(dpg.get_value(s)),
                                tag="always_on_top_checkbox")
                dpg.add_checkbox(label="截图时隐藏窗口", 
                                default_value=config.get("hide_on_capture", False),
                                callback=lambda s: cbs.set_hide_on_capture(dpg.get_value(s)),
                                tag="hide_on_capture_checkbox")
                dpg.add_checkbox(label="自动调用OCR模型", 
                                default_value=config.get("ocr_auto", False),
                                callback=lambda s: cbs.set_ocr_auto(dpg.get_value(s)),
                                tag="ocr_auto_checkbox")
                dpg.add_checkbox(label="自动搜索答案(开启自动调用OCR模型后生效)", 
                                default_value=config.get("search_auto", False),
                                callback=lambda s: cbs.set_search_auto(dpg.get_value(s)),
                                tag="search_auto_checkbox")
            with dpg.group(horizontal=True):
                dpg.add_checkbox(label="自动复制答案",default_value=config.get("auto_copy", False),
                                callback=lambda s: cbs.set_auto_copy(dpg.get_value(s)),
                                tag="auto_copy_checkbox")
            dpg.add_input_text(label="截图快捷键",default_value=config.get("hotkey_capture", "ctrl+q"))
            dpg.add_input_text(label="搜索快捷键",default_value=config.get("hotkey_search", "ctrl+w"))

            with dpg.group(horizontal=True):
                dpg.add_button(label="保存设置", callback=lambda: cbs.save_settings())
            dpg.add_separator()

def create_search_gui():
    with dpg.collapsing_header(label="答题API设置",default_open=False):
        dpg.add_text("答题API设置")
        dpg.add_input_text(label="API地址",
                                            default_value=config.get("search/api_url"),
                                            width=400,
                                            tag="search/api_url")
        dpg.add_input_text(label="Token",
                                                password=True,
                                                default_value=config.get("search/api_token"),
                                                width=400,
                                                tag="search/api_token")
        
        dpg.add_button(label="还没有Token? 点此即可申请Token",tag="apply_token_text",callback=lambda: cbs.openlink("https://www.datam.site/doc/apply_token"))

        dpg.add_combo(label="模型选择",default_value=config.get("search/api_model","deepseek-v3"),
                      items=["deepseek-v3","deepseek-r1","gpt-4o","o3-mini","gemini-2.0-pro-exp","基础推理模型","免费模型(充值用户使用)"],
                      tag="search/api_model",callback=lambda s: cbs.set_query_model(dpg.get_value(s)))
        with dpg.group(horizontal=True):
            dpg.add_button(label="保存API配置", callback=lambda: cbs.save_api_config())
            dpg.add_button(label="复制Token", callback=lambda: cbs.copy_token())

        dpg.add_separator()

def create_ocr_gui():
    with dpg.collapsing_header(label="OCR模型设置",default_open=False):
        dpg.add_text("OCR模型设置")
        dpg.add_combo(label="模型选择",tag="ocr/model",items=["阿里百炼OCR","PaddleOCR"],default_value=config.get("ocr/model","阿里百炼OCR"))
        dpg.add_text("OCR参数设置")
        with dpg.tree_node(label="阿里百炼OCR"):
            dpg.add_input_text(label="API密钥",default_value=config.get("ocr/ali-ocr/api_key"),tag="ocr/ali-ocr/api_key",password=True)
            dpg.add_button(label="阿里百炼官网",tag="ocr_ali_text",callback=lambda: cbs.openlink("https://bailian.console.aliyun.com/"))
        with dpg.tree_node(label="PaddleOCR"):
            dpg.add_input_text(label="模型路径",default_value=config.get("ocr/paddle-ocr/model_path"),tag="ocr/paddle-ocr/model_path")
            dpg.add_input_text(label="字典路径",default_value=config.get("ocr/paddle-ocr/dict_path"),tag="ocr/paddle-ocr/dict_path")
        dpg.add_spacer(height=6)
        dpg.add_separator()
        with dpg.group(horizontal=True):
            dpg.add_button(label="保存OCR设置", callback=lambda: cbs.save_ocr_config())
        dpg.add_separator()

def create_func_gui():
    with dpg.collapsing_header(label="功能页面",default_open=True):
        with dpg.group(horizontal=False,label="functions"):
            dpg.add_text("功能界面")
            #dpg.add_image("screenshot.png")
            dpg.add_combo(label="当前题目类型",tag="search/query_type",items=["单选题","多选题","判断题","填空题","其他类型题目"],
                          default_value=config.get("search/query_type","单选题"),callback=lambda s: cbs.set_query_type(dpg.get_value(s)))
            dpg.add_input_text(label="识别内容",tag="recognition_context",multiline=True)
            with dpg.group(horizontal=True):
                # 修改按钮的回调为 capture_interactive_screenshot
                dpg.add_button(label="截图", callback=lambda: cbs.capture_interactive_screenshot(), tag="btn_capture")
                dpg.add_button(label="OCR识别", callback=lambda: cbs.ocr_recognize(), tag="btn_ocr_recognize")
                dpg.add_button(label="搜索", callback=lambda: cbs.search_question_wrapper(), tag="btn_search")
            dpg.add_text("", tag="search_result_tag")
            dpg.add_spacer(height=10)

        dpg.add_separator()

def create_log_gui():
    with dpg.collapsing_header(label="系统日志",default_open=True):
            with dpg.group(horizontal=False):
                dpg.add_text("操作日志：")
                dpg.add_text("", tag="log_output", wrap=500)