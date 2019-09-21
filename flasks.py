import itertools
import logging
import time
import random
import utils

from utils.configs import get_config
from utils.listener import KeyboardListener
from utils.iterators import RandomKeyIterator
from threading import Thread, Event
from pynput.keyboard import Controller


class FlaskSequence:
    def __init__(self, keys: list, interval: tuple, random_keys: bool = True):
        self.keys = keys
        self.interval = interval
        self._iter_keys = RandomKeyIterator(keys) if random_keys else itertools.cycle(keys)

    @property
    def next_flask(self):
        delay = random.uniform(self.interval[0], self.interval[1])
        logging.debug(f"Sleeping for {delay}s")
        time.sleep(delay)
        return next(self._iter_keys)


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
            # Check if we're paused, if yes, block till Event is set again.
            logging.info("waiting for pause to be set")
            self.is_paused.wait()

            self.press_key(self.flasks.next_flask, self.release_delay)


if __name__ == "__main__":
    config = get_config()
    sequence = FlaskSequence(config['keys'], tuple(config['keys_delay']), random_keys=True)
    macro = FlaskMacro(sequence, tuple(config['press_release_delay']))
    logging.basicConfig(level=logging.DEBUG)
    macro.start()
