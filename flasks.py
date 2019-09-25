import logging
import time
import random

from utils.configs import get_config
from utils.listener import KeyboardListener
from utils.iterators import KeyIterator
from threading import Thread, Event
from pynput.keyboard import Controller


class FlaskSequence:
    def __init__(self, keys: list, interval: tuple, sequence_interval: tuple):
        self.keys = keys
        self.interval = interval
        self.sequence_interval = sequence_interval
        self._iter_keys = KeyIterator(keys)
        self.sequence_end = False

    @property
    def next_flask(self):
        if not self.sequence_end:
            delay = random.uniform(self.interval[0], self.interval[1])
            logging.debug(f"Sleeping for {delay}s")
            time.sleep(delay)
        else:
            delay = time.sleep(random.uniform(self.sequence_interval[0], self.sequence_interval[1]))
            logging.debug(f"Sleeping for {delay}s")
            self.sequence_end = False
        key = next(self._iter_keys)
        if key[1]:
            self.sequence_end = True
        return key[0]


class FlaskMacro:
    def __init__(self, flasks: FlaskSequence, release_delay: tuple = (0.04, 0.17)):
        self.controller = Controller()
        self.is_paused = Event()
        self.is_paused.set()
        self.flasks = flasks
        self.release_delay = release_delay
        self.keyboard_listener = KeyboardListener(self)

    @property
    def is_macro_paused(self):
        return not self.is_paused.is_set()

    def pause(self):
        self.is_paused.clear()

    def resume(self):
        self.is_paused.set()

    def press_key(self, key: str, delay_range: tuple = None):
        try:
            self.controller.press(key)

            if delay_range:
                delay = random.uniform(delay_range[0], delay_range[1])
                logging.debug(f"Sleeping for {delay}s")
                time.sleep(delay)

            self.controller.release(key)
        except (ValueError, AttributeError) as e:
            logging.error(f"{key} is not a valid press-able key.")

    def start(self):
        self.keyboard_listener.start()
        while True:
            # Check if we're paused, if yes, blo434ck till Event is set again.
            logging.info("waiting for pause to be set")
            self.is_paused.wait()

            self.press_key(self.flasks.next_flask, self.release_delay)


if __name__ == "__main__":
    config = get_config()
    sequence = FlaskSequence(config['keys'], tuple(config['keys_delay']), tuple(config['sequence_interval']))
    macro = FlaskMacro(sequence, tuple(config['press_release_delay']))
    logging.basicConfig(level=logging.DEBUG)
    macro.start()
