import time
import keyboard
import win32clipboard

class ClipboardWatcher:
    def __init__(self):
        self.setup_hotkey()

    def get_clipboard_data(self):
        win32clipboard.OpenClipboard()
        data = None
        try:
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_TEXT):
                data = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT).decode("utf-8")
        finally:
            win32clipboard.CloseClipboard()
        return data
    
    def copy_to_clipboard(self, data):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(data)
        win32clipboard.CloseClipboard()

    def modify_data(self, data: str) -> str:
        sentences = data.split('. ')
        return '. '.join(sentence.capitalize() for sentence in sentences)
    
    def get_data(self):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.CloseClipboard()

        keyboard.press_and_release('ctrl+x')

        time.sleep(0.01)

        if data := self.get_clipboard_data():
            self.copy_to_clipboard(self.modify_data(data))
            keyboard.press_and_release('ctrl+v')

    def handle_hotkey(self):
        self.get_data()

    def setup_hotkey(self):
        keyboard.add_hotkey('f8', self.handle_hotkey)

    def start_listening(self):
        keyboard.wait('esc')

# Utilisation de la classe ClipboardWatcher
watcher = ClipboardWatcher()
watcher.start_listening()