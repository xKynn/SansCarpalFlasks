from pynput import keyboard
from flasks import FlaskMacro


class KeyboardListener:
    def __init__(self, macro: FlaskMacro):
        self.macro = macro
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.chat_init = False

    def on_press(self, key):
        if str(key) == "Key.enter":
            self.chat_init = True
            self.pause_macro()
        if self.chat_init and (str(key) == "Key.Enter" or str(key) == "Key.esc"):
            self.chat_init = False

    def pause_macro(self):
        self.macro.pause()

    def resume_macro(self):
        self.macro.resume()

    def start(self):
        self.listener.start()
