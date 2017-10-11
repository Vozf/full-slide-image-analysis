from slide_analysis.descriptors.descriptor_class import Descriptor


class HistogramDescriptor(Descriptor):
    def __init__(self, tile, scheme):
        Descriptor.__init__(self, tile)
        self.scheme = scheme
        (self.r_mod, self.g_mod, self.b_mod) = self.scheme

    def rgb_use_scheme(self, rgb):
        (r, g, b) = rgb
        res = r >> (8 - self.r_mod) << (8 - self.r_mod)\
                    + g >> (8 - self.g_mod) << (8 - self.g_mod - self.r_mod)\
                    + b >> (8 - self.b_mod)

    def _calc(self):
        tile = self.tile
