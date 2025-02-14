import keyboard
from config import config
import callbacks as cbs

def handle_hotkey():
    keyboard.add_hotkey(config.get('hotkey_capture','ctrl+q'),cbs.capture_interactive_screenshot)
    keyboard.add_hotkey(config.get('hotkey_search','ctrl+w'), cbs.search_question_wrapper)
