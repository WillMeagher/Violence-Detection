from collections import deque

class Buffer:
    def __init__(self, size):
        self.size = size
        self.buffer = deque(maxlen=size)

    def add(self, item):
        self.buffer.append(item)

    def get(self):
        return self.buffer