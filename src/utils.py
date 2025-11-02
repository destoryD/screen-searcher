# src/utils.py
import datetime
import pyperclip
import requests

def log_message(message, log_output_tag="log_output", max_length=10):
    """
    更新日志消息到 Dear PyGui 的文本组件。

    Args:
        message (str): 要显示的消息。
        log_output_tag (str): 日志输出文本组件的tag。
        max_length (int, optional): 最大显示长度，None表示不限制。
    """
    import dearpygui.dearpygui as dpg  # 避免循环导入
    #添加时间前缀
    pre_message = dpg.get_value(log_output_tag)
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")  # 自定义时间格式
    message = f"[{formatted_time}] {message}\n"+pre_message
    length = str(message).count('\n')
    if max_length and length >= max_length:
        message = message.split('\n')[:max_length]  # 保留最新的max_length行
        message = '\n'.join(message)
    dpg.set_value(log_output_tag, message)

def copy_to_clipboard(message):
    pyperclip.copy(message)

def get_newest_version():
    '''
        获取最新版本号，使用GitHub API
    '''
    try:
        resp = requests.get("https://api.github.com/repos/destoryD/screen-searcher/releases/latest")
        resp.raise_for_status()  # 检查HTTP错误
        latest = resp.json()
        latest_version = latest["tag_name"].lstrip("v")
        return latest_version
    except:
        # 如果GitHub API失败，回退到备用API
        try:
            api_url = "https://www.datam.site/addons/screen_searcher.json"
            data = requests.get(api_url).json()
            return data["newest_version"]
        except:
            return "1.0.0"

def show_message_box(message, title="提示", message_type="info"):
    """
    显示消息弹窗的通用函数

    Args:
        message (str): 要显示的消息内容
        title (str): 弹窗标题
        message_type (str): 消息类型 ("info", "warning", "error", "success")
    """
    import dearpygui.dearpygui as dpg  # 避免循环导入

    # 根据消息类型设置不同的颜色和图标
    colors = {
        "info": (0, 100, 200, 255),    # 蓝色
        "warning": (255, 165, 0, 255), # 橙色
        "error": (255, 0, 0, 255),     # 红色
        "success": (0, 255, 0, 255)    # 绿色
    }

    # 确保弹窗唯一性，如果已存在则删除
    if dpg.does_item_exist("message_box"):
        dpg.delete_item("message_box")

    # 获取视口尺寸以居中显示弹窗
    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()
    window_width = 400
    window_height = 200
    center_x = (viewport_width - window_width) // 2
    center_y = (viewport_height - window_height) // 2

    # 创建模态弹窗
    with dpg.window(tag="message_box", modal=True, show=True, pos=[center_x, center_y], width=window_width, height=window_height, no_title_bar=False):
        dpg.add_text(title, color=colors.get(message_type, colors["info"]))
        dpg.add_spacer(height=10)
        dpg.add_text(message)
        dpg.add_spacer(height=10)
        with dpg.group(horizontal=True):
            dpg.add_button(label="确定", width=100, height=30, callback=lambda: dpg.delete_item("message_box"))

def check_update(current_version):
    try:
        resp = requests.get("https://api.github.com/repos/destoryD/screen-searcher/releases/latest")
        resp.raise_for_status()  # 检查HTTP错误
        latest = resp.json()
        latest_version = latest["tag_name"].lstrip("v")
        
        # 使用 packaging.version 进行安全的版本比较
        from packaging import version
        if version.parse(latest_version) > version.parse(current_version):
            return {
                "has_update": True,
                "latest_version": latest_version,
                "release_url": latest["html_url"],
                "download_url": latest.get("assets", [{}])[0].get("browser_download_url", latest["html_url"]) if latest.get("assets") else latest["html_url"]
            }
        else:
            return {"has_update": False}
    except requests.exceptions.RequestException as e:
        print("网络请求错误:", e)
        return {"has_update": False, "error": f"网络请求错误: {e}"}
    except KeyError as e:
        print("响应数据格式错误:", e)
        return {"has_update": False, "error": f"响应数据格式错误: {e}"}
    except Exception as e:
        print("检查更新时发生未知错误:", e)
        return {"has_update": False, "error": f"未知错误: {e}"}