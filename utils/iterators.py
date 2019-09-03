import random


class RandomKeyIterator:

    def __init__(self, keys: list):
        self.keys = list(set(keys))
        self.visited = list()

    def __iter__(self):
        return self

    def _reset(self):
        self.keys = self.visited
        self.visited = list()

    def __next__(self):
        if not self.keys:
            self._reset()

        key = random.choice(self.keys)
        self.keys.pop(self.keys.index(key))
        self.visited.append(key)
        return key
