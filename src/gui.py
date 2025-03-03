import dearpygui.dearpygui as dpg
from config import config
import callbacks as cbs
import utils
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
                dpg.add_checkbox(label="搜索时自动添加题目类型",default_value=config.get("auto_complete", True),
                                callback=lambda s: cbs.set_auto_complete(dpg.get_value(s)),
                                tag="auto_complete_checkbox")
            dpg.add_input_text(label="截图快捷键",default_value=config.get("hotkey_capture", "ctrl+q"),tag="hotkey_capture")
            dpg.add_input_text(label="搜索快捷键",default_value=config.get("hotkey_search", "ctrl+w"),tag="hotkey_search")

            with dpg.group(horizontal=True):
                dpg.add_button(label="保存快捷键设置", callback=lambda: cbs.save_settings())
            dpg.add_separator()

def create_search_gui():
    with dpg.collapsing_header(label="答题API设置",default_open=False):
        dpg.add_text("答题API设置")
        dpg.add_combo(label="题库选择",default_value=config.get("search/tiku","LIKE知识库"),items=["LIKE知识库","OpenAI兼容API"],callback= lambda s: cbs.set_api_model(dpg.get_value(s)))
        dpg.add_spacer(height=3)
        with dpg.tree_node(label="LIKE知识库"):
            with dpg.group(horizontal=True):
                dpg.add_text("当前API状态：不可用",tag="search/like/api_status")
                dpg.add_text("API余额：0 次",tag="search/like/api_balance")
                dpg.add_button(label="刷新",callback=lambda: cbs.refresh_like_api())
            dpg.add_input_text(label="API地址",
                                                default_value=config.get("search/like/api_url"),
                                                width=400,
                                                tag="search/like/api_url")
            dpg.add_input_text(label="Token",
                                                    password=True,
                                                    default_value=config.get("search/like/api_token"),
                                                    width=400,
                                                    tag="search/like/api_token")
            with dpg.group(horizontal=True):
                dpg.add_button(label="LIKE知识库官网",callback=lambda: cbs.openlink("https://www.datam.site/"))
                dpg.add_button(label="还没有Token? 点此即可申请Token，首次注册免费享500次查询",callback=lambda: cbs.openlink("https://www.datam.site/doc/apply_token"))

            dpg.add_combo(label="模型选择",default_value=config.get("search/like/api_model","deepseek-v3"),
                        items=["deepseek-v3","deepseek-r1","gpt-4o","o3-mini","gemini-2.0-pro-exp","基础推理模型","免费模型(充值用户使用)"],
                        tag="search/api_model",callback=lambda s: cbs.set_query_model(dpg.get_value(s)))
            dpg.add_checkbox(label="启用联网搜索",default_value=config.get("search/like/api_search", False),tag="search/like/api_search",
                        callback=lambda s: cbs.set_search_online(dpg.get_value(s)))
            with dpg.group(horizontal=True):
                dpg.add_button(label="保存API配置", callback=lambda: cbs.save_api_config())
                dpg.add_button(label="复制Token", callback=lambda: cbs.copy_token())
        with dpg.tree_node(label="OpenAI兼容API"):
            with dpg.group(horizontal=True):
                dpg.add_text("当前API状态：不可用",tag="search/openai/api_status")
                dpg.add_button(label="刷新(自动保存配置)",callback=lambda: cbs.refresh_openai_api())
            dpg.add_input_text(label="API地址",
                                default_value=config.get("search/openai/api_url", "https://api.openai.com/v1/chat/completions"),
                                width=400,
                                tag="search/openai/api_url")
            dpg.add_text("注意：这里的API只需填写base地址，不要填写/chat/completions等路径，否则可能导致API调用失败。")
            dpg.add_input_text(label="API密钥",
                                password=True,
                                default_value=config.get("search/openai/api_key", ""),
                                width=400,
                                tag="search/openai/api_key")
            dpg.add_input_text(label="模型名称",
                        default_value=config.get("search/openai/model", "gpt-4o-mini"),
                        callback = lambda s: cbs.set_openai_query_model(dpg.get_value(s)),
                        tag="search/openai/model")
            dpg.add_slider_float(label="温度",
                                default_value=config.get("search/openai/temperature", 0.7),
                                min_value=0.0,
                                max_value=1.5,
                                tag="search/openai/temperature")
            dpg.add_slider_int(label="最大Token数",
                            default_value=config.get("search/openai/max_tokens", 4096),
                            min_value=1024,
                            max_value=8192,
                            tag="search/openai/max_tokens")
            with dpg.group(horizontal=True):
                dpg.add_button(label="保存API配置", callback=lambda: cbs.save_openai_api_config())
                dpg.add_button(label="点此查看兼容平台/模型列表",callback=lambda: cbs.openlink("https://platform.openai.com/"))
        dpg.add_spacer(height=6)
        dpg.add_separator()

