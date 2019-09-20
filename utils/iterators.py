class RandomKeyIterator:

    def __init__(self, keys: list):
        self.keys = list(set(keys))

    def __iter__(self):
        return self

    def __next__(self):
        self.keys.append(self.keys[0])
        return self.keys.pop(0)