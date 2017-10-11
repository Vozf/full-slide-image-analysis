from slide_analysis.descriptors.descriptor_class import Descriptor


class TestDescriptor(Descriptor):
    def __init__(self):
        Descriptor.__init__(self)

    def set_tile(self, tile):
        self.tile = tile

    def set_val(self, val):
        self.has_value = True
        self.value = val

    def _calc(self):
        (r, g, b, a) = self.tile.data[0]
        self.value = r + g + b
        self.has_value = True

    def get_value(self):
        if self.has_value:
            return self.value
        else:
            self._calc()
            self.has_value = True
            return self.value