def create_ocr_gui():
    with dpg.collapsing_header(label="OCR模型设置",default_open=False):
        dpg.add_text("OCR模型设置")
        dpg.add_combo(label="模型选择",tag="ocr/model",items=["阿里百炼OCR","硅基流动","智谱AI","PaddleOCR"],default_value=config.get("ocr/model","阿里百炼OCR"),
                      callback=lambda s: cbs.set_ocr_model(dpg.get_value(s)))
        dpg.add_text("OCR参数设置")
        with dpg.tree_node(label="阿里百炼OCR"):
            dpg.add_input_text(label="API密钥",default_value=config.get("ocr/ali-ocr/api_key"),tag="ocr/ali-ocr/api_key",password=True)
            dpg.add_button(label="阿里百炼官网-注册送100W免费额度",tag="ocr_ali_text",callback=lambda: cbs.openlink("https://bailian.console.aliyun.com/"))
        with dpg.tree_node(label="硅基流动"):
            dpg.add_input_text(label="API密钥",default_value=config.get("ocr/sili-ocr/api_key"),tag="ocr/sili-ocr/api_key",password=True)
            dpg.add_button(label="硅基流动官网-注册送2000W免费Token",tag="ocr_sili_text",callback=lambda: cbs.openlink("https://cloud.siliconflow.cn/i/uXnJI1u7"))
            dpg.add_combo(label="视觉模型选择",items=['Pro/Qwen/Qwen2-VL-7B-Instruct'],default_value=config.get("ocr/sili-ocr/model","Pro/Qwen/Qwen2-VL-7B-Instruct"),tag="ocr/sili-ocr/model")
        with dpg.tree_node(label="智谱AI(个人免费)"):
            dpg.add_input_text(label="API密钥",default_value=config.get("ocr/zhipu-ocr/api_key"),tag="ocr/zhipu-ocr/api_key",password=True)
            dpg.add_button(label="智谱Bigmodel官网，注册享无限次免费使用(GLM-4V-Flash模型)",tag="ocr_zhipu_text",callback=lambda: cbs.openlink("https://www.bigmodel.cn/invite?icode=Kb6taSxhmGss52jYOyx%2FarC%2Fk7jQAKmT1mpEiZXXnFw%3D"))
            dpg.add_combo(label="视觉模型选择",items=['GLM-4V-Flash'],default_value=config.get("ocr/zhipu-ocr/model","GLM-4V-Flash"),tag="ocr/zhipu-ocr/model")
        with dpg.tree_node(label="PaddleOCR"):
            dpg.add_combo(label="语言选择",tag="ocr/paddle-ocr/lang",items=["ch","en"],default_value=config.get("ocr/paddle-ocr/lang","ch"))
            dpg.add_combo(label="模型选择",tag="ocr/paddle-ocr/model",items=["PP-OCRv4","PP-OCRv3"],default_value=config.get("ocr/paddle-ocr/model","PP-OCRv4"))
        dpg.add_spacer(height=6)
        dpg.add_separator()
        with dpg.group(horizontal=True):
            dpg.add_button(label="保存OCR设置", callback=lambda: cbs.save_ocr_config())
        dpg.add_separator()

def create_func_gui():
    with dpg.collapsing_header(label="功能页面",default_open=True):
        with dpg.group(horizontal=False,label="functions"):
            dpg.add_text("功能界面")
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

def create_info_gui():
    with dpg.collapsing_header(label="关于本软件",default_open=True):
        with dpg.group(horizontal=False):
            dpg.add_text("当前版本：1.0.0")
            #dpg.add_text("最新版本：{}".format(utils.get_newest_version()))
            dpg.add_text("Github：https://github.com/destoryD/screen-searcher")
            dpg.add_text("本软件仅供学习交流使用，请勿用于商业用途。")
        with dpg.group(horizontal=True):
            dpg.add_button(label="项目主页",callback=lambda: cbs.openlink("https://github.com/destoryD/screen-searcher"))
            dpg.add_button(label="最新版本",callback=lambda: cbs.openlink("https://github.com/destoryD/screen-searcher/releases"))
            dpg.add_button(label="问题反馈",callback=lambda: cbs.openlink("https://github.com/destoryD/screen-searcher/issues"))
            dpg.add_button(label="加入交流QQ群",callback=lambda: cbs.openlink("https://qm.qq.com/q/kJ7lKBhtkc"))