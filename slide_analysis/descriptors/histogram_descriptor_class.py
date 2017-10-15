import numpy


class HistogramDescriptor:
    def __init__(self, scheme):
        (self.r_mod, self.g_mod, self.b_mod) = scheme

    def calc_by_tile(self, tile):
        self.tile = tile
        arr = numpy.array(tile.data)
        self.value = numpy.histogram((arr[:, 0] >> (8 - self.r_mod) << (8 - self.r_mod))
                                     + (arr[:, 1] >> (8 - self.b_mod) << self.g_mod)
                                     + (arr[:, 2] >> (8 - self.g_mod)), bins=numpy.arange(0, 256))[0]
        del tile.data
