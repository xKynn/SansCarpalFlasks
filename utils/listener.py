import logging
from pynput import keyboard


class KeyboardListener:
    def __init__(self, macro):
        self.macro = macro
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.chat_init = False

    def on_press(self, key):
        if self.chat_init and (str(key) == "Key.enter" or str(key) == "Key.esc"):
            self.chat_init = False
            self.resume_macro()
        elif str(key) == "Key.enter":
            self.chat_init = True
            self.pause_macro()
        elif str(key) == "Key.f8":
            if self.macro.is_macro_paused:
                self.resume_macro()
            else:
                self.pause_macro()



    def pause_macro(self):
        logging.info("Pausing.")
        self.macro.pause()

    def resume_macro(self):
        logging.info("Resuming.")
        self.macro.resume()

    def stop(self):
        self.listener.stop()

    def start(self):
        self.listener.start()
