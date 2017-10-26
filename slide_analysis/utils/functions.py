from functools import reduce
from slide_analysis.descriptors import all_descriptors
from slide_analysis.utils.tile_class import Tile
import openslide


def _compose_util(f, g):
    return lambda *a, **kw: f(g(*a, **kw))


def compose(*fs):
    return reduce(_compose_util, fs)


def get_descriptor_class_by_name(name):
    return next((x for x in all_descriptors if x.__name__ == name), None)


def get_tile_from_coordinates( path, x_coord, y_coord, width, height):
    return Tile(x_coord, y_coord, width, height,
                openslide.open_slide(path).read_region((x_coord, y_coord), 0,
                                                       (width, height)).getdata())
