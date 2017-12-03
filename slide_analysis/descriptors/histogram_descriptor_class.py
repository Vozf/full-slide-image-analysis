import numpy

from slide_analysis.descriptors.constants import *
from concurrent.futures import ProcessPoolExecutor


class HistogramDescriptor:
    def __init__(self, scheme):
        (self.r_mod, self.g_mod, self.b_mod) = scheme

    def calc(self, tile):
        arr = numpy.array(tile.data)
        value = numpy.histogram((numpy.ravel(arr[:, :, 0]) >> (8 - self.r_mod) << (8 - self.r_mod))
                                + (numpy.ravel(arr[:, :, 1]) >> (8 - self.b_mod) << self.g_mod)
                                + (numpy.ravel(arr[:, :, 2]) >> (8 - self.g_mod)),
                                bins=numpy.arange(0, COLOR_RANGE + 1))[0]
        return value

    def get_descriptor_array(self, tile_stream):
        with ProcessPoolExecutor() as executor:
            self.descr_arr = list(executor.map(self.calc, tile_stream))
            return self.descr_arr
