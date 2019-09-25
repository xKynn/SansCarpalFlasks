class KeyIterator:

    def __init__(self, keys: list):
        self.keys = list(set(keys))
        self.counter = 1

    def __iter__(self):
        return self

    def __next__(self):
        looped = False
        if(len(self.keys) == self.counter):
            looped = True
            self.counter = 1
        else:
            self.counter += 1
        self.keys.append(self.keys[0])
        return (self.keys.pop(0), looped)