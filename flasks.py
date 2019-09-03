import itertools
import logging
import time
import random

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
        time.sleep(random.uniform(self.interval))
        return next(self._iter_keys)


class FlaskMacro:
    def __init__(self, flasks: FlaskSequence, release_delay: tuple = (0.1, 0.4)):
        self.controller = Controller()
        self.is_paused = Event()
        self.is_paused.set()
        self.flasks = flasks
        self.release_delay = release_delay
        #self.keyboard_listener = foo.bar()

    def pause(self):
        self.is_paused.clear()

    def resume(self):
        self.is_paused.set()

    def press_key(self, key: str, delay_range: tuple = None):
        try:
            self.controller.press(key)

            if delay_range:
                time.sleep(random.uniform(delay_range))

            self.controller.release(key)
        except (ValueError, AttributeError) as e:
            logging.error(f"{key} is not a valid press-able key.")

    def start(self):
        while True:
            # Check if we're paused, if yes, block till Event is set again.
            self.is_paused.wait()

            self.press_key(self.flasks.next_flask, self.release_delay)
