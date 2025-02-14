# src/utils.py
import datetime
import pyperclip
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