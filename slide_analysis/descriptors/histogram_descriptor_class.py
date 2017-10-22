import numpy
from slide_analysis.descriptors.constants import *


class HistogramDescriptor:
    def __init__(self, scheme, tile):
        (self.r_mod, self.g_mod, self.b_mod) = scheme
        self.tile = tile

    def calc(self):
        arr = numpy.array(self.tile.data)
        self.value = numpy.histogram((arr[:, 0] >> (8 - self.r_mod) << (8 - self.r_mod))
                                     + (arr[:, 1] >> (8 - self.b_mod) << self.g_mod)
                                     + (arr[:, 2] >> (8 - self.g_mod)),
                                     bins=numpy.arange(0, COLOR_RANGE))[0]
