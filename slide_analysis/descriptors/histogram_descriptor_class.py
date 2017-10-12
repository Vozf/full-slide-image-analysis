from slide_analysis.descriptors.descriptor_class import Descriptor


class HistogramDescriptor(Descriptor):
    def __init__(self, scheme):
        Descriptor.__init__(self)
        (self.r_mod, self.g_mod, self.b_mod) = scheme

    def set_tile(self, tile):
        self.tile = tile

    def set_val(self, value):
        self.has_value = True
        self.value = value

    def get_simplified(self, rgba):
        (r, g, b, a) = rgba
        return (r >> (8 - self.r_mod) << (8 - self.r_mod))\
                    + (g >> (8 - self.g_mod) << (8 - self.g_mod - self.r_mod))\
                    + (b >> (8 - self.b_mod))

    def _calc(self):
        for i in range(0, len(self.tile.data)):
            self.value[self.get_simplified(self.tile.data[i])] += 1
