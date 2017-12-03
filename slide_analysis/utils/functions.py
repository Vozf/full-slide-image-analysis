from functools import reduce

import numpy
import openslide

from slide_analysis.descriptors import all_descriptors
from slide_analysis.utils.tile_class import Tile


def _compose_util(f, g):
    return lambda *a, **kw: f(g(*a, **kw))


def compose(*fs):
    return reduce(_compose_util, fs)


def get_descriptor_class_by_name(name):
    return next((x for x in all_descriptors if x.__name__ == name), None)


def get_tile_from_coordinates(path, x_coord, y_coord, width, height):
    return Tile(x_coord, y_coord, width, height,
                openslide.open_slide(path).read_region((x_coord, y_coord), 0,
                                                       (width, height)))


def get_tiles_coords_from_indexes(indexes, step, img_w):
    num_cols = int(img_w / step)
    row = (indexes / num_cols).astype(int)
    column = indexes - row * num_cols
    y_coord = row * step
    x_coord = column * step
    return numpy.array([x_coord, y_coord]).T
