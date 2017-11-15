class TopNList:
    MIN_IDX = 0

    def __init__(self, n):
        self._data = list([(0, 0)] * n)

    def __iter__(self):
        return iter(self._data)

    def __str__(self):
        return str(self._data)

    def update(self, element):
        if element[0] > self._data[self.MIN_IDX][0]:
            del self._data[self.MIN_IDX]
            self._data.append(element)
            self._data.sort(key=lambda x: x[0])
