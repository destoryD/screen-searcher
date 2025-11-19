# src/main.py
import dearpygui.dearpygui as dpg
from config import config
import hotkeys
import gui
import callbacks as cbs

try:
    from version import __version__ as APP_VERSION
except ImportError:
    APP_VERSION = "unknown" 

def init_settings():
    dpg.set_viewport_always_top(config.get("always_on_top", False))

if __name__ == '__main__':
    dpg.create_context()

    # 加载字体
    with dpg.font_registry():
        with dpg.font("resources/SarasaUiCL-Bold.ttf", 16) as font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
            dpg.add_font_range(0x1, 0x400)
            dpg.bind_font(font)

    dpg.create_viewport(title=f'Searcher ver: {APP_VERSION}', width=700, height=800, min_width=400, min_height=300,small_icon="resources/logo.ico", large_icon="resources/logo.ico")

    with dpg.window(tag="MainWindow"):
        gui.create_software_settings_gui()
        gui.create_search_gui()
        gui.create_ocr_gui()
        gui.create_func_gui()
        gui.create_log_gui()
        gui.create_info_gui(ver=APP_VERSION)

    init_settings()
    cbs.set_ocr_model(config.get("ocr/model"))
    cbs.set_api_model(config.get("search/tiku"))
    hotkeys.handle_hotkey()
    dpg.set_primary_window("MainWindow", True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    # 应用窗口置顶配置
    dpg.start_dearpygui()
    dpg.destroy_context()
