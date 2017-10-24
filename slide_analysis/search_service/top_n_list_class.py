from blist import sortedlist


class TopNList:
    MIN_IDX = 0

    def __init__(self, n):
        self._data = sortedlist([(0, 0)] * n)

    def __iter__(self):
        return iter(self._data)

    def __str__(self):
        return str(self._data)

    def update(self, element):
        if element > self._data[self.MIN_IDX]:
            del self._data[self.MIN_IDX]
            self._data.add(element)
