import numpy
from slide_analysis.descriptors.constants import *


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
        self.desc_arr = numpy.empty([len(tile_stream), COLOR_RANGE], dtype=int)
        self.iteration = 0
        tile_stream.for_each(lambda tile: self._put_to_arr(self.calc(tile)))
        return self.desc_arr

    def _put_to_arr(self, desc):
        self.desc_arr[self.iteration] = desc
        self.iteration += 1
