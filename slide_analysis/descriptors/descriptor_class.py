class Descriptor:
    def __init__(self):
        self.value = [0 for t in range(0, 256)]
        self.has_value = False

    def _calc(self):
        return

    def get_value(self):
        if self.has_value:
            return self.value
        else:
            self._calc()
            self.has_value = True
            return self.value